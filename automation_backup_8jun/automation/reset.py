import os
import time

#files=os.listdir('C:\\Users\\lab\\automation\\text files')
#for file in files:
    #os.popen('del C:\\Users\\lab\\automation\\text files\\'+file)
    
#time.sleep(5)

#files=os.listdir("C:\\Users\\lab\\automation\\result")
#for file in files:
    #os.popen('del C:\\Users\\lab\\automation\\result\\'+file)

#time.sleep(5)

os.system('Echo Y|rmdir /S "C:\\Users\\lab\\automation\\text files"')
os.system('Echo Y|rmdir /S C:\\Users\\lab\\automation\\result')
time.sleep(3)

os.system('mkdir "C:\\Users\\lab\\automation\\text files"')
os.system('mkdir C:\\Users\\lab\\automation\\result')
time.sleep(3)

os.popen('copy "C:\\Users\\lab\\automation\\backup\\info.txt" "C:\\Users\\lab\\automation\\text files\\"')

with open('C:\\Users\\lab\\automation\\text files\\Test_System.txt','w+') as f:
    f.write("")
with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','w+') as f:
    f.write("")
    
