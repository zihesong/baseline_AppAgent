from util import *


    
    
def login_youtubemusic(username, password= "Wojiuyaobaipiao"):
    time.sleep(3)
    # Cancel the promotion if popped up
    adb_input("tap 714 95")
    adb_input("tap 49 79")    


def login_spotify(username, password= "Wojiuyaobaipiao!"):
    time.sleep(3)
    adb_input("tap 383 1072", 1)
    
    # ID
    adb_input("tap 121 307", 0.5)    
    adb_input("text " + username, 1)
    
    # Password
    adb_input("keyevent KEYCODE_TAB", 0.5)
    adb_input("text " + password, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)

def login_pandora(password = "Wojiuyaobaipiao"):
    time.sleep(5)
    # Tap to sign in w/ Google
    adb_input("tap 384 1097", 8)
    # Skip picking artist
    adb_input("tap 686 116")
    adb_input("tap 355 888")
    
    # adb_input("tap 135 454", 2)
    # adb_input("tap 300 600", 1)
    # adb_input("tap 176 653", 1)
    # adb_input("text " + password, 1)   
    # adb_input("tap 684 1132", 2)
    # adb_input("tap 684 1132", 2)
    # adb_input("tap 408 585") 


def login_maps():
    pass

def login_waze():
    time.sleep(5)
    # Location Permission
    adb_input("tap 398 1073", 2)
    adb_input("tap 381 837", 5)
    # Login Page
    adb_input("tap 386 865", 5)
    adb_input("tap 403 1105", 2) # Continue as guest
    adb_input("tap 687 109")

def login_mapquest():
    time.sleep(2)
    adb_input("tap 639 748", 2)
    adb_input("tap 381 837", 3)
    
def login_booking():
    time.sleep(2)
    adb_input("tap 369 461", 2)
    adb_input("tap 376 633", 8)
    # Cancel AI assistant
    adb_input("tap 361 1120", 3)
    adb_input("tap 65 116", 2)

def login_tripadvisor():
    time.sleep(2)
    adb_input("tap 397 733", 2)
    adb_input("tap 376 633", 5)
    adb_input("tap 343 843", 2)
    adb_input("tap 397 835", 2)
    # Input name
    adb_input("tap 164 1237", 2)


def login_agoda():
    time.sleep(10)
    adb_input("tap 383 1092", 3)
    adb_input("tap 376 633", 8)
    adb_input("tap 364 837", 3)
    adb_input("tap 190 255", 1)
    adb_input("tap 376 1120", 4)
    adb_input("tap 190 255", 1)

    
def login_google(username, password= "Wojiuyaobaipiao"):
    # Need to be at home screen
    adb_input("tap 103 1110", 1)
    adb_input("tap 86 90", 1)
    adb_input("tap 712 101", 8)  
    
    # ID
    adb_input("tap 144 534", 0.5)
    adb_input("text " + username, 1)
    adb_input("keyevent KEYCODE_ENTER", 3)
    
    # Password
    adb_input("text " + password, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)
    
    adb_input("tap 592 1092", 5)
    
    adb_input("tap 625 1105", 2)
    adb_input("tap 625 1100")
    
    
def login_app(apk:str):
    print("login")
    time.sleep(1)
    if f'login_{apk}' not in globals():
        return True
    flag = globals()[f'login_{apk}'](*get_account(apk))
    if flag is None:
        return True
    return flag

def exit_app_goto_menu():
    adb_input("tap 383 1235")
    adb_input("touchscreen swipe 380 820 380 220")

if __name__ == "__main__":
    login_google() 
    # exit_app_goto_menu()
    # login_youtubemusic() 
    # login_spotify()
    # login_pandora()
    # login_maps()
    # login_waze() 
    # login_mapquest()
    # login_booking()
    # login_tripadvisor()
    # login_agoda()
    
    
    
    
