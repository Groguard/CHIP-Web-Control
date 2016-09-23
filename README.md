## C.H.I.P GPIO Web Control - V0.6

**Only for kernel 4.4**

<a href="http://imgur.com/OBdLqax"><img src="http://i.imgur.com/OBdLqaxl.png" title="source: imgur.com" /></a>

<a href="http://imgur.com/UJYgUO1"><img src="http://i.imgur.com/UJYgUO1h.jpg" title="source: imgur.com" /></a>

## Install the modfied kernel to allow reading the sensor:

**Credit to @danjperron for the kernel.**

**Copy and paste exactly as it is.

sudo bash (enter password)

cd /Dont forget the "/"

wget https://dl.dropboxusercontent.com/u/48891705/chip/kernel-4.4.11-DJP.tgz

tar -xzf kernel-4.4.11-DJP.tgz

rm kernel-4.4.11-DJP.tgz

reboot

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

**Open the config.cfg file and setup your pins, names, and timers.**

screen

sudo python3 CHIPWebControl.py

You should be able to navigate in your browser and view the web page at yourchipsip:8080
With the program running in a screen, you can disconnect from the terminal and it will continue to run. If it should shutdown for some reason it will need to be restarted using steps 4-5. I'm working on a script to make it run at start, should have the soon.

## DHT22 Wiring
[img]/uploads/nextthing/original/2X/4/4bda21d7ce4eb36122fe230f78f365073594afa6.png[/img]

<a href="http://imgur.com/RsKuapf"><img src="http://i.imgur.com/RsKuapf.png" title="source: imgur.com" /></a>
