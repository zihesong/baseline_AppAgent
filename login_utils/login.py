from .util import *
import pdb

def login_youtubemusic(username, password):
    # Cancel the promotion if popped up
    adb_input("tap 714 95")
    adb_input("tap 49 79")    


def login_spotify(username, password):
    adb_input("tap 383 1072", 1)
    
    # ID
    adb_input("tap 121 307", 0.5)    
    adb_input("text " + username, 1)
    
    # Password
    adb_input("keyevent KEYCODE_TAB", 0.5)
    adb_input("text " + password, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)
    
    # Bluetooth
    adb_input("tap 389 1092", 1)

def login_pandora(username, password):
    # Tap to sign in w/ Google
    adb_input("tap 384 1097", 8)
    # adb_input("tap 634 888") 
    # adb_input("tap 686 116")
    # adb_input("tap 355 888")
    # adb_input("tap 135 454", 2)
    # adb_input("tap 300 600", 1)
    # adb_input("tap 176 653", 1)
    # adb_input("text " + password, 1)   
    # adb_input("tap 684 1132", 2)
    # adb_input("tap 684 1132", 2)
    # adb_input("tap 408 585") 


def login_maps(username, password):
    pass

def login_waze(username, password):
    # Location Permission
    # adb_pm("grant com.waze android.permission.ACCESS_COARSE_LOCATION")
    # adb_pm("grant com.waze android.permission.ACCESS_FINE_LOCATION")
    
    adb_input("tap 398 1073", 2)
    adb_input("tap 381 837", 10)
    # Login Page
    adb_input("tap 386 865", 5)
    adb_input("tap 403 1105", 2) # Continue as guest
    adb_input("tap 687 109")

def login_mapquest(username, password):
    # adb_pm("grant com.mapquest.android.ace android.permission.ACCESS_COARSE_LOCATION")
    # adb_pm("grant com.mapquest.android.ace android.permission.ACCESS_FINE_LOCATION")
    adb_input("tap 639 748", 2)
    adb_input("tap 381 837", 3)
    
def login_booking(username, password):
    # adb_pm("grant com.booking android.permission.ACCESS_COARSE_LOCATION")
    # adb_pm("grant com.booking android.permission.ACCESS_FINE_LOCATION")
    
    adb_input("tap 369 461", 2)
    adb_input("tap 376 633", 8)
    # Cancel AI assistant
    adb_input("tap 361 1120", 3)
    adb_input("tap 65 116", 2)

def login_tripadvisor(username, password):
    # adb_pm("grant com.tripadvisor.tripadvisor android.permission.ACCESS_COARSE_LOCATION")
    # adb_pm("grant com.tripadvisor.tripadvisor android.permission.ACCESS_FINE_LOCATION")
    
    adb_input("tap 397 733", 4)
    adb_input("tap 376 633", 5)
    adb_input("tap 343 843", 2)
    adb_input("tap 397 835", 2)
    # Input name
    # adb_input("tap 164 1237", 2)

def login_agoda(username, password):
    pdb.set_trace()
    adb_pm("grant com.agoda.mobile.consumer android.permission.ACCESS_COARSE_LOCATION")
    adb_pm("grant com.agoda.mobile.consumer android.permission.ACCESS_FINE_LOCATION")
    
    adb_input("tap 383 1092", 3)
    adb_input("tap 376 633", 8)
    adb_input("tap 364 837", 3)
    adb_input("tap 190 255", 1)
    adb_input("tap 376 1120", 4)
    adb_input("tap 190 255", 1)


def login_simplealarmclock(username = 0, password = 0):
    adb_input("tap 140 525", 2) 
    adb_input("tap 385 715", 2) 
    adb_input("tap 575 445", 2) 
    adb_input("tap 385 845", 2) 
    adb_input("tap 185 850", 2) 
    adb_input("tap 530 980", 2) 
    adb_input("tap 620 220", 2) 


def login_1weather(username = 0, password = 0):
    adb_input("tap 383 987", 2)
    adb_input("tap 385 837", 3)


def login_accuweather(username = 0, password = 0):
    adb_input("tap 375 1065", 2)
    adb_input("tap 375 1065", 2)
    adb_input("tap 375 1065", 2)
    adb_input("tap 385 837", 3)
    adb_input("tap 375 1065", 2)
    adb_input("tap 390 735", 2)

