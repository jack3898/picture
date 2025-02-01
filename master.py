# This is the main python script!

from utils.btn import handle_buttons
from inky.auto import auto
from utils.img import get_dir_image, get_unsplash_image
from utils.usb import toggle_usb_connectivity, internal_mount_location, run_command

def load_dir_image():
    print("Loading image from directory...")
    inky = auto(ask_user=True)
    image = get_dir_image(internal_mount_location)
    inky.set_image(image, saturation=0.6)
    inky.show()

def load_unsplash_image():
    print("Loading image from Unsplash...")
    inky = auto(ask_user=True)
    image = get_unsplash_image()
    inky.set_image(image, saturation=0.6)
    inky.show()

def handle_button(_, btn_info):
    print(f"Button {btn_info[2]} pressed!")
    (index) = btn_info[0]

    if index == 0:
        toggle_usb_connectivity(usb=False)
        load_dir_image()
    elif index == 1:
        toggle_usb_connectivity(usb=True)
    elif index == 2:
        load_unsplash_image()
    elif index == 3:
        run_command("sudo reboot")

print("Picture frame active! Press Ctrl+C to exit!\n")

handle_buttons(handle_button)
