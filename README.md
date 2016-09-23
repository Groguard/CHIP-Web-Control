

## C.H.I.P GPIO Web Control - V0.6

**Only for kernel 4.4**

<a href="http://imgur.com/OBdLqax"><img src="http://i.imgur.com/OBdLqax.png" title="source: imgur.com" /></a>
<a href="http://imgur.com/cclHPII"><img src="http://i.imgur.com/cclHPII.jpg" title="source: imgur.com" /></a>

**Install the modfied kernel to allow for reading the sensor**

Credit to danjperron on the nextthingco forums for the kernel.

Copy and paste exactly as it is.

1. sudo bash (enter password)
2. cd /   <--- Dont forget the "/"
3. wget https://dl.dropboxusercontent.com/u/48891705/chip/kernel-4.4.11-DJP.tgz
4. tar -xzf kernel-4.4.11-DJP.tgz
5. rm kernel-4.4.11-DJP.tgz
6. reboot

**How to install**

1. sudo apt-get update
2. sudo apt-get install git build-essential python3 python3-dev python3-pip flex bison screen
3. sudo pip3 install flask

**Installing CHIP_IO from @xtacocorex git https://github.com/xtacocorex/CHIP_IO:**

1. git clone https://github.com/atenart/dtc
2. cd dtc
3. make
4. sudo make install PREFIX=/usr
5. cd
6. git clone git://github.com/xtacocorex/CHIP_IO.git
7. cd CHIP_IO
8. sudo python3 setup.py install
9. cd
10. sudo rm -rf CHIP_IO


**Downloading and running the software:**

1. git clone git://github.com/Groguard/CHIP-Web-Control.git
2. cd CHIP-Web-Control
3. Open the config.cfg file and setup your pins, names, and timers
4. screen
5. sudo python3 CHIPWebControl.py
6. You should be able to navigate in your browser and view the web page at yourchipsip:8080

With the program running in a screen, you can disconnect from the terminal and it will continue to run. If it should shutdown for some reason it will need to be restarted using steps 4-5. I'm working on a script to make it run at start, should have the soon.

<a href="http://imgur.com/RsKuapf"><img src="http://i.imgur.com/RsKuapf.png" title="source: imgur.com" /></a>
