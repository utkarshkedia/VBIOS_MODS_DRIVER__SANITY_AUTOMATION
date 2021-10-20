import os
import time
import paramiko
from scp import SCPClient
from datetime import datetime
import stat
import pandas as pd
import csv

#parameters/constants/paths
Mods_pen_family_path = "\\\\netapp-hq\\quickturn\\Updates\\TestDiags\\x-release\\Linux\\"
result_path = 'C:\\Users\\lab\\automation\\result\\'
text_files = 'C:\\Users\\lab\\automation\\text files\\'
automation_directory = 'C:\\Users\\lab\\automation\\'
test_system_automation_directory = '/C:/Users/lab/Automation/'
autochar_directory = "/D:/tmp/PowerScripts/Autochar/"
driver_baseAddr = "\\\\pu-cdot02-sw01\\builds_sc\\PreRel\\NV\\wddm2-x64"
driver_targetLoc = "D:\\Drivers"





with open('C:\\Users\\lab\\automation\\text files\\current_exec_system.txt','r+') as f:
    f_contents=f.readline()
    n=len(f_contents)
    hostname=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    username=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    password=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    win_hostname=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    win_username=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    win_password=f_contents[0:n-1]
with open(text_files+hostname+'directory.txt','r+') as f:
    directory=f.readline()
with open(text_files+hostname+'ROM.txt','r+') as f:
    ROM=f.readline()
with open(text_files+hostname+'Mods_family.txt','r+') as f:
    Mods_family=f.readline()
with open(text_files+hostname+'params.txt','r+') as f:
    params=f.readlines()
with open(text_files+hostname+'Tests.txt','r+') as f:
    Tests=f.readlines()
with open(text_files+hostname+'cwd.txt','r+') as f:
    cwd=f.read()
if cwd =='':
    cwd="/mnt/storage/mods"
with open(text_files+hostname+'scheduler.txt','r+') as f:
    scheduler=f.read()
with open(text_files+hostname+'apps.txt','r+') as f:
    app=f.readlines()
with open(text_files+hostname+'meas_sys.txt','r+') as f:
    meas_hostname=f.read()
with open(text_files+hostname+'latest_rom.txt','r+') as f:
    last_ROM_Path=f.readline()
frequency=[]
with open(text_files+hostname+'frequency.txt','r+') as f:
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
    f_contents=f.readline()
    n=len(f_contents)
    frequency.append(f_contents[0:n-1])
reg_values=[]
iterations=10
with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'reg_values.txt','r+') as f:
    for i in range(1,11):
        f_contents=f.readline()
        n=len(f_contents)
        reg_values.append(f_contents[0:n-1])
        if f_contents[0:n-1] == "None":
            iterations = iterations-1
with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'shmoo.txt','r+') as f:
    f_contents=f.readline()
    n=len(f_contents)
    shmoo_initial=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    shmoo_final=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    mods_shmoo_initial=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    mods_shmoo_final=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    driver_shmoo_initial=f_contents[0:n-1]
    f_contents=f.readline()
    n=len(f_contents)
    driver_shmoo_final=f_contents[0:n-1]

#Decoding regression parameter
if params[4] == "None\n":
    PowerAsParam = False
else:
    PowerAsParam = True
    Power_probable = params[6][0:len(params[6])-1]
    Power_low = 0.95*float(Power_probable)
    Power_high = 1.05*float(Power_probable)
if params[5] == "None\n":
    ModsAsParam = False
else:
    ModsAsParam =True

ROM_Paths=[]
if directory == '':


    #retriving GPU details
    with open(text_files+hostname+'gpu_name.txt','r+') as f:
        gpu_name=f.readline()
    with open(text_files+hostname+'board_name.txt','r+') as f:
        board_name=f.readline()
    with open(text_files+hostname+'mem_type.txt','r+') as f:
        mem_type=f.readline()

    
    #reading a line from text file
    f = open("C:\\Users\\lab\\automation\\text files\\info.txt",'r+')    #when installing in remote system, put the correct address
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


    #shmoo ROMs
    shmoo_list=[]
    version_list=[]
    if shmoo_initial != 'None' and shmoo_final != 'None':
        try:
            initial_ROM = line1 + '\\' + gpu_name + '\\' + shmoo_initial
            init_time = os.path.getctime(initial_ROM)
            final_ROM = line1 + '\\' + gpu_name + '\\' + shmoo_final
            end_time = os.path.getctime(final_ROM)
            dir_path= line1 + '\\' + gpu_name
            all_files=os.listdir(dir_path)
            for file in all_files:
                if file.endswith("DO_NOT_USE"):
                    pass
                else:
                    path = dir_path + '\\' + file
                    if os.path.getctime(path) >= init_time and os.path.getctime(path) <= end_time:
                        shmoo_list.append(path)
                        version_list.append(file)
        except:
            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                f.write("Cannot access the directory corresponding to the given gpu_name\n")
    else:
        try:
            dir_path= line1 + '\\' + gpu_name
            all_files=os.listdir(dir_path)
            ctime=0
            for file in all_files:
                if file.endswith("DO_NOT_USE"):
                    pass
                else:
                    path = dir_path + '\\' + file
                    if os.path.getctime(path) > ctime:
                        ctime = os.path.getctime(path)
                        latest_path = path
                        latest_file = file
        except:
            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                f.write("Cannot access the directory corresponding to the given gpu_name\n")

        shmoo_list.append(latest_path)
        version_list.append(latest_file)
        
    for latest_path in shmoo_list:    
        pen_path = latest_path + '\\' + line2 + '\\' + mem_type + '\\' + board_name + '\\' + line3

        
        #choosing the default ROM file
        if ROM == '':
            all_files = os.listdir(pen_path)
            for file in all_files:
                if file.endswith("pc0.rom"):
                    ROM = file
                    break

        ROM_Paths.append(pen_path + '\\' + ROM)
        

else:
    ROM_Paths.append(directory)

