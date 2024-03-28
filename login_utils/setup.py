from . import login
from .util import *
import time, os, pdb


def disable_keyboard():
    os.system(f"adb install -r Null_Keyboard-one.apk")
    adb_exec("ime set com.wparam.nullkeyboard/.NullKeyboard", 2)

def setup_device():
    # For Text Input Interface
    disable_keyboard()

def setup_app(apk):
    ensure_reinstalled(apk)
    start_app(apk)
    time.sleep(10)
    return login.login_app(apk)

def simple_setup_app(apk):
    ensure_reinstalled(apk)
    start_app(apk)

def setup_googleaccount():
    return login.login_google(username="test.utd.test@gmail.com", password="Wojiuyaobaipiao")

if __name__ == '__main__':
    setup_app("bookingcom")
