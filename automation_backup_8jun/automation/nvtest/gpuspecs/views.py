from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import GPU,Test_System
from .serializers import GPUSerializer, Test_SystemSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import subprocess
import time
import paramiko
from scp import SCPClient
import subprocess
import os


def home(request):
    return render(request,'home.html')

 

# Create your views here.
class GPUspecs(APIView):

    def get(self,request):
        gpu_details = GPU.objects.all()
        serializer = GPUSerializer(gpu_details, many=True)
        #print(GPU.objects.get(id=id).__str__)
        return Response(serializer.data)
    def post(self,request):
        serializer = GPUSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print(serializer['name_of_the_gpu'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Test_Systems(APIView):

    def get(self,request):
        system_details = Test_System.objects.all()
        serializer = Test_SystemSerializer(system_details, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = Test_SystemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
             
         
         

def test(request):
    param=[]
    Test=[]
    app=[]
    frequency=[]
    reg_values=[]
    shmoo=[]
    id=request.POST['id']
    directory= request.POST['directory']
    hostname_ids=request.POST['hostname']
    win_hostname_ids=request.POST['win_hostname']
    Mods_family=request.POST['Mods_family']
    cwd=request.POST['cwd']
    if request.POST['shmoo_initial'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['shmoo_initial']+"\n")

    if request.POST['shmoo_final'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['shmoo_final']+"\n")

    if request.POST['mods_shmoo_initial'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['mods_shmoo_initial']+"\n")

    if request.POST['mods_shmoo_final'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['mods_shmoo_final']+"\n")

    if request.POST['driver_shmoo_initial'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['driver_shmoo_initial']+"\n")

    if request.POST['driver_shmoo_final'] == '':
        shmoo.append('None\n')
    else:
        shmoo.append(request.POST['driver_shmoo_final']+"\n")
        
    for i in range(1,22):
        if 'app'+str(i) in request.POST:
            app.append(request.POST['app'+str(i)]+'\n')
        else:
            app.append("None\n")
            
    meas_id=request.POST['meas_id']
    if request.POST['nvvdd'] != '':
        frequency.append(request.POST['nvvdd']+'\n')
    else:
        frequency.append("1100\n") #sets default nvvdd value as 1100
    if request.POST['gpcclk_from'] != '':
        frequency.append(request.POST['gpcclk_from']+'\n')
    else:
        frequency.append("None\n")
    if request.POST['gpcclk_to'] != '':
        frequency.append(request.POST['gpcclk_to']+'\n')
    else:
        frequency.append("None\n")
    if request.POST['gpcclk_step'] != '':
        frequency.append(request.POST['gpcclk_step']+'\n')
    else:
        frequency.append("None\n")
    if request.POST['mclk_from'] != '':
        frequency.append(request.POST['mclk_from']+'\n')
    else:
        frequency.append("None\n")
    if request.POST['mclk_to'] != '':
        frequency.append(request.POST['mclk_to']+'\n')
    else:
        frequency.append("None\n")
    if request.POST['mclk_step'] != '':
        frequency.append(request.POST['mclk_step']+'\n')
    else:
        frequency.append("None\n")
    
    if 'param0' in request.POST:
        param.append(request.POST['param0']+'\n')
    else:
        param.append("None\n")
    if 'param1' in request.POST:
        param.append(request.POST['param1']+'\n')
    else:
        param.append("None\n")
    if 'param2' in request.POST:
        param.append(request.POST['param2']+'\n')
    else:
        param.append("None\n")
    if 'param3' in request.POST:
        param.append(request.POST['param3']+'\n')
    else:
        param.append("None\n")
    if 'testtype1' in request.POST:
        param.append(request.POST['testtype1']+'\n')
    else:
        param.append("None\n")
    if 'testtype2' in request.POST:
        param.append(request.POST['testtype2']+'\n')
    else:
        param.append("None\n")
    if request.POST['power'] != "":
        param.append(request.POST['power']+'\n')
    else:
        param.append("None\n")
    for i in range(11):
        if 'Test'+str(i) in request.POST:
            Test.append(request.POST['Test'+str(i)]+'\n')
        else:
            Test.append("None\n")

    for i in range(1,11):
        if 'reg_write' in request.POST:
            if request.POST['iteration'+str(i)] != '':
                reg_values.append(request.POST['iteration'+str(i)]+'\n')
            else:
                reg_values.append("None\n")
        else:
            reg_values.append("None\n")
    if 'cl_shmoo' in request.POST:
        cl_shmoo = True
    else:
        cl_shmoo = False
        
    #changing the info.txt file according to the type of shmoo
    with open('C:\\Users\\lab\\automation\\text files\\info.txt','r+') as f:
        dir = f.readlines()
    if cl_shmoo == True:
        dir[0] = r'\\dc7-cdot15-scr01\gfw_backup\DVS'+'\n'
    else:
        dir[0] = r'\\builds\prerelease\BIOS'+'\n'
    with open('C:\\Users\lab\\automation\\text files\\info.txt','w+') as f:
            f.writelines(dir)

    hostname_ids=hostname_ids.split(",")
    win_hostname_ids=win_hostname_ids.split(",")
    #handling empty/duplicate 'hostname id' field
    with open('C:\\Users\\lab\\automation\\text files\\Test_System.txt','r+') as f:
            f.seek(0)
            previous_ids=f.readline()
            previous_ids=previous_ids.split(",")
            n=len(previous_ids)
            previous_ids=previous_ids[0:n-1]
    with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','r+') as f:
            f.seek(0)
            previous_win_ids=f.readline()
            previous_win_ids=previous_win_ids.split(",")
            n=len(previous_win_ids)
            previous_win_ids=previous_win_ids[0:n-1]
                
    if hostname_ids==[''] :
        hostname_ids=previous_ids
        win_hostname_ids=previous_win_ids
    else:
        if previous_ids !=['']:
            m=len(previous_ids)
            n=len(hostname_ids)
            for i in range(n):
                present = False
                for j in range(m):
                    if hostname_ids[i]==previous_ids[j]:
                        present=True
                        break
                if present:
                    pass
                else:
                    with open('C:\\Users\\lab\\automation\\text files\\Test_System.txt','a+') as f:
                        f.write(hostname_ids[i]+",")
                    if win_hostname_ids != ['']:
                        with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','a+') as f:
                            f.write(win_hostname_ids[i]+",")
                    else:
                        with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','a+') as f:
                            f.write("X,")
        else:
            with open('C:\\Users\\lab\\automation\\text files\\Test_System.txt','a+') as f:
                n=len(hostname_ids)
                for i in range(n):
                    f.write(hostname_ids[i]+",")
            with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','a+') as f:
                if win_hostname_ids != ['']:
                    n=len(win_hostname_ids)
                    for i in range(n):
                        f.write(win_hostname_ids[i]+",")
                else:
                    n=len(hostname_ids)
                    for i in range(n):
                        f.write("X,")
                    
            
       
       
    n=len(hostname_ids)
    for i in range(n):
        System_id=int(hostname_ids[i])
        if win_hostname_ids != ['']:
            win_System_id=int(win_hostname_ids[i])
        hostname=Test_System.objects.get(id=System_id).hostname
        OS=Test_System.objects.get(id=System_id).Operating_System
        username=Test_System.objects.get(id=System_id).username
        password=Test_System.objects.get(id=System_id).password
        if win_hostname_ids != ['']:
            win_hostname=Test_System.objects.get(id=win_System_id).hostname
            win_OS=Test_System.objects.get(id=win_System_id).Operating_System
            win_username=Test_System.objects.get(id=win_System_id).username
            win_password=Test_System.objects.get(id=win_System_id).password

        if meas_id == '':
            meas_hostname = ''
        else:
            meas_hostname=Test_System.objects.get(id=int(meas_id)).hostname
        text_file=hostname+'.txt'

        #clearing exceptions everytime before new execution
        with open('C:\\Users\\lab\\automation\\result\\'+hostname+'Exceptions.txt','w+') as f:
            f.write("")

        #changing the schduler value to False
        with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'scheduler.txt','w+') as f:
            f.write("False")
        if directory=='' :
            if id=='' :
                with open('C:\\Users\\lab\\automation\\text files\\' + text_file, 'r+') as f:
                    f.seek(0)
                    id=f.readline()
        
            with open('C:\\Users\\lab\\automation\\text files\\' + text_file, 'w+') as f:
                f.seek(0)
                f.write(id)
               
            gpu_name = GPU.objects.get(id=int(id)).name_of_the_gpu
            mem_type = GPU.objects.get(id=int(id)).memory_type
            board_name = GPU.objects.get(id=int(id)).board_name
            ROM = GPU.objects.get(id=int(id)).ROM_name
            #hostname=Test_System.objects.get(id=System_id).hostname

            with open('C:\\Users\\lab\\automation\\text files\\current_exec_system.txt','w+') as f:
                f.write(hostname+'\n')
                f.write(username+'\n')
                f.write(password+'\n')
                if win_hostname_ids != ['']:
                    f.write(win_hostname+'\n')
                    f.write(win_username+'\n')
                    f.write(win_password+'\n')
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'ROM.txt','w+') as f:
                f.write(ROM)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'gpu_name.txt','w+') as f:
                f.write(gpu_name)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'board_name.txt','w+') as f:
                f.write(board_name)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'mem_type.txt','w+') as f:
                f.write(mem_type)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'Mods_family.txt','w+') as f:
                f.write(Mods_family)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'Tests.txt','w+') as f:
                f.writelines(Test)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'params.txt','w+') as f:
                f.writelines(param)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'cwd.txt','w+') as f:
                f.write(cwd)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'apps.txt','w+') as f:
                f.writelines(app)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'meas_sys.txt','w+') as f:
                f.write(meas_hostname)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'directory.txt','w+') as f:
                f.write('')
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'frequency.txt','w+') as f:
                f.writelines(frequency)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'reg_values.txt','w+') as f:
                f.writelines(reg_values)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'shmoo.txt','w+') as f:
                f.writelines(shmoo)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'latest_rom.txt','w+') as f:
                f.write('')

        else:
            try:
                dir_split=directory.split("\\")
                ROM=dir_split[len(dir_split)-1]
            except:
                dir_split=directory.split("/")
                ROM=dir_split[len(dir_split)-1]
                
                                          
            with open('C:\\Users\\lab\\automation\\text files\\current_exec_system.txt','w+') as f:
                f.write(hostname+'\n')
                f.write(username+'\n')
                f.write(password+'\n')
                if win_hostname_ids != ['']:
                    f.write(win_hostname+'\n')
                    f.write(win_username+'\n')
                    f.write(win_password+'\n')
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'ROM.txt','w+') as f:
                f.write(ROM)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'directory.txt','w+') as f:
                f.write(directory)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'Mods_family.txt','w+') as f:
                f.write(Mods_family)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'Tests.txt','w+') as f:
                f.writelines(Test)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'params.txt','w+') as f:
                f.writelines(param)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'cwd.txt','w+') as f:
                f.write(cwd)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'apps.txt','w+') as f:
                f.writelines(app)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'meas_sys.txt','w+') as f:
                f.write(meas_hostname)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'frequency.txt','w+') as f:
                f.writelines(frequency)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'reg_values.txt','w+') as f:
                f.writelines(reg_values)
            with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'shmoo.txt','w+') as f:
                f.writelines(shmoo)
            
                        
        try:   
            os.popen('python C:\\Users\\lab\\automation\\nvtest\\test.py')
            time.sleep(3)
        except IOError:
            with open('C:\\Users\\lab\\automation\\result\\'+hostname+'Exceptions.txt','a+') as f:
                f.write("Cannot run shell file in test system - "+hostname )

        
    return HttpResponse("done......log files are stored in the test system in the directory: '/mnt/storage/automationLog/'....... Go to 'C:\\Users\\lab\\automation' to check the results:...............(A):'results' directory to check updates for the regular tests, exceptions file stores errors in tests or errors encountered during the tests....(B)'excel files' directory stores results in the form of excel sheets, generated after Autochar is run on the test system")


