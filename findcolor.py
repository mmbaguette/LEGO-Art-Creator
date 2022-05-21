from pynput import keyboard
import json
import pyautogui

def changeColor(color,value):
    r = open('dict.json','r')
    txt = r.read()
    r.close()
    if txt != "":
        dic = json.loads(txt)
    else:
        dic = dict()
    dic[color] = value
    toWrite = json.dumps(dic,indent=4,sort_keys=True)
    w = open('dict.json','w')
    w.write(toWrite)
    w.close()
    print('Saved',color,"as",str(value) + '\n')

def on_press(key):
    try:
        if key.char == "G":
            coords = tuple(pyautogui.position())
            img = pyautogui.screenshot().convert('RGB')
            #x,y = coords
            value = img.getpixel(coords)
            color = input('Enter color: ')
            changeColor(color,value)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()