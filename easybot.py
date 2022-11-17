import os
from subprocess import Popen, PIPE, call
import configparser
import shutil
import time
import cv2
#設定
config = configparser.ConfigParser()
config.read('config.ini')

#設定ADB
ADB_PATH = (config["ADB"]['adb_path'])

#設定　device
device = (config["device"]['device1'])

#SHARED_DIR = os.getenv('HOMEPATH')+'/Nox_share'
SHARED_DIR = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")+ "\\Pictures\MEmu Photo\Screenshots"
LATEST_MATCH_LOC = [0, 0]

def tap(device, loc, duration=''):
    call(ADB_PATH+' -s '+device+' shell input tap '+str(loc[0])+' '+str(loc[1])+' '+str(duration))
    return

def ChromeOpen():
    call(ADB_PATH+' -s '+device+' shell am start https://github.com/')
    print(ADB_PATH+' -s '+device+' shell am start https://github.com/')
    
def tap(device, loc, duration=''):
    os.system(ADB_PATH+' -s '+device+' shell input tap '+str(loc[0])+' '+str(loc[1])+' '+str(duration))
    return

def swipe(device, src, dst, duration=500):
    call(ADB_PATH+' -s '+device+' shell input swipe '+str(src[0])+' '+str(src[1])+' '+str(dst[0])+' '+str(dst[1])+' '+str(duration))
    return

def get_screen(device):
    path=("/storage/emulated/0/Pictures/Screenshots/")
    file_id = device.replace(':', '_')
    call(ADB_PATH+' -s '+device+' shell screencap -p '+path+'screen'+file_id+'.png')
    time.sleep(1)
    #写真移動
    shutil.move(SHARED_DIR+'\screen'+file_id+".png","%s/Screenshot/"%os.getcwd()+'\screen'+file_id+".png")
    #print("move "+SHARED_DIR+'\screen'+file_id+".png " +"%s/Screenshot"%a)
    #call("move "+SHARED_DIR+'\screen'+file_id+".png " +"%s/Screenshot"%a)
    return

#未実装
def find_img(device, temp, threshold=0.97, trim=(0, 0, 0, 0)):
    get_screen(device)
    file_id = device.replace(':', '_')
    img = cv2.imread("%s/Screenshot/"%os.getcwd()+'\screen'+file_id+".png", 1)

    if trim != (0, 0, 0, 0):
        img = img[trim[1]:trim[3], trim[0]:trim[2]]

    template = cv2.imread(temp, 1)
    (h, w, d) = template.shape

    # Apply template Matching
    try:
        matches = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)
    except:
        print('## OpenCV Error ##')
        return False

    if max_val > threshold:
        LATEST_MATCH_LOC[0] = trim[0] + int(max_loc[0] + w/2)
        LATEST_MATCH_LOC[1] = trim[1] + int(max_loc[1] + h/2)
        #print "  ", temp, "= (", LATEST_MATCH_LOC, ")"
        print (max_val, max_val)
        return True
    else:
        return False

if __name__ == '__main__':
    
    temp=(r"C:\Users\ryu\github\easy-android-automation\easy-android-automation\Screenshot\img.png")
    find_img(device, temp)
    #temp = 1
    #find_img(device, temp)
    #ChromeOpen()