#creating the Mods list   
mods_shmoo_list = []
mods_version_list = []
if mods_shmoo_initial != "None" and mods_shmoo_final != "None":
    Mods_shmoo = True
    Mods_family_path = Mods_pen_family_path + Mods_family
    initial_mods = Mods_family_path + "\\" + mods_shmoo_initial
    init_time = os.path.getctime(initial_mods)
    final_mods = Mods_family_path + '\\' + mods_shmoo_final
    end_time = os.path.getctime(final_mods)
    try:
        all_files=os.listdir(Mods_family_path)
    except:
        with open(result_path+hostname+'Exceptions.txt','a+') as f:
            f.write("Cannot access the directory corresponding to the given mods version\n")
            
    for file in all_files:
        if file.endswith("DO_NOT_USE"):
            pass
        else:
            path = Mods_family_path + '\\' + file
            if os.path.getctime(path) >= init_time and os.path.getctime(path) <= end_time:
                mods_shmoo_list.append(path)
                mods_version_list.append(file)
    
else:
    if Tests[10] == "None\n":
        Mods_family_path = Mods_pen_family_path + Mods_family
        #finding the latest Mods path
        try:
            all_files=os.listdir(Mods_family_path)
        except:
            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                f.write("Cannot access the directory corresponding to the entered Mods_family\n")
        
        ctime=0
        for file in all_files:
            if file.endswith("DO_NOT_USE"):
                pass
            else:
                path = Mods_family_path + '\\' + file
                if os.path.getctime(path) > ctime:
                    ctime = os.path.getctime(path)
                    Mods_path = path
                    Mods_file = file
                    
        mods_shmoo_list.append(Mods_path)
        mods_version_list.append(Mods_file)
    else:
        mods_shmoo_list.append("None")
        mods_version_list.append("None")
        
#creating the drivers shmoo list
driver_shmoo_list = []
driver_version_list = []
if driver_shmoo_initial != "None" and driver_shmoo_final != "None":
    initial_driver = driver_baseAddr + "\\" + driver_shmoo_initial
    init_time = os.path.getctime(initial_driver)
    final_driver = driver_baseAddr + "\\" + driver_shmoo_final
    end_time = os.path.getctime(final_driver)
    try:
        all_files=os.listdir(driver_baseAddr)
    except:
        with open(result_path+hostname+'Exceptions.txt','a+') as f:
            f.write("Cannot access the directory corresponding to the given driver base address\n")
            
    for file in all_files:
        path = driver_baseAddr + "\\" + file
        if "develop" in file.lower():
            pass
        if "sandbag" in file.lower():
            pass
        if "nprofile" in file.lower():
            pass
        if "bullseye" in file.lower():
            pass
        else:
            if os.path.getctime(path) >= init_time and os.path.getctime(path) <= end_time:
                driver_shmoo_list.append(path)
                driver_version_list.append(file)
else:
    driver_shmoo_list.append("None")
    driver_version_list.append("None")
                

