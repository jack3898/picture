# Fancy e-ink picture frame

Once the picture frame is all configured, it should be a set and forget. But sometimes more technical work needs to happen, so this is here to make sure it's all written down for future reference.

## Controls:

- Button 1 picks a random picture uploaded to this picture frame.
- Button 2 enables USB connectivity mode.
- Button 3 picks a random picture from the internet. Namely, a website called "Unsplash".

## Add more pictures:

1. Plug the picture frame into your computer using a USB cable.
2. Press button 2.
3. Make sure the image is a reasonable file size (~100kb), and has the dimensions of 800 x 480px.
   - I recommend https://squoosh.app as a convenient online tool to resize and convert images.
   - There is also Microsoft PowerToys, which can let you resize in bulk all in one go!
4. Then when you have uploaded all of your pictures unmount this device safely, and press button 1 again. That will disable USB connectivity and load a random picture from your pool.

## Change the WiFi:

The easiest method is to just plug the device into a screen via HDMI, and use `sudo raspi-config` to change network options.

6. Transfer the MicroSD card back and power on the device.
7. 🤞

## More notes

### Venv
Ensure you activate the correct virtual environment before running any inky Python scripts.

### First time setup

- Clone this repository in `~/picture`
- Clone https://github.com/pimoroni/inky in `~/inky`
- `cd ~/inky` then execute the `install.sh` file. Follow the steps.
- Run `sudo raspi-config`
- Go to `Interface Options` and enable `SPI` and `I2C`
- `sudo nano /boot/firmware/config.txt` and add `dtoverlay=dwc2`

### Systemd configuration

This is used to launch the Python script on boot, and also relaunches it if it crashes.

This assumes there is a Python virtual environment valled `pimoroni`. This is created when running the inky install script from the Pimoroni GitHub. Feel free to change it if a different venv is being used.

Create a new `picture.service` file in `/etc/systemd/system` and paste the below configuration:

```
[Unit]
Description=Pictureframe
After=network.target

[Service]
ExecStart=/home/pi/.virtualenvs/pimoroni/bin/python /home/pi/picture/master.py
WorkingDirectory=/home/pi
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

To enable and register this service run these commands:

```sh
sudo systemctl daemon-reload
```

```sh
sudo systemctl enable picture.service
```

```sh
sudo systemctl start picture.service
```

Make sure it's working with:

```sh
sudo systemctl status picture.service
```

Stop at any time with:

```sh
sudo systemctl stop picture.service
```
