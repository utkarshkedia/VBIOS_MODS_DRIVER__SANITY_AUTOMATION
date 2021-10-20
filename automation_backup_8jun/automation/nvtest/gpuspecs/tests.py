from django.test import TestCase
import os
import time
import paramiko
from scp import SCPClient
import tarfile
from .models import GPU,Test_System

with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\current_exec_system.txt','r+') as f:
    system_id=int(f.readline())
    
hostname=Test_System.objects.get(id=system_id).hostname
OS=Test_System.objects.get(id=system_id).Operating_System
username=Test_System.objects.get(id=system_id).username
password=Test_System.objects.get(id=system_id).password

with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'directory.txt','r+') as f:
    directory=f.readline()
with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'ROM.txt','r+') as f:
    ROM=f.readline()
with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Mods_family.txt','r+') as f:
    Mods_family=f.readline()
with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'params.txt','r+') as f:
    params=f.readlines()
with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Tests.txt','r+') as f:
    Tests=f.readlines()
with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'cwd.txt','r+') as f:
    cwd=f.read()
if cwd =='':
    cwd="/mnt/storage/mods"

if directory == '':

    with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'.txt','r+') as f:
        id=f.read()

    
    #retriving GPU details
    gpu_name = GPU.objects.get(id=int(id)).name_of_the_gpu
    mem_type = GPU.objects.get(id=int(id)).memory_type
    board_name = GPU.objects.get(id=int(id)).board_name
    ROM = GPU.objects.get(id=int(id)).ROM_name
    

    
    #reading a line from text file
    f = open("C:\\Users\\ukedia\\Desktop\\modules\\text files\\info.txt",'r+')    #when installing in remote system, put the correct address
    f_contents=f.readline()
    n=len(f_contents)
    line1=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    line2=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    line3=f_contents[0:n-1]
    f.close()

    #selects the latest folder/file from the directory
    
    try:
        dir_path= line1 + '\\' + gpu_name
        all_files=os.listdir(dir_path)
        mtime=0
        for file in all_files:
            if file.endswith("DO_NOT_USE"):
                pass
            else:
                path = dir_path + '\\' + file
                if os.path.getmtime(path) > mtime:
                    mtime = os.path.getmtime(path)
                    latest_path = path
                    latest_file = file
    except IOError:
        with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
            f.write("Check gpu_name again")

    pen_path = latest_path + '\\' + line2 + '\\' + mem_type + '\\' + board_name + '\\' + line3

    
    #choosing the ROM file
    if ROM == '':
        all_files = os.listdir(pen_path)
        for file in all_files:
            if file.endswith("pc0.rom"):
                ROM = file
                break

    ROM_Path = pen_path + '\\' + ROM
        

else:
    ROM_Path = directory

Mods_family_path = "\\\\netapp-hq\\quickturn\\Updates\\TestDiags\\x-release\\Linux\\" + Mods_family

#finding the latest Mods path
try:
    all_files=os.listdir(Mods_family_path)
except IOError:
    with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
            f.write("Mods_family does not exist")
    
mtime=0
for file in all_files:
    
    if file.endswith("DO_NOT_USE"):
        pass
    else:
        path = Mods_family_path + '\\' + file
        if os.path.getmtime(path) > mtime:
            mtime = os.path.getmtime(path)
            Mods_path = path
            Mods_file = file

#connecting to the test system
try:
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname,username=username,password=password,port=22)
except IOError:
    with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
        f.write("Cannot connect to the given host\n")

#checking whether the latest Mods is already present in the remote system
sftp=ssh.open_sftp()
files=sftp.listdir(cwd)
n=len(files)
for i in range(n):
    if files[i]==Mods_file:
        latest_Mods_present = True
        break
    else:
        latest_Mods_present = False

if latest_Mods_present == False:
    #transfer of latest mods
    try:
        sftp=ssh.open_sftp()
        sftp.mkdir(cwd+'/'+Mods_file)
        files=os.listdir(Mods_path)
        for file in files:
            path=Mods_path+'/'+file
            with SCPClient(ssh.get_transport()) as scp:
                    scp.put( path,cwd+'/'+Mods_file)
    except RuntimeError:
        with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
            f.write("Cannot copy Mods to the romote system")


    fileObject=sftp.file('/localhome/lab/extract.py','r+')
    contents = fileObject.readlines()
    contents[2] = "files=os.listdir("+"'" + cwd + "'"+")" + "\n"
    contents[5] = "    path="+"'"+cwd+"'"+ "+ '/' + file" + "\n"
    fileObject.close()
    fileObject=sftp.file('/localhome/lab/extract.py','w+')
    fileObject.writelines(contents)
    fileObject.close()

    ssh.exec_command('python3 /localhome/lab/extract.py')
    
