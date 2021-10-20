Echo Y | SCHTASKS /CREATE /SC MONTHLY /D 15 /TN "MyTasks\Run_server" /TR "C:\Users\lab\Automation\Automate_server.bat" /ST 11:00
SCHTASKS.EXE /RUN /TN "MyTasks\Run_server"