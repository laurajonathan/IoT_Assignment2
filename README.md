# IoT_Assignment2

This project is intended to read the data from the SenseHat sensor on Raspberry Pi 3 B which will run automatically via cronjob. Including the basic monitor, report, bluetooth, notification and analytics modules.

## Getting Started

The tools for this project are
* [Raspberry Pi + SenseHat](https://au.element14.com/element14/pi3-ibm-iot-learnkit/raspberry-pi-3-ibm-iot-learner/dp/2606882) - The raspberry pi used

### Prerequisites

The programming language and library used
```
Python 3.5+
Matplotlib
Plotly
Pybluez
Pylint3
```

The external API included
```
PushBullet
Plotly (For the online plot but not included in this project)
```

### Installing

Install the library and bluetooth modules using apt and pip3

```
sudo apt install bluetooth bluez blueman bluez-tools
pip3 install matplotlib plotly pybluez pylint3
```

### Coding Style

This project is built by following [PEP 8](https://www.python.org/dev/peps/pep-0008/) style and the linting tool used is pylint3

```
pylint3 python_file.py
```

## Structure

### Python modules

This project consists of 5 python modules
* monitor_and_notify.py
* create_report.py
* bluetooth_local.py
* analytics.py
* virtual_sense_hat.py

### Cron Job
The cron job will run the script with the setting in /etc/cron.d/IoT_Assignment1
```
* * * * * pi /path_to_script/run_monitor.sh
@reboot pi /path_to_script/run_bluetooth.sh
```
This project has 2 bash script
* run_monitor.sh
* run_bluetooth.sh

## IDE tools

* VScode
* Spyder

## Versioning

Version 1.0

## Authors

* Suwat Tangtragoonviwatt (s3710374)
* Laura Jonathan (s3696013)

## License

This project is licensed under the RMIT University

## Acknowledgments

* Shekhar Kalra (Project Mentor)
* Matthew Bolger (Project Advisor)
