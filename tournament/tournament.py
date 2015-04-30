#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(name) AS num FROM players")
    number = c.fetchall()
    db.close()
    return number[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    player_count = countPlayers()
    db = connect()
    c = db.cursor()
    c.execute('''create view playedmatches as select p1 as player, count(p1) as matchcount from matches group by p1 union all select p2 as player, count(p2) as matchcount from matches group by p2;
        select players.id, players.name, coalesce(w.wins,0) as wins, coalesce(m.matchcount,0) as matches from players left join (select player, matchcount from playedmatches) as m on m.player=players.id left join(select winner, count(winner) as wins from matches group by winner) as w on players.id = w.winner;''')
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (p1, p2, winner) VALUES (%s, %s, %s);", (winner, loser, winner,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    matchup = []
    standings = sorted(playerStandings(), key=lambda wins: wins[3])
    total_matches = len(standings)/2
    pos = 0
    for i in range(total_matches):
        matchup.append((standings[pos][0],standings[pos][1],standings[pos+1][0],standings[pos+1][1]))
        pos += 2
    print matchup
    return matchup

    # Match players that follow each other in the standings, if they havent played together before
    #
