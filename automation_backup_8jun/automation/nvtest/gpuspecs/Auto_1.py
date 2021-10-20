import pywinauto
from pywinauto import application
from pywinauto.keyboard import send_keys
import time
from pynput.keyboard import Key,Controller
import paramiko
from scp import SCPClient
import subprocess
import os


def connect_to_PuTTY():
    app.start("C:\Program Files (x86)\PuTTY\PuTTY.exe")          # location of PuTTY in the local system
    app.PuTTYConfigBox.Edit3.type_keys('WinSCP temporary session')
    app.PuTTYConfigBox.Button5.click()
    app.PuTTYConfigBox['&Open:Button'].click()  #same as app.PuTTYConfigBox.Button.click()   
    time.sleep(4)                                
    window=app.window(title='root@power-2')
    window.wait('ready')
    while app.Dialog.exists():
        keyboard=Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        app.kill()
        connect_to_PuTTY()
    app.PuTTY.type_keys('nvidian')        #Enters password in the PuTTY dialog box      
    keyboard=Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)

#lects the latest folder/file from the directory
dir_path="\\\\builds\\prerelease\\BIOS\\GA102"
all_files=os.listdir(dir_path)
mtime=0
for file in all_files:
    path = dir_path + '\\' + file
    if os.path.getmtime(path) > mtime:
    	mtime = os.path.getmtime(path)
    	latest_pat = path
    	latest_file = file

    	
#copies VBIOS from the network to the local system
app=application.Application()
#app.start("explorer.exe Shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}")           #to open run dialog box
#time.sleep(2)
#w_handle=pywinauto.findwindows.find_windows(title="Run")[0]
#window=app.window(handle=w_handle)
#window['&Open:Edit'].type_keys('\\\\builds\prerelease\BIOS')
#window.OK.click()
#subprocess.call(['C:\\Users\\ukedia\\Desktop\\modules\\filecopy.bat - Shortcut'])  #shortcut bcz wanted to run the batch file as administrator
#time.sleep(5)

#transferring the file to the remote system
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='power-2',username='root',password='nvidian',port=22)
with SCPClient(ssh.get_transport()) as scp:
    scp.put('C:\\Users\\ukedia\\Downloads\\memory solutions\\ProjectPlanReport.pptx', '/root/')  #(source in remote system, destination in local system) /C:/Users/lab
ssh.close()
time.sleep(2)

#opens WinSCP
app.start("C:\Program Files (x86)\WinSCP\WinSCP.exe")        #Enter location of WinSCP in the local system
app.Login.LoginEdit4.type_keys('power-2')
app.Login.LoginEdit3.type_keys('root')
app.Login.LoginEdit2.type_keys('nvidian')
app.Login.LoginButton.click()
time.sleep(5)

#Connecting PuTTY through the current WinSCP session
connect_to_PuTTY()

#Flashing the GPU with the desired VBIOS
keyboard=Controller()
app.PuTTY.type_keys('nvflash_eng')
keyboard.press(Key.space)
keyboard.release(Key.space)
app.PuTTY.type_keys('-A')
keyboard.press(Key.space)
keyboard.release(Key.space)
app.PuTTY.type_keys('')               #enter VBIOS name
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(2)

#Reset
app.PuTTY.type_keys('nvmt')
keyboard.press(Key.space)
keyboard.release(Key.space)
app.PuTTY.type_keys('rst')               
keyboard.press(Key.enter)
keyboard.release(Key.enter)

#MODS init test






    
            



 
