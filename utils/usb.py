import os
import subprocess
from pathlib import Path

img_location = os.path.expanduser("~/piusb.img")
internal_mount_location = os.path.expanduser("~/usb")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print(f"Exception raised when running command '{command}', {e}")
        return "", str(e)

def check_udc():
    output, _ = run_command("ls /sys/class/udc/")
    return bool(output)

def create_backing_file_if_not_exists():
    if not os.path.exists(img_location):
        print("Creating backing file...")
        run_command(f"sudo dd if=/dev/zero of={img_location} bs=1M count=4096")
        run_command(f"sudo mkfs.vfat {img_location}")
        run_command(f"sudo chmod 666 {img_location}")
    else:
        print("Backing file already exists.")

def enable_dwc2():
    output, _ = run_command("lsmod | grep dwc2")

    if not "dwc2" in output:
        print("Loading dwc2 module...")
        run_command("sudo modprobe dwc2")

def check_usb_connection():
    output, _ = run_command("dmesg | tail -n 30")
    print("Checking dmesg logs...")
    print(output)

def unset_storage():
    run_command(f"sudo umount {internal_mount_location}")
    run_command("sudo modprobe -r g_mass_storage")

def enable_usb_storage():
    print("Enabling USB Mass Storage Mode...")
    unset_storage()

    # Set a nice name for the computer connecting to this device
    run_command(f"sudo fatlabel {img_location} Pictureframe")
    # Enable mass storage
    run_command(f"sudo modprobe g_mass_storage file={img_location} removable=1")

def disable_usb_storage():
    print("Disabling USB Mass Storage Mode...")
    unset_storage()

    # Mount locally for Pi access
    run_command(f"sudo mount -o loop {img_location} {internal_mount_location}")

def create_internal_mountpoint():
    print(f"Checking {internal_mount_location}...")
    folder_path = Path(internal_mount_location)
    os.makedirs(folder_path, exist_ok=True)

def toggle_usb_connectivity(usb = False):

    print("Checking UDC availability...")
    if not check_udc():
        print("No available UDC found. Ensure the Pi is in OTG mode and reboot.")
        return

    print("Ensuring backing file exists...")
    create_backing_file_if_not_exists()

    print("Checking USB connection...")
    check_usb_connection()

    if usb:
        print("Loading necessary kernel modules...")
        enable_dwc2()

        print("Setting up Raspberry Pi as a USB storage device...\n")
        enable_usb_storage()
    else:
        print("Giving Pi read access to USB files...\n")
        create_internal_mountpoint()
        disable_usb_storage()

    print("Success!")