#Tournament database

##How to run

To run the database and tournament_test.py files from a virtual machine on the command line, follow these steps:

* from the command line, cd into the fullstack-tournament folder;
* run the command vagrant up, which will configure vagrant and install all dependencies for the vm;
* run the command vagrant ssh, which logs you into a ubuntu VM;
* cd into /vagrant/tournament;
* run the command psql;
* run the command \i tournament.sql to setup the db;
* quit psql by entering the command \q;
* run the command python tournament_test.py to run the tests on the db;

You should be able to see all success messages from the tests if they are executed correctly.

##How to quit the VM

To quit the VM, simply enter the command sudo shutdown now. You will be taken back to the root folder. To close vagrant, enter the command vagrant halt.
