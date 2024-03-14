from util import *
import pdb

# def login_tripadvisor(username, password):
#     adb_pm("grant com.tripadvisor.tripadvisor android.permission.ACCESS_COARSE_LOCATION")
#     adb_pm("grant com.tripadvisor.tripadvisor android.permission.ACCESS_FINE_LOCATION")
#     if not wait_for_activity(['RebrandOnboardingActivity', 'TASignInActivity'], 5):
#         return False

#     cur_act = get_current_activity()
#     if 'RebrandOnboardingActivity' in cur_act:
#         # close button
#         adb_input("tap 710 98", 1)

#     # input()

#     # username
#     adb_input("tap 540 660", 0.5)
#     adb_input("text " + username, 0.5)
#     adb_input("tap 540 660", 0.5)
#     # password
#     adb_input("keyevent KEYCODE_TAB", 0.5)
#     adb_input("text " + password, 0.5)
#     # login
#     adb_input("tap 730 100", 5)
#     adb_input("tap 384 962", 2)
#     adb_input("tap 570 715", 2)

#     return not check_activity('TASignInActivity')

    
    
def login_googlemusic(username = "utd.paypal.24@gmail.com", password= "Wojiuyaobaipiao"):
    pass

def login_spotify(username = "utd.paypal.24@gmail.com", password= "Wojiuyaobaipiao!"):
    pdb.set_trace()
    adb_input("tap 383 1072", 1)
    
    # ID
    adb_input("tap 121 307", 0.5)    
    adb_input("text " + username, 1)
    
    # Password
    adb_input("keyevent KEYCODE_TAB", 0.5)
    adb_input("text " + password, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)
    
    
def login_maps():
    pass

def login_waze():
    time.sleep(2)
    adb_input("tap 398 1073", 2)
    adb_input("tap 381 837", 5)
    
    # Login Page
    adb_input("tap 386 865", 5)
    adb_input("tap 403 1105", 2) # Continue as guest
    # adb_input("tap 687 109")

def login_mapquest():
    time.sleep(2)
    adb_input("tap 639 748", 2)
    adb_input("tap 381 837", 3)
    
def login_facebook(username = "utd.paypal.24@gmail.com", password="Wojiuyaobaipiao"):
    time.sleep(3)
    adb_input("tap 313 468")
    adb_input("text " + username, 1)
    adb_input("tap 95 392")
    adb_input("text " + password, 1)
    adb_input("tap 379 501")

def login_tiktok():
    time.sleep(10)
    adb_input("tap 379 743", 5)
    adb_input("tap 376 638", 10)
    adb_input("tap 205 1113", 2)
    adb_input("tap 381 1070", 10)
    adb_input("tap 383 696", 5)
    
def login_whatsapp():
    time.sleep(2)
    adb_input("tap 679 1085", 2)
    adb_input("tap 453 763", 2)
    

def login_booking():
    time.sleep(2)
    adb_input("tap 369 461", 2)
    adb_input("tap 376 633", 5)
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

def login_pandora(password = "Wojiuyaobaipiao"):
    time.sleep(5)
    adb_input("tap 384 1097", 2)
    adb_input("tap 135 454", 2)
    adb_input("tap 300 600", 1)
    adb_input("tap 176 653", 1)
    adb_input("text " + password, 1)    
    adb_input("tap 684 1132", 2)
    adb_input("tap 684 1132", 2)
    adb_input("tap 686 116")
    adb_input("tap 355 888")
    
    

    
def login_google(username = "utd.paypal.24@gmail.com", password= "Wojiuyaobaipiao"):
    # Need to be at home screen
    adb_input("tap 103 1110", 1)
    adb_input("tap 86 90", 1)

    adb_input("tap 712 101", 5)  
    
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
    # Pre-requisite: login with google account first


    # login_google()
    # exit_app_goto_menu()
    # pdb.set_trace()
    # login_googlemusic() # Google
    # login_spotify() # Spotify
    # login_maps()
    # login_waze() 
    # login_mapquest()
    login_booking()
    
    
    
    
