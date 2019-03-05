# Master Thesis project

# Instructions (Work in Progress)

Start the simulator by running:

Execute gui.py:
```shell
user@computer:/../ANT$ python3 gui.py
```

# Install instructions (Unix only)
Based on python3
 - This program uses compiled c/c++ files. Make sure that both a c and c++ compiler are installed
 - (optional) make sure pip3 is installed: ```user@computer:~$ sudo apt-get install python3-pip```
 - (optional) use virtual environment, make sure virtualenv is available: ```user@computer:~$  sudo apt install virtualenv ```
 - (optional) DB browser for sqlite ```user@computer:~$  sudo apt install sqlitebrowser ```
 - (optional) Make a virtual environment ``` user@computer:~$ virtualenv pythonenvs/theANT3000 -p python3 ``` and ```user@computer:~$  source
  pythonenvs/theANT3000/bin/activate ```
 - The visualization module makes use of tkinter: ``` user@computer:~$ sudo apt install python3-tk ```
 - Install dependencies: ``` pip3 install ...```
 - Clone the project:
```shell
  user@computer:~$ git clone https://github.com/Elmosnewshoes/Stigmergy/ theANT3000
  user@computer:~$ cd theANT3000
  ```
 - Create the database: ``` user@computer:~/theANT3000$ python deploy.py ```
 - Let python compile the source code: ``` user@computer:~/theANT3000$ python setup.py build_ext -i ```
 - Launch! ``` user@computer:~/theANT3000$ python gui.py ```
 - Click the run button to populate the database for the first time
## Package dependencies
 - numpy
 - pysqlite3
 - matplotlib
 - pyqt5
 - cython
 - pandas

## Troubleshooting
```shell
cythonic/plugins/functions.c:606:10: fatal error: numpy/arrayobject.h: No such file or directory
 #include "numpy/arrayobject.h"
          ^~~~~~~~~~~~~~~~~~~~~
compilation terminated.
error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```
This is bad. Probably numpy is installed through pip, try: ``` sudo apt-get install python-numpy ``` then, recompile
```shell
warning: #warning "Using deprecated NumPy API, disable it by " "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
```
This is normal and should not affect the working of the program
```shell
 warning: cythonic/core/map.pyx:47:12: Unsigned index type not allowed before OpenMP 3.0
 ```
 This is normal and should not affect the working of the program
