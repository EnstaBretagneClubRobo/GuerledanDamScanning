# GuerledanDamScanning
Repository for scanning the Guerledan Water Dam with a front sonar

## Required packages
 - hokuyo_node
 - xsens_driver
 - nmea_navsat_driver:
 	- just execute `python setup.py install` in the folder sensors/nmea_navsat_driver

## Required library for maestro
- [Pololu Maestro Controller Drivers](https://www.pololu.com/docs/0J40/3.b):  
	- Read README.txt to install dependencies and rights.  
	- Activate **USB Dual Port** in the *Serial Settings* tab of the app **Pololu Maestro Control Center** (`./MaestroControlCenter`).
