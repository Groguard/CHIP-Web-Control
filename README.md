# CHIP-Web-Control
Control C.H.I.P's GPIO from the web using flask.
Temperature and Humidity readings not working yet.

Installation Guide:

sudo apt-get update

sudo apt-get install git build-essential python3 python3-dev python3-pip flex bison

sudo pip3 install flask

Installing CHIP_IO from xtacocorex git https://github.com/xtacocorex/CHIP_IO:

  git clone https://github.com/atenart/dtc
  
  cd dtc
  
  make
  
  sudo  make install PREFIX=/usr
  
  cd
  
  git clone git://github.com/xtacocorex/CHIP_IO.git
  
  cd CHIP_IO
  
  sudo python3 setup.py install
  
  cd
  
  sudo rm -rf CHIP_IO

Running the software:

1. Navigate to the folder which you downloaded CHIP-Web-Control software.

2. Run the command sudo python3 CHIPWebControlV0.5.py

3. You should now be able to navigate to your CHIPs ip address like "192.168.1.22:8080" Server is running on port 8080 so make sure to include that.


Patch notes for CHIP-Web-Control V0.5:

- All flask related stuff working

- GPIO control works
- Timers work