#checking if the required ROM is already present in the remote system in the latest mods directory
files=sftp.listdir(cwd+'/'+Mods_file)
n=len(files)
for i in range(n):
    if files[i]==ROM:
        latest_ROM_present = True
        break
    else:
        latest_ROM_present = False

                
#transferring the files to the remote system and performing tests
if latest_ROM_present and latest_Mods_present:
    pass
elif latest_ROM_present:
    pass
    
    

    
        
elif latest_Mods_present:

    try:
        sftp=ssh.open_sftp()
        with SCPClient(ssh.get_transport()) as scp:
                scp.put( ROM_Path,cwd+'/'+Mods_file)
    except RuntimeError:
        with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
            f.write("Cannot copy ROM to the romote system")

    #Run the Tests
    if Tests[0] == "MODS init\n":
        testCopyCommand="sudo cp /localhome/lab/Tests/Test0 "+ cwd +'/'+ Mods_file
        ssh.exex_command(testCopyCommand)
        fileObject=sftp.file(cwd+'/'+Mods_file+'/Test0.sh','r+')
        test_commands=fileObject.readlines()
        n=len(test_commands)
        test_commands[3]="./nvflash_eng -A" + " " + ROM
        if params[0] == "-4\n":
                         test_commands[3]=test_commands[3] + " " + "-4"

        if params[1]=="-5\n":
                         test_commands[3]=test_commands[3] + " " + "-5"

        if params[2]=="-6\n":
                         test_commands[3]=test_commands[3] + " " + "-6"

        test_commands[3]=test_commands[3] + "\n"

        if params[3]== "-A\n":
                         test_commands[5]="./mods -A mods.js -no_gold -fundamental_reset" + "\n"
                     
        fileObject=sftp.file(cwd+'/'+Mods_file+'/Test0.sh','w+')
        fileObject.writelines(test_commands)
        testRunCommand="sudo bash" + " " + cwd +'/'+Mods_file+'/Test0.sh'
        ssh.exec_command(testRunCommand)

        time.sleep(30)

        fileObject = sftp.file(cwd+'/'+Mods_file+"/mods.log",'r+')
        contents = fileObject.readlines()
        notification=contents[len(contents)-1]
        fileObject.close()
        if notification.startswith('MODS end'):
            n=length(contents)
            for i in range(n):
                if contents[i].startswith('Error'):
                    with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
                        f.write("for"+hostname+"..."+contents[i]+"\n")         
            with open("C:\\Users\\ukedia\\Desktop\\modules\\text files\\final_results.txt",'a+') as f:
                f.write("successful initialisation for" + hostname)
        else:
            with open("C:\\Users\\ukedia\\Desktop\\modules\\text files\\final_results.txt",'a+') as f:
                f.write("failed initialisation for" + hostname)
            n=length(contents)
            for i in range(n):
                if contents[i].startswith('Error'):
                    with open('C:\\Users\\ukedia\\Desktop\\modules\\text files\\'+hostname+'Exceptions.txt','a+') as f:
                        f.write("for"+hostname+"..."+contents[i]+"\n")


    if Tests[1] == "Test1\n":
        testCopyCommand="sudo cp /localhome/lab/Tests/Test1.sh " + cwd + '/' + Mods_file
        ssh.exex_command(testCopyCommand)
        testRunCommand="sudo bash" + " " + cwd+ '/' +Mods_file+'/Test1.sh'
        ssh.exec_command(testRunCommand)

        time.sleep(10)

    if Tests[2] == "Test2\n":
        testCopyCommand="sudo cp /localhome/lab/Tests/Test2.sh " + cwd +"/" + Mods_file
        ssh.exex_command(testCopyCommand)
        testRunCommand="sudo bash" + " " + cwd +'/'+ Mods_file+'/Test2.sh'
        ssh.exec_command(testRunCommand)

        time.sleep(10)
        
        
            



