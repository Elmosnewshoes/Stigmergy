# Master Thesis project

# Instructions (Work in Progress)

Start the simulator by running:

Execute gui.py:
```shell
user@computer:/../ANT$ python3 gui.py
```

# Install instructions (Unix only)
Based on python3
 - (optional) make sure pip3 is installed: ```user@computer:~$ sudo apt-get install python3-pip```
 - (optional) use virtual environment, make sure virtualenv is available: ```user@computer:~$  sudo apt install virtualenv ```
 - (optional) DB browser for sqlite ```user@computer:~$  sudo apt install sqlitebrowser ```
 - (optional) Make a virtual environment ``` user@computer:~$ virtualenv theANT3000 -p python3 ``` and ```user@computer:~$  source theANT3000/bin/activate ```
 - Install dependencies: ``` pip3 install ...```
 - Clone the project:
```shell
  user@computer:~$ git clone https://github.com/Elmosnewshoes/Stigmergy/ theANT3000
  user@computer:~$ cd theANT3000
  ```
 - Create the database: ``` user@computer:~/theANT3000$ python deploy.py ```
 - Let python compile the source code: ``` user@computer:~/theANT3000$ python setup.py build_ext -i ```
## Package dependencies
 - numpy
 - sqlite3
 - matplotlib
 - pyqt5
 - cython