def scheduled(request):
    with open('C:\\Users\\lab\\automation\\text files\\Test_System.txt','r+') as f:
        f.seek(0)
        hostname_ids=f.readline()
        hostname_ids=hostname_ids.split(",")
        n=len(hostname_ids)
        hostname_ids=hostname_ids[0:n-1]
    with open('C:\\Users\\lab\\automation\\text files\\win_Test_System.txt','r+') as f:
        f.seek(0)
        win_hostname_ids=f.readline()
        win_hostname_ids=win_hostname_ids.split(",")
        n=len(win_hostname_ids)
        win_hostname_ids=win_hostname_ids[0:n-1]



    n=len(hostname_ids)
    for i in range(n):
        system_id=int(hostname_ids[i])
        if win_hostname_ids[i] != 'X':
            win_system_id=int(win_hostname_ids[i])
        hostname=Test_System.objects.get(id=system_id).hostname
        username=Test_System.objects.get(id=system_id).username
        password=Test_System.objects.get(id=system_id).password
        if win_hostname_ids[i] != 'X':
            win_hostname=Test_System.objects.get(id=win_system_id).hostname
            win_OS=Test_System.objects.get(id=win_system_id).Operating_System
            win_username=Test_System.objects.get(id=win_system_id).username
            win_password=Test_System.objects.get(id=win_system_id).password

        #clearing exceptions everytime before new execution
        with open('C:\\Users\\lab\\automation\\result\\'+hostname+'Exceptions.txt','w+') as f:
                f.write("")
        #changing the schduler value to True
        with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'scheduler.txt','w+') as f:
                f.write("True")

        with open('C:\\Users\\lab\\automation\\text files\\current_exec_system.txt','w+') as f:
                f.write(hostname+'\n')
                f.write(username+'\n')
                f.write(password+'\n')
                if win_hostname_ids[i] != 'X':
                    f.write(win_hostname+'\n')
                    f.write(win_username+'\n')
                    f.write(win_password+'\n')
        with open('C:\\Users\\lab\\automation\\text files\\'+hostname+'directory.txt','w+') as f:
                f.write('')
        try:   
            os.popen('python C:\\Users\\lab\\automation\\nvtest\\test.py')
            time.sleep(3)
        except IOError:
            with open('C:\\Users\\lab\\automation\\result\\'+hostname+'Exceptions.txt','a+') as f:
                f.write("Cannot run shell file in test system - "+hostname )
        
        
        
    return HttpResponse("done")

            

    
        
    
        


    
    
    
    
    
