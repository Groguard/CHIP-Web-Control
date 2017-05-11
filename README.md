## C.H.I.P GPIO Web Control
This is a program that I orginally had made for the raspberry pi, and I have since ported it over to C.H.I.P made by NextThingCo.
The purpose of this program is to allow easy control and reading of the GPIO of C.H.I.P on the web. I originally made it to control my indoor garden setup, but there are many other uses this software could be used for if you want to control the GPIO of C.H.I.P from a browser.  

## How to install:

sudo apt-get update

sudo apt-get install git build-essential python3 python3-dev python3-pip flex bison screen

sudo pip3 install flask

## Installing CHIP_IO

from @xtacocorex git https://github.com/xtacocorex/CHIP_IO

git clone https://github.com/atenart/dtc

cd dtc

make

sudo make install PREFIX=/usr

cd

git clone git://github.com/xtacocorex/CHIP_IO.git

cd CHIP_IO

sudo python3 setup.py install

cd

sudo rm -rf CHIP_IO

## Downloading and running the software:

git clone git://github.com/Groguard/CHIP-Web-Control.git

cd CHIP-Web-Control

sudo python3 main.py

You should be able to navigate in your browser and view the web page at yourchipsip:8080
With the program running in a screen, you can disconnect from the terminal and it will continue to run. If it should shutdown for some reason it will need to be restarted using steps 4-5. I'm working on a script to make it run at start, should have the soon.
