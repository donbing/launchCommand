# rocket launchers
```gherkin
Feature: M&S missile launcher web service
    As a website visitor 
    So that i have fun shooting chris with foam missiles
    I want a webcam view from the launcher, and to be able to move and fire the launcher
```

# setup
```sh
# install pyusb
sudo pip install pyusb
# install picamera
sudo pip install picamera
# install flask
sudo pip install flask
```

## udev permissions
In order to connect to the USB without being a super user, we need to add an udev rule.
```sh
# 666 perms on device 1130:0202
sudo touch /etc/udev/rules.d/99-missile.rules
sudo echo SUBSYSTEM=="usb", ATTR{idVendor}=="1130", ATTR{idProduct}=="0202", MODE="0666" > /etc/udev/rules.d/99-missile.rules
# restart udev 
sudo udevadm trigger
```

## github links
* [Retaliation](https://github.com/codedance/Retaliation)
* [sentinel](https://github.com/AlexNisnevich/sentinel)
* [usb-missile-launcher](https://github.com/pddring/usb-missile-launcher)
* [tenx-missile](https://github.com/anxodio/tenx-missile)
