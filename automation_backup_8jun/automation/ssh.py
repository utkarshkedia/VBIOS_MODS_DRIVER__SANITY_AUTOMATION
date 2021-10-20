import datetime
from datetime import datetime
import paramiko
from scp import SCPClient
import time
from threading import *

#def connect():
    #ssh=paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname='power-2',username='lab',password='labuser',port=22)
    #ssh.exec_command('WMIC /NODE:"10.41.199.147" process call create "C:\\Users\\lab\\Automation\\Automate_server.bat"')
    #ssh.exec_command("C:\\Users\\lab\\Automation\\Schedule_task.bat")
    
#X=Thread(target = connect)
#X.start()
#start = time.perf_counter()
#print("done")
#X.join()
#end = time.perf_counter()
#print("done")
#print(end-start)
##    time.sleep(5)
##    print(stdin.readlines())
##    print(stderr.read())
#sftp=ssh.open_sftp()
#with SCPClient(ssh.get_transport()) as scp:
    #scp.put('C:\\Users\\ukedia\\Documents\\Custom Office Templates\\Corp_PPT_Template_LIGHT_WEBEX_September2020.pptx', '/C:/Users/lab/Automation')
#utime = sftp.stat("/mnt/storage/mods/400.307.6/mods.log").st_mtime
#last_modified = datetime.fromtimestamp(utime)
#command='SCHTASKS.EXE /RUN /TN "automation"'
#stdin,sdtout,stderr=ssh.exec_command("D:\\Win_OS_change.bat")
##    channel=ssh.invoke_shell()
##    channel.send('import sys\n')
##    channel.send('sys.plstform\n')
##    time.sleep(2)
##    channel_data=str()
##    if channel.recv_ready():
##        channel_data = channel.recv(9999)
##    else:
##        time.sleep(2)
##        channel_data = channel.recv(9999)
##
##    if 'Debian' in channel_data.decode(encoding='utf-8') or 'debian' in channel_data.decode(encoding='utf-8'):
##        system_in_debian =True
##        system_in_windows =False
##    else if 'Win' in channel_data.decode(encoding='utf-8') or 'win' in channel_data.decode(encoding='utf-8'):
##        system_in_debian =False
##        system_in_windows =True
##    else:
##        with open('','w+') as f:
##            f.write("cannot determine the os of the test system")
##    

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='power-2',username='lab',password='labuser',port=22)
#stdin, stdout, stderr = ssh.exec_command('WMIC /NODE:"power-2" process call create "C:\\Users\\lab\\Automation\\run_autochar.bat"')
#ssh.exec_command("C:\\Users\\lab\\Automation\\Schedule_task.bat")
#exit_status = stdout.channel.recv_exit_status()
stdin, stdout, stderr = ssh.exec_command("python d:\\tmp\\PowerScripts\\Autochar\\Run_Automation1.py")
#stdin, stdout, stderr = ssh.exec_command('WMIC /NODE:"power-2" process call create "process"')
stdin, stdout, stderr = ssh.exec_command("wmic process")
exit_status = False
while exit_status != True:
    exit_status = stdout.channel.exit_status_ready()
#print(exit_status)



    