def login_alarmclockforme(username = 0, password = 0):
    adb_input("tap 590 908", 2)
    adb_input("tap 380 815", 2)
    adb_input("tap 410 615", 2)
    #open alarm
    adb_input("tap 72 893", 2)
    #modify first alarm
    adb_input("tap 125 322", 2)
    adb_input("tap 105 482", 2)
    #choose mon-fri
    adb_input("tap 705 265", 2)
    adb_input("tap 705 370", 2)
    adb_input("tap 705 473", 2)
    adb_input("tap 705 577", 2)
    adb_input("tap 705 682", 2)
    adb_input("tap 56 155", 2)
    #change to 8:30
    adb_input("tap 348 340", 2)
    adb_input("tap 290 694", 2)
    adb_input("tap 578 866", 2)
    adb_input("tap 588 1034", 15)
    adb_input("tap 735 46", 2)
    #modify second alarm
    adb_input("tap 90 470", 2)
    adb_input("tap 87 484", 2)
    #choose sat-sun
    adb_input("tap 705 788", 2)
    adb_input("tap 705 888", 2)
    adb_input("tap 56 155", 2)
    adb_input("tap 331 340", 2)
    adb_input("swipe 485 610 485 100", 2)
    adb_input("swipe 485 610 485 100", 2)
    adb_input("swipe 485 610 485 100", 2)
    adb_input("tap 576 867", 2)
    adb_input("tap 588 1034", 15)
    adb_input("tap 735 46", 2)
    #close alarm
    adb_input("tap 58 206", 2)

def login_aliexpress(username = 0, password = 0):
    time.sleep(10)
    adb_input("tap 366 1050", 10)
    adb_input("tap 55 100", 10)
    
    adb_input("tap 660 1030", 4)
    adb_input("tap 383 557", 4)
    adb_input("tap 123 559", 4)
    adb_input("tap 632 759", 10)
    adb_input("swipe 146 812 673 812", 4)
    adb_input("tap 387 1053", 5)
    adb_input("tap 48 93", 5)
    
    
def login_etsy(username = 0, password = 0):
    pdb.set_trace()
    adb_input("tap 378 1107", 2)
    adb_input("tap 538 1127", 2)
    adb_input("tap 390 509", 2)
    adb_input("tap 380 1095", 6)
    adb_input("swipe 485 610 485 100", 2)
    adb_input("tap 80 1118", 4)
    adb_input("tap 378 980", 4)
    adb_input("tap 390 840", 4)
    
    
def login_shein(username = 0, password = 0):
    adb_input("tap 400 888", 4)
    adb_input("tap 665 203", 4)
    adb_input("tap 693 1033", 4)
    adb_input("tap 394 870", 4)
    adb_input("tap 333 616", 4)
    #turn off ad
    adb_input("tap 692 1123", 4)
    adb_input("tap 385 1135", 4)
    adb_input("tap 80 1120", 4)

def login_theclockalarm(username = 0, password = 0):
    adb_input("tap 382 1110", 2)
    adb_input("tap 82 1110", 2)
    adb_input("tap 712 117", 2)
    #modify first alarm
    adb_input("tap 218 454", 2)
    adb_input("tap 219 623", 2)
    adb_input("tap 219 623", 2)
    adb_input("tap 722 123", 2)
    #modify second alarm
    adb_input("tap 211 624", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("swipe 392 497 392 60", 2)
    adb_input("tap 232 390", 2)
    adb_input("tap 722 123", 2)

def login_theweatherchannel(username = 0, password = 0):
    adb_input("tap 67 1039", 2)
    adb_input("tap 387 985", 2)
    adb_input("swipe 420 865 420 420", 2)
    adb_input("tap 387 1057", 2)
    adb_input("tap 385 837", 2)
    adb_input("tap 300 1095", 3)

    
def login_google(username, password):
    # Need to be at home screen
    adb_input("tap 103 1110", 3)
    adb_input("tap 86 90", 1)
    adb_input("tap 712 101", 20)  
    
    # ID
    adb_input("tap 144 534", 0.5)
    adb_input("text " + username, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)
    
    # Password
    adb_input("text " + password, 1)
    adb_input("keyevent KEYCODE_ENTER", 5)
    
    adb_input("tap 592 1092", 5)
    
    adb_input("tap 625 1105", 2)
    adb_input("tap 625 1100")
    
    exit_app_goto_menu()
    
    
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

def login_app(apk:str):
    print("login")
    time.sleep(1)
    if f'login_{apk}' not in globals():
        return True
    flag = globals()[f'login_{apk}'](*get_account(apk))
    if flag is None:
        return True
    return flag


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