for Driver_Path in driver_shmoo_list:
    driver_shmoo_index = driver_shmoo_list.index(Driver_path)
    driver_file = driver_version_list[driver_shmoo_index]
    for ROM_Path in ROM_Paths:
        shmoo_index = ROM_Paths.index(ROM_Path)
        for Mods_path in mods_shmoo_list:
            mods_shmoo_index = mods_shmoo_list.index(Mods_path)
            Mods_file = mods_version_list[mods_shmoo_index]
            if Tests[10]=="None\n":   
                #connecting to the test system
                try:
                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=hostname,username=username,password=password,port=22)
                    
                except:
                    try:
                        ssh=paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                        ssh.exec_command("mkdir C:\\Users\\lab\\Automation")
                        time.sleep(3)
                        
                        try:
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot_to_debian.pl","/C:/Users/lab/Automation")
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot_to_debian.bat","/C:/Users/lab/Automation")
                        except:
                            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                f.write("Cannot copy files to the given test system\n")
                                
                        ssh.exec_command('WMIC /NODE:"'+win_hostname+'" process call create "C:\\Users\\lab\\Automation\\boot_to_debian.bat"')
                        time.sleep(60)
                        
                        try:
                            ssh=paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=hostname,username=username,password=password,port=22)
                        except:
                            time.sleep(60)
                            ssh=paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=hostname,username=username,password=password,port=22)
             
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot connect to the given host\n")
                            
                sftp=ssh.open_sftp()
                #checking whether the latest Mods is already present in the remote system
                if shmoo_index == 0:
                    try:
                        files=sftp.listdir(cwd)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Current working directory does not exist\n")
                    
                    n=len(files)
                    for i in range(n):
                        if files[i]==Mods_file:
                            latest_Mods_present = True
                            break
                        else:
                            latest_Mods_present = False
                else:
                    latest_Mods_present = True

                if latest_Mods_present == False:
                    #transfer of latest mods
                    try:
                        sftp.mkdir(cwd+'/'+Mods_file)
                        files=os.listdir(Mods_path)
                        for file in files:
                            path=Mods_path+'/'+file
                            with SCPClient(ssh.get_transport()) as scp:
                                    scp.put( path,cwd+'/'+Mods_file)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy Mods to the romote system\n")

                    #transfer extract.py to the test system
                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\test_system_files\\extract.py","/localhome/lab/extract.py")
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy extract.py to the romote system\n")
                            
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
                if last_ROM_Path==ROM_Path:
                    files=sftp.listdir(cwd+'/'+Mods_file)
                    n=len(files)
                    for i in range(n):
                        if files[i]==ROM:
                            latest_ROM_present = True
                            break
                        else:
                            latest_ROM_present = False
                else:
                    latest_ROM_present=False
                    with open(text_files+hostname+'latest_rom.txt','w+') as f:
                        f.write(ROM_Path)

                #transferring the latest ROM if not already present
                if latest_ROM_present == False:

                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put(ROM_Path,cwd+'/'+Mods_file)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy ROM to the remote system\n")
        
            else:
                #connecting to the test system
                try:
                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=hostname,username=username,password=password,port=22)
                except:
                    try:
                        ssh=paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                        ssh.exec_command("mkdir C:\\Users\\lab\\Automation")
                        time.sleep(3)
                        
                        try:
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot_to_debian.pl","/C:/Users/lab/Automation")
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot_to_debian.bat","/C:/Users/lab/Automation")
                        except:
                            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                f.write("Cannot copy files to the given test system\n")

                        ssh.exec_command('WMIC /NODE:"'+win_hostname+'" process call create "C:\\Users\\lab\\Automation\\boot_to_debian.bat"')
                        time.sleep(60)
                        
                        try:
                            ssh=paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=hostname,username=username,password=password,port=22)
                        except:
                            time.sleep(60)
                            ssh=paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=hostname,username=username,password=password,port=22)
                            
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot connect to the given host\n")
                        
                sftp=ssh.open_sftp()        
                ssh.exec_command("mkdir /mnt/storage/VBIOS")
                time.sleep(4)
                #checking if the required ROM is already present in the remote system in the latest mods directory
                if last_ROM_Path==ROM_Path:
                    sftp=ssh.open_sftp()
                    files=sftp.listdir("/mnt/storage/VBIOS")
                    n=len(files)
                    for i in range(n):
                        if files[i]==ROM:
                            latest_ROM_present_win = True
                            break
                        else:
                            latest_ROM_present_win = False
                else:
                    latest_ROM_present_win=False
                    with open(text_files+hostname+'latest_rom.txt','w+') as f:
                        f.write(ROM_Path)
                    

                #transferring the latest ROM if not already present
                if latest_ROM_present_win == False:

                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( ROM_Path,"/mnt/storage/VBIOS")
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy ROM to the romote system\n")
                latest_ROM_present=True
                latest_Mods_present=True
                 
            date=datetime.now()
            time_str=date.strftime("%H:%M:%S")
            date=date.strftime("%d%m%Y")

            # condition for not performing the tests
            summary=[]
            if scheduler == "True" and Tests[10] == "None\n" and latest_ROM_present and latest_Mods_present:
                summary.append("everything is upto date for " + hostname + " for VBIOS version " + version_list[shmoo_index] + " on " + date + " at " + time_str + "\n")
            elif scheduler == "True" and Tests[10] == "Test10\n" and latest_ROM_present_win:
                summary.append("everything is upto date for " + hostname + " for VBIOS version " + version_list[shmoo_index] + " on " + date + " at " + time_str + "\n")
            elif Tests[10] == "None\n":
                #Run the Tests
                if Tests[0] == "MODS init\n":
                    if shmoo_index == 0:
                        #transfer nvmt to the current executing directory in the remote system
                        try:
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "\\\\netapp-hq02\\sc_med\\nvmt\\Linux\\nvmt",cwd+'/'+Mods_file)
                        except:
                            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                f.write("Cannot copy nvmt to the romote system\n")
                               
                        #transfer of shell file to the remote system
                        try:
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put( "C:\\Users\\lab\\automation\\Tests\\Test0.sh",cwd+'/'+Mods_file)
                        except:
                            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                f.write("Cannot copy Test0.sh to the romote system\n")
                                     
                    fileObject=sftp.file(cwd+'/'+Mods_file+'/Test0.sh','r+')
                    test_commands=fileObject.readlines()
                    fileObject.close()
                    n=len(test_commands)
                    test_commands[0]="cd " + cwd + '/' + Mods_file +"\n"
                    test_commands[2]="./nvflash_eng -A" + " " + ROM
                    if params[0] == "-4\n":
                        test_commands[2]=test_commands[2] + " " + "-4"

                    if params[1]=="-5\n":
                        test_commands[2]=test_commands[2] + " " + "-5"

                    if params[2]=="-6\n":
                        test_commands[2]=test_commands[2] + " " + "-6"

                    test_commands[2]=test_commands[2] + " >> nvflash.log\n"

                    if params[3]== "-A\n":
                        test_commands[4]="./mods -A mods.js -no_gold -fundamental_reset" + "\n"
                                 
                    fileObject=sftp.file(cwd+'/'+Mods_file+'/Test0.sh','w+')
                    fileObject.writelines(test_commands)
                    fileObject.close()

                    #running the test    
                    testRunCommand="bash" + " " + cwd +'/'+Mods_file+'/Test0.sh'
                    ssh.exec_command(testRunCommand)

                    time.sleep(30)

                    if ModsAsParam == True:
                        try:
                            fileObject = sftp.file(cwd+'/'+Mods_file+"/mods.log",'r+')
                        except:
                            time.sleep(60)
                            fileObject = sftp.file(cwd+'/'+Mods_file+"/mods.log",'r+')
                        contents = fileObject.readlines()
                        notification=contents[len(contents)-1]
                        fileObject.close()
                        if notification.startswith('MODS end'):
                            error = False
                            assertion = False
                            n=len(contents)
                            for i in range(n):
                                if contents[i].startswith('Error'):
                                    if '000000000000' in contents[i]:
                                        pass
                                    else:
                                        error = True
                                    if "ModsDrvBreakPoint" in contents[i]:
                                        assertion = True
                                        if directory == '':
                                            summary.append("Test0:assertion for " + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and " +  Mods_file +"\n")
                                        else:
                                            summary.append("Test0:assertion for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                                                           
                                    with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                        f.write("Test0:for"+hostname + " for VBIOS version " + version_list[shmoo_index] + " and " +  Mods_file+"..."+contents[i]+"\n")
                            if assertion == False and error == False:
                                if directory == '':
                                    summary.append("Test0:successful initialisation for" + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and "  + Mods_file+"\n")
                                else:
                                    summary.append("Test0:successful initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                            elif assertion == False and error == True:
                                if directory == '':
                                    summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] +  " and " + Mods_file+"\n")
                                else:
                                    summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                  
                        else:
                            if directory == '':
                                summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and " + Mods_file+"\n")
                            else:
                                summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                            n=len(contents)
                            for i in range(n):
                                if contents[i].startswith('Error'):
                                    with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                        f.write("Test0:for"+hostname+ " for VBIOS version " + version_list[shmoo_index] + " and " +  Mods_file+"..."+contents[i]+"\n")

                    copyModsCommand = "sudo cp " + cwd + '/'  + Mods_file + '/mods.log ' + '/mnt/storage/automationLog/' + date + '/shmoo'+str(shmoo_index)+'Modsshmoo'+str(mods_shmoo_index)+'Test0.log'
                    ssh.exec_command("mkdir /mnt/storage/automationLog")
                    time.sleep(3)
                    ssh.exec_command("mkdir /mnt/storage/automationLog/"+date)
                    time.sleep(3)
                    ssh.exec_command(copyModsCommand)
                    time.sleep(3)
                    copyModsCommand = "sudo cp " + cwd + '/'  + Mods_file + '/nvflash.log ' + '/mnt/storage/automationLog/' + date + '/shmoo'+str(shmoo_index)+'nvflash.log'
                    ssh.exec_command(copyModsCommand)

                
                for i in range(1,10):
                    if Tests[i] == "Test" +str(i) +"\n":
                        if shmoo_index == 0:
                            #transfer of shell file to the remote system
                            try:
                                with SCPClient(ssh.get_transport()) as scp:
                                    scp.put( "C:\\Users\\lab\\automation\\Tests\\Test"+str(i)+".sh",cwd+'/'+Mods_file)
                            except:
                                with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                    f.write("Cannot copy Test"+str(i)+".sh to the romote system\n")
                    
                        fileObject=sftp.file(cwd+'/'+Mods_file+'/Test'+str(i)+'.sh','r+')
                        test_commands=fileObject.readlines()
                        fileObject.close()
                        test_commands[0]="cd " + cwd + '/' + Mods_file +"\n"
                        test_commands[1]= "cp /localhome/lab/nvutil/nvflash_eng ." + "\n"
                        test_commands[2]="./nvflash_eng -A" + " " + ROM
                        if params[0] == "-4\n":
                            test_commands[2]=test_commands[2] + " " + "-4"

                        if params[1]=="-5\n":
                            test_commands[2]=test_commands[2] + " " + "-5"

                        if params[2]=="-6\n":
                            test_commands[2]=test_commands[2] + " " + "-6"

                        test_commands[2]=test_commands[2] + " >> nvflash.log\n"
                        test_commands[3]="./nvmt rst" + "\n"
                        fileObject=sftp.file(cwd+'/'+Mods_file+'/Test'+str(i)+'.sh','w+')
                        time.sleep(3)
                        fileObject.writelines(test_commands)
                        fileObject.close()

                        #running the test
                        testRunCommand="bash" + " " + cwd +'/'+ Mods_file+'/Test'+str(i)+'.sh'
                        ssh.exec_command("mv" + " " + cwd +'/'+Mods_file+'/mods.log ' +   cwd +'/'+Mods_file+'/mods_prev.log')
                        time.sleep(3)
                        ssh.exec_command(testRunCommand)
                        
                        files=sftp.listdir(cwd +'/'+Mods_file)
                        test_executed = False
                        last_to_last_modified = 0
                        while test_executed == False:
                            time.sleep(120)
                            if "mods.log" in files:
                                utime = sftp.stat(cwd +'/'+Mods_file+"/mods.log").st_mtime
                                last_modified = datetime.fromtimestamp(utime)
                                if last_modified == last_to_last_modified:
                                    test_executed = True
                                else:
                                    last_to_last_modified = last_modified
                            else:
                                files=sftp.listdir(cwd +'/'+Mods_file)
                        if ModsAsParam == True:
                            fileObject = sftp.file(cwd+'/'+Mods_file+"/mods.log",'r+')
                            contents = fileObject.readlines()
                            notification=contents[len(contents)-1]
                            fileObject.close()
                            if notification.startswith('MODS end'):
                                error= False
                                assertion = False
                                n=len(contents)
                                for j in range(n):
                                    if contents[j].startswith('Error'):
                                        if "ModsDrvBreakPoint" in contents[i]:
                                            assertion = True
                                            if '000000000000' in contents[i]:
                                                pass
                                            else:
                                                error = True
                                            if directory == '':
                                                summary.append("Test"+str(i)+":assertion for" + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and " + Mods_file +"\n")
                                            else:
                                                summary.append("Test"+str(i)+":assertion for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                            f.write("Test"+str(i)+":for"+hostname + " for VBIOS version " + version_list[shmoo_index] + " and " +  Mods_file+"..."+contents[j]+"\n")
                                if assertion == False and error == False:
                                    if directory == '':
                                        summary.append("Test"+str(i)+":successful initialisation for" + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] +  " and " + Mods_file+"\n")
                                    else:
                                        summary.append("Test"+str(i)+":successful initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                                elif assertion == False and error == True:
                                    if directory == '':
                                        summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and " + Mods_file+"\n")
                                    else:
                                        summary.append("Test0:failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                          
                            else:
                                if directory == '':
                                    summary.append("Test"+str(i)+":failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and " + Mods_file+"\n")
                                else:
                                    summary.append("Test"+str(i)+":failed initialisation for " + hostname + " on " + date + " at " + time_str + " with " + ROM+"\n")
                                n=len(contents)
                                for j in range(n):
                                    if contents[j].startswith('Error'):
                                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                            f.write("Test"+str(i)+":for"+hostname+ " for VBIOS version " + version_list[shmoo_index] + " and " +Mods_file+"..."+contents[j]+"\n")

                        copyModsCommand = "sudo cp " + cwd + '/'  + Mods_file + '/mods.log ' + '/mnt/storage/automationLog/' + date + '/shmoo'+str(shmoo_index)+'Modsshmoo'+str(mods_shmoo_index)+'Test'+str(i)+'.log'
                        ssh.exec_command("mkdir /mnt/storage/automationLog")
                        time.sleep(3)
                        ssh.exec_command("mkdir /mnt/storage/automationLog/"+date)
                        time.sleep(3)
                        ssh.exec_command(copyModsCommand)
                        
                    
            #with open("C:\\Users\\lab\\automation\\result\\final_results.txt",'a+') as f:
                #f.writelines(summary)
                
            if  meas_hostname != '' and Tests[10]=="None\n":
                latest_ROM_present_win=latest_ROM_present

                        
            if Tests[10]=="Test10\n" and (latest_ROM_present_win == False or scheduler == False):
                try:
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.put( "C:\\Users\\lab\\automation\\Tests\\Test10.sh","/mnt/storage/VBIOS")
                except:
                    with open(result_path+hostname+'Exceptions.txt','a+') as f:
                        f.write("Cannot copy Test10.sh to the romote system\n")
                            
                fileObject=sftp.file('/mnt/storage/VBIOS/Test10.sh','r+')
                test_commands=fileObject.readlines()
                fileObject.close()
                n=len(test_commands)
                test_commands[2]="./nvflash_eng -A" + " " + ROM
                if params[0] == "-4\n":
                    test_commands[2]=test_commands[2] + " " + "-4"

                if params[1]=="-5\n":
                    test_commands[2]=test_commands[2] + " " + "-5"

                if params[2]=="-6\n":
                    test_commands[2]=test_commands[2] + " " + "-6"

                test_commands[2]=test_commands[2] + " >> nvflash.log\n"

                                 
                fileObject=sftp.file('/mnt/storage/VBIOS/Test10.sh','w+')
                fileObject.writelines(test_commands)
                fileObject.close()
                testRunCommand="bash" + " " +'/mnt/storage/VBIOS/Test10.sh'
                ssh.exec_command(testRunCommand)
                time.sleep(10)

                ssh.exec_command("mkdir /mnt/storage/automationLog")
                time.sleep(3)
                ssh.exec_command("mkdir /mnt/storage/automationLog/"+date)
                time.sleep(3)
                copyModsCommand = "sudo cp " + '/mnt/storage/VBIOS/nvflash.log ' + '/mnt/storage/automationLog/' + date + '/shmoo'+str(shmoo_index)+'nvflash.log'
                ssh.exec_command(copyModsCommand)

            if meas_hostname != '' and (latest_ROM_present_win == False or scheduler == False):
                #Resetting a variable bcz of shmoo
                IsPowerCorrect = True
                
                #switch the test system to windows and reboot the system
                
                try:
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot.sh","/localhome/lab/boot.sh")
                except:
                    with open(result_path+hostname+'Exceptions.txt','a+') as f:
                        f.write("Cannot copy boot.sh to the romote system\n")
                        
                ssh.exec_command("export TERM=xterm;bash /localhome/lab/boot.sh")
                time.sleep(40)

                #At this point all the work in debian is done
                sftp.close()
                ssh.close()
                
                #connecting to test system in windows
                try:
                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                except:
                    try:
                        time.sleep(40)
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot connect to the given test system in windows\n")

                if shmoo_index == 0 and mods_shmoo_index == 0:
                    applist=[]
                    for i in range(21):
                        if app[i] != "None\n":
                            n=len(app[i])
                            app[i]=app[i][0:n-1]
                            applist.append(app[i])
                    sftp=ssh.open_sftp()
                    fileObject=sftp.file('D:/tmp/PowerScripts/Autochar/Test_config.py','r+')
                    contents = fileObject.readlines()
                    
                    if contents[41].startswith("APP_LIST"):
                        contents[41] = "APP_LIST=" + str(applist)+"\n"
                    else:
                        for content in contents:
                            if content.startswith("APP_LIST"):
                                content = "APP_LIST=" + str(applist)+"\n"
                                
                    if contents[258].startswith("powermeasIP"):            
                        contents[258] = "powermeasIP= " +"'"+ meas_hostname+"'"+"\n"
                    else:
                        for content in contents:
                            if content.startswith("powermeasIP"):
                                content = "powermeasIP= " +"'"+ meas_hostname+"'"+"\n"
                                
                    if "None" in frequency:
                        if contents[189].startswith("if_GPCCLK_shmoo"):            
                            contents[189] = "if_GPCCLK_shmoo_req = False\n"
                        else:
                            for content in contents:
                                if content.startswith("if_GPCCLK_shmoo"):
                                    content = "if_GPCCLK_shmoo_req = False\n"

                        if contents[190].startswith("if_MCLK_shmoo"):            
                            contents[190] = "if_MCLK_shmoo_req = False\n"
                        else:
                            for content in contents:
                                if content.startswith("if_MCLK_shmoo"):
                                    content = "if_MCLK_shmoo_req = False\n"
                                    
                    else:
                        if contents[189].startswith("if_GPCCLK_shmoo"):            
                            contents[189] = "if_GPCCLK_shmoo_req = True\n"
                        else:
                            for content in contents:
                                if content.startswith("if_GPCCLK_shmoo"):
                                    content = "if_GPCCLK_shmoo_req = True\n"
                                
                        if contents[190].startswith("if_MCLK_shmoo"):            
                            contents[190] = "if_MCLK_shmoo_req = True\n"
                        else:
                            for content in contents:
                                if content.startswith("if_MCLK_shmoo"):
                                    content = "if_MCLK_shmoo_req = True\n"
                                
                    if contents[219].startswith("MSVDD_FBVDD_PEXVDD_SHMOO_RANGE"):          
                        line2=contents[219]
                        v2=219
                    else:
                        for content in contents:
                            if content.startswith("MSVDD_FBVDD_PEXVDD_SHMOO_RANGE"):
                                line2=content
                                v2=contents.index(content)
                    line2=line2.split("[")
                    values2=line2[line2.index('')+1]
                    if values2[-3] != ']':
                        values2=values2[0:len(values2)-1]
                    elif values2[-3] == ']':
                        values2=values2[0:len(values2)-2]

                    if contents[220].startswith("XBARCLK_SYSCLK_NVDCLK_HOSTCLK_SHMOO_RANGE"):    
                        line3=contents[220]
                        v3=220
                    else:
                        for content in contents:
                            if content.startswith("XBARCLK_SYSCLK_NVDCLK_HOSTCLK_SHMOO_RANGE"):
                                line3=content
                                v3=contents.index(content)           
                    line3=line3.split("[")
                    values3=line3[line3.index('')+1]
                    if values3[-3] != ']':
                        values3=values3[0:len(values3)-1]
                    elif values3[-3] == ']':
                        values3=values3[0:len(values3)-2]
                        
                    if contents[221].startswith("HUBCLK_DISPCLK_SHMOO_RANGE"):   
                        line4=contents[221]
                        v4=221
                    else:
                        for content in contents:
                            if content.startswith("HUBCLK_DISPCLK_SHMOO_RANGE"):
                                line4=content
                                v4=contents.index(content)
                    line4=line4.split("[")
                    values4=line4[line4.index('')+1]
                    if values4[-3] != ']':
                        values4=values4[0:len(values4)-1]
                    elif values4[-3] == ']':
                        values4=values4[0:len(values4)-2]

                    if contents[218].startswith("NVVDD_GPCCLK_MCLK_SHMOO_RANGE"):
                        v1=218
                    else:
                        for content in contents:
                            if content.startswith("NVVDD_GPCCLK_MCLK_SHMOO_RANGE"):
                                v1=contents.index(content)

                    if iterations != 0:
                        if contents[247].startswith("to_run_special_script"):
                            contents[247]="to_run_special_script = True\n"
                        else:
                            for content in contents:
                                if content.startswith("to_run_special_script"):
                                    content="to_run_special_script = True\n"

                        if contents[248].startswith("Special_Scripts"):
                            contents[248]="Special_Scripts = ['reg_write.py']\n"
                        else:
                            for content in contents:
                                if content.startswith("Special_Scripts"):
                                    content="Special_Scripts = ['reg_write.py']\n"
                    else:
                        if contents[247].startswith("to_run_special_script"):
                            contents[247]="to_run_special_script = False\n"
                        else:
                            for content in contents:
                                if content.startswith("to_run_special_script"):
                                    content="to_run_special_script = False\n"

                        if contents[248].startswith("Special_Scripts"):
                            contents[248]="Special_Scripts = []\n"
                        else:
                            for content in contents:
                                if content.startswith("Special_Scripts"):
                                    content="Special_Scripts = []\n"
                                
                                
                    #MSVDD_FBVDD_PEXVDD_SHMOO_RANGE=[[1.04,1.35,1.00],[1.04,1.35,1.00]]
                    #XBARCLK_SYSCLK_NVDCLK_HOSTCLK_SHMOO_RANGE=[[0.95,0.9,0.95,0.6],[0.95,0.9,0.95,0.6]]
                    #HUBCLK_DISPCLK_SHMOO_RANGE = [[0.9,0.8],[0.9,0.8]]
                    #NVVDD_GPCCLK_MCLK_SHMOO_RANGE=[[1100,1200,1200,1,6000]]
                    if "None" in frequency:
                        pass
                    else:
                        if frequency[4] == frequency[5]:
                            contents[v1] = "NVVDD_GPCCLK_MCLK_SHMOO_RANGE=[[" + frequency[0] +"," +frequency[1] + "," + frequency[2] + "," + frequency[3] + "," + frequency[4] + "]]\n"
                            contents[v2] = "MSVDD_FBVDD_PEXVDD_SHMOO_RANGE=[[" + values2 + "]\n"
                            contents[v3] = "XBARCLK_SYSCLK_NVDCLK_HOSTCLK_SHMOO_RANGE=[[" + values3 + "]\n"
                            contents[v4] = "HUBCLK_DISPCLK_SHMOO_RANGE = [[" + values4 + "]\n"
                        elif frequency[4] != frequency[5]:
                            start=int(frequency[4])
                            end = int(frequency[5])
                            step=int(frequency[6])
                            j=(end-start)/step
                            i=0
                            contents[v1] = "NVVDD_GPCCLK_MCLK_SHMOO_RANGE=[[" + frequency[0] +"," +frequency[1] + "," + frequency[2] + "," + frequency[3] + "," + frequency[4] + "]"
                            contents[v2] = "MSVDD_FBVDD_PEXVDD_SHMOO_RANGE=[[" + values2
                            contents[v3] = "XBARCLK_SYSCLK_NVDCLK_HOSTCLK_SHMOO_RANGE=[[" + values3 
                            contents[v4] = "HUBCLK_DISPCLK_SHMOO_RANGE = [[" + values4 
                            while i<j:
                                intermediate_value=str(start+(i+1)*step)
                                contents[v1] = contents[v1] + ",[" + frequency[0] +"," +frequency[1] + "," + frequency[2] + "," + frequency[3] + "," +  intermediate_value + "]"
                                contents[v2] = contents[v2] + ",[" + values2
                                contents[v3] = contents[v3] + ",[" + values3
                                contents[v4] = contents[v4] + ",[" + values4
                                i=i+1
                            contents[v1]=contents[v1]+"]\n"
                            contents[v2]=contents[v2]+"]\n"
                            contents[v3]=contents[v3]+"]\n"
                            contents[v4]=contents[v4]+"]\n"
                    
                    fileObject.close()
                    fileObject=sftp.file('D:/tmp/PowerScripts/Autochar/Test_config.py','w+')
                    fileObject.writelines(contents)
                    fileObject.close()

                    #Transfer of drivers
                    #Checking whether driver is already present
                    all_files = sftp.listdir(driver_targetLoc)
                    for file in files:
                        if file == driver_file:
                            driver_present =True
                        else:
                            try:
                                with SCPClient(ssh.get_transport()) as scp:
                                    scp.put( Driver_path + "\\IS.zip",driver_targetLoc + "\\" + driver_file)
                                with SCPClient(ssh.get_transport()) as scp:
                                    scp.put(automation_directory + "test_system_files\\zip_extracter.py", test_system_automation_directory)
                            except:
                                with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                    f.write("Cannot copy_{}_to the given measurement system\n".format(driver_file))
                                    
                    ssh.exec_command("python " + test_system_automation_directory + "zip_extracter.py --driver_file = {}".format(driver_file))           
                    

                    #close the connection with the test system
                    sftp.close()
                    ssh.close()
                    
                    #connect to the measurement system to start the server
                    try:
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=meas_hostname,username="lab",password="labuser",port=22)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot connect to the given measurement system\n")

                    ssh.exec_command("mkdir C:\\Users\\lab\\Automation")
                    time.sleep(3)
                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\measurement_system_files\\Automate_server.bat","/C:/Users/lab/Automation")
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\measurement_system_files\\Schedule_task.bat","/C:/Users/lab/Automation")
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\measurement_system_files\\Disable_task.bat","/C:/Users/lab/Automation")
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy files to the given measurement system\n")

                    ssh.exec_command("C:\\Users\\lab\\Automation\\Schedule_task.bat")
                    time.sleep(2)

                    #close the connection with the measurement system
                    ssh.close()

                    #connect back to the test system

                    try:
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot connect to the given test system in windows\n")
                        
                if iterations == 0:
                    true_iterations = 1
                else:
                    true_iterations=iterations
                
                for t in range(true_iterations):
                    if iterations != 0:
                        #checking whether tool needs to boot the test system to windows again
                        if t!=0:
                            if system_in_debian:
                                #boot to windows
                                ssh.exec_command("export TERM=xterm;bash /localhome/lab/boot.sh")
                                time.sleep(40)
                                ssh.close()

                                #connecting to test system in windows
                                try:
                                    ssh=paramiko.SSHClient()
                                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                    ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                                except:
                                    try:
                                        time.sleep(40)
                                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                        ssh.connect(hostname=win_hostname,username=win_username,password=win_password,port=22)
                                    except:
                                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                            f.write("Cannot connect to the given test system in windows\n")

                        
                        #getting the values again bcz of shmoo
                        with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'reg_values.txt','r+') as f:
                            for i in range(1,11):
                                f_contents=f.readline()
                                n=len(f_contents)
                                reg_values.append(f_contents[0:n-1])

                        #seperating register addresses and value to be written
                        reg=[]
                        reg_dict={}
                        reg_values[t]=reg_values[t].split(",")
                        for reg_value in reg_values[t]:
                            reg_value=reg_value.split(":")
                            reg.append(reg_value[0])
                            reg_dict[reg_value[0]]=reg_value[1]

                        #editing the reg write and read values and transferring the files  
                        with open(automation_directory + "test_system_files\\reg_read.py","r+") as f:
                            contents=f.readlines()

                        contents[4] = "reg_list = " + str(reg) + "\n"

                        with open(automation_directory + "test_system_files\\reg_read.py","w+") as f:
                            f.writelines(contents)

                        with open(automation_directory + "test_system_files\\reg_write.py","r+") as f:
                            contents=f.readlines()

                        contents[2] = "reg_list = " + str(reg) + "\n"
                        contents[3] = "reg_dict = " +str(reg_dict) + "\n"

                        with open(automation_directory + "test_system_files\\reg_write.py","w+") as f:
                            f.writelines(contents)
                        
                        try:
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(automation_directory + "test_system_files\\reg_write.py",autochar_directory)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(automation_directory + "test_system_files\\reg_read.py",autochar_directory)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(automation_directory + "test_system_files\\reg_writeback.py",autochar_directory)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(automation_directory + "test_system_files\\reg_read.bat",autochar_directory)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(automation_directory + "test_system_files\\reg_writeback.bat",autochar_directory)
                                
                        except:
                            with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                f.write("Cannot copy reg_write/read files to the given test system\n")
                
                    ssh.exec_command("mkdir C:\\Users\\lab\\Automation")
                    time.sleep(3)
                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\test_system_files\\run_autochar.bat","/C:/Users/lab/Automation")
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\test_system_files\\Schedule_task.bat","/C:/Users/lab/Automation")
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put( "C:\\Users\\lab\\automation\\test_system_files\\Disable_task.bat","/C:/Users/lab/Automation")
                    except:
                        with open(result_path+hostname+'Exceptions.txt','a+') as f:
                            f.write("Cannot copy files to the given test system\n")
                            
                    if iterations != 0:        
                        #to read register values
                        ssh.exec_command('WMIC /NODE:"'+win_hostname+'" process call create "D:\\tmp\\PowerScripts\\Autochar\\reg_read.bat"')
                        time.sleep(5)

                            
                    ssh.exec_command("C:\\Users\\lab\\Automation\\Schedule_task.bat")

                    #calculate wait time
                    l1=len(applist)
                    if "None" in frequency:
                        distinct_sets = 1 #incase frequency field are left empty and they are interpretd as "None"
                    else:
                        distinct_sets=int((((int(frequency[2])-int(frequency[1]))/int(frequency[3]))+1)*(((int(frequency[5])-int(frequency[4]))/int(frequency[6]))+1))
                    
                    wait_time = 840*l1*distinct_sets
                    time.sleep(wait_time)

                    #determining the os of the test system
                    try:
                        channel=ssh.invoke_shell()
                        channel.send('import sys\n')
                        channel.send('sys.plstform\n')
                        time.sleep(2)
                        channel_data=str()
                        if channel.recv_ready():
                            channel_data = channel.recv(9999)
                        else:
                            time.sleep(2)
                            channel_data = channel.recv(9999)

                        if 'Debian' in channel_data.decode(encoding='utf-8') or 'debian' in channel_data.decode(encoding='utf-8'):
                            system_in_debian =True
                            system_in_windows =False
                        elif 'Win' in channel_data.decode(encoding='utf-8') or 'win' in channel_data.decode(encoding='utf-8'):
                            system_in_debian =False
                            system_in_windows =True
                        
                    except:
                        system_in_debian =True
                        system_in_windows =False
                    
                    if iterations != 0:
                        #write back original values in the registers
                        if system_in_windows:
                            ssh.exec_command('WMIC /NODE:"'+win_hostname+'" process call create "D:\\tmp\\PowerScripts\\Autochar\\reg_writeback.bat"')
                            time.sleep(4)
                        elif system_in_debian:
                            #connect to debian
                            autochar_in_debian = True
                            try:
                                ssh=paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh.connect(hostname=hostname,username=username,password=password,port=22)
                            except:
                                with open(result_path+hostname+'Exceptions.txt','a+') as f:
                                    f.write("Cannot connect to the given test system in debian\n")
                                    
                            ssh.exec_command("python2 /mnt/storage/tmp/PowerScripts/Autochar/reg_writeback.py")
                            time.sleep(4)
                        
                        
                    
                    
                    #taking power measurements
                    sftp=ssh.open_sftp()
                    if system_in_debian:
                        pass

                    else:
                        files=sftp.listdir("D:\\tmp\\results\\power_logs")
                    file_probables=[]
                    for file in files:
                        if gpu_name in file:
                            file_probables.append(file)
                    mtime=0
                    for i in range(len(file_probables)):
                        if system_in_debian:
                            pass
                        else:
                            path="D:\\tmp\\results\\power_logs\\"+file_probables[i]
                        if sftp.stat(path).st_mtime > mtime:
                            mtime = sftp.stat(path).st_mtime
                            path1 = path+"\\Templates"
                    files=sftp.listdir(path1)
                    mtime=0
                    for file in files:    
                        path = path1 + '\\' + file
                        if sftp.stat(path).st_mtime > mtime:
                            mtime = sftp.stat(path).st_mtime
                            pen_path = path
                            pen_file = file
                    files=sftp.listdir(pen_path)
                    for file in files:
                        res_path=pen_path+"\\"+file
                    os.popen("mkdir C:\\Users\\lab\\automation\\excel_files\\"+date)
                    os.popen("mkdir C:\\Users\\lab\\automation\\excel_files\\"+date+"\\"+hostname)
                    time.sleep(2)
                    sftp.get( res_path,"C:\\Users\\lab\\automation\\excel_files\\"+date+"\\"+hostname+"\\VBIOSshmoo"+str(shmoo_index)+"MODSshmoo"+str(mods_shmoo_index)+"result"+str(t)+".xlsx")
                    df=pd.read_excel("C:\\Users\\lab\\automation\\excel_files\\"+date+"\\"+hostname+"\\VBIOSshmoo"+str(shmoo_index)+"MODSshmoo"+str(mods_shmoo_index)+"result"+str(t)+".xlsx",sheet_name = [2])
                    r1=1
                    r2=1
                    r3=1
                    length=len(df[2]['Unnamed: 2'])
                    for i in range(length):
                        field_name=str(df[2]['Unnamed: 2'].loc[i])
                        if "Voltages" in field_name:
                            r1=i
                        if "Current" in field_name:
                            r2=i
                        if "Power" in field_name:
                            r3=i
                        if field_name=="MCLK":
                            r4=i
                        if field_name == "GPCCLK":
                            r5=i
                        if field_name == "Perf":
                            r6=i

                    header=["time","vbios_shmoo_index","VBIOS_version","Mods_version","iteration","gpu_name","label","mclk","gpcclk","power","unit(V)","unit(I)","perf","total_fb_power"]
                    results=[]
                    if "None" in frequency:
                        distinct_sets =1
                    else:
                        distinct_sets=int((((int(frequency[2])-int(frequency[1]))/int(frequency[3]))+1)*(((int(frequency[5])-int(frequency[4]))/int(frequency[6]))+1))
                    for x in range(distinct_sets):
                        power_dict={}
                        count=0
                        for i in range(r1+1,r2):
                            voltage_field=str(df[2]['Unnamed: 2'].loc[i])
                            voltage_field_list=voltage_field.split("_")
                            for j in range(r2+1,r3):
                                current_field=str(df[2]['Unnamed: 2'].loc[j])
                                current_field_list=current_field.split("_")
                                if voltage_field_list[0]==current_field_list[0] and voltage_field_list[1]==current_field_list[1] and voltage_field_list[3]==current_field_list[3] :
                                    count=count+1
                                    power_dict[voltage_field]=float(df[2]['Unnamed: '+str(x+3)].loc[i])*float(df[2]['Unnamed: '+str(x+3)].loc[j])
                                    results.append([time_str,str(shmoo_index),version_list[shmoo_index],Mods_file,str(t),gpu_name,voltage_field,str(df[2]['Unnamed: '+str(x+3)].loc[r4]),str(df[2]['Unnamed: '+str(x+3)].loc[r5]),power_dict[voltage_field],str(df[2]['Unnamed: 2'].loc[r1]),str(df[2]['Unnamed: 2'].loc[r2]),str(df[2]['Unnamed: '+str(x+3)].loc[r6])])

                        keys=list(power_dict.keys())
                        l1=0
                        while l1 < len(keys):
                            total_power=power_dict[keys[l1]]+power_dict[keys[l1+1]]
                            if PowerAsParam:
                                if total_power > Power_low and total_power < Power_high:
                                    pass
                                else:
                                    IsPowerCorrect = False
                            results[l1+(x*count)].append(total_power)
                            results[l1+(x*count)+1].append(total_power)
                            l1=l1+2
                                      
                    with open("C:\\Users\\lab\\automation\\excel_files\\"+date+"\\"+hostname+"\\power_values.csv","a+") as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(header)
                        csvwriter.writerows(results)
                        
                
                if PowerAsParam:
                    if IsPowerCorrect:
                        summary.append("Successful power measurement for" + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and "  + Mods_file+"\n")
                    else:
                        summary.append("Out of bounds power measurement for" + hostname + " on " + date + " at " + time_str + " with " + gpu_name + " " + board_name + " " + ROM + " for VBIOS version " + version_list[shmoo_index] + " and "  + Mods_file+"\n")
                            
          

            #close the connections once the tests are complete for one shmoo case
            sftp.close()
            ssh.close()
                
            with open("C:\\Users\\lab\\automation\\result\\final_results.txt",'a+') as f:
                f.writelines(summary)
                
            #ssh.exec_command("C:\\Users\\lab\\Automation\\Disable_task.bat")
            #time.sleep(2)
                    
            #reboot the test system to debian
    ##        try:
    ##            with SCPClient(ssh.get_transport()) as scp:
    ##                scp.put( "C:\\Users\\lab\\automation\\test_system_files\\boot_to_debian.pl","/C:/Users/lab/Automation")
    ##            
    ##        except:
    ##            with open(result_path+hostname+'Exceptions.txt','a+') as f:
    ##                f.write("Cannot copy files to the given test system\n")
    ##
    ##        ssh.exec_command("perl C:\\Users\\lab\\Automation\\boot_to_debian.pl")
    ##        time.sleep(5)

            #connect to the measurement system and disable the scheduled task
        ##    try:
        ##        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ##        ssh.connect(hostname=meas_hostname,username="lab",password="labuser",port=22)
        ##    except:
        ##        with open(result_path+hostname+'Exceptions.txt','a+') as f:
        ##            f.write("Cannot connect to the given measurement system\n")
        ##
        ##    ssh.exec_command("C:\\Users\\lab\\Automation\\Disable_task.bat")
        ##    time.sleep(2)
            
            
