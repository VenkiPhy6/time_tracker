from datetime import datetime
import re
import pickle
import subprocess
#import sys
#
#task_name = sys.argv[1]

def file_displayer():
    print("This is the current task list:")
    with open('task_list.txt', 'r') as file:
        for line in file:
            print(line, end = '')
    print("\n")
    
def list_start():
    with open('task_list.txt', 'w') as f:
        f.write('Task_ID\tStart\tEnd\tDuration(Mins)\n')
    
    #Printing the file just for me to see it.
    print("Welcome! List started.")
    file_displayer()
    
def start_task(task_name):
    fmt = "%Y-%m-%d %H:%M:%S"
    
    #Checking if its a "funny" situation and dealing with it
    r1 = re.compile(f"^({task_name}\t)")
    r2 = re.compile("\t$")
    with open('task_list.txt', 'r') as f:
        for line in f:
            if r1.search(line) and len(line.split("\t")) == 3: #Is there an unfinished Task_ID already? If so, then say there is already an unclosed entry. 
                existing_start_time = line.split("\t")[1]
                print(f"You have already started {task_name} at {existing_start_time}.")
                #Printing the file just for me to see it.
                file_displayer()
                return
            elif r2.search(line): #Is there an unfinished task still ongoing? Then stop it before you start the next one.
                task_id = line.split("\t")[0]
                print(f"Before I start {task_name}, I am closing {task_id} for you since you had left it unfinished.")
                stop_task(task_id)
    
    #Actually adding in the task
    start_time = datetime.now().strftime(fmt)
    with open('task_list.txt', 'a') as file:
        file.write(f"{task_name}\t{start_time}\t")
    with open(f'start_time_{task_name}.pickle', 'wb') as p:
        pickle.dump(start_time, p)
    
    #Printing the file just for me to see it.
    print(f"{task_name} added.")
    file_displayer()
    
def stop_task(task_name):
    fmt = "%Y-%m-%d %H:%M:%S"
    checker = 0
    
    #Checking if its a "funny" situation and dealing with it
    with open('task_list.txt', 'r') as f:
        for line in f:
            contents = line.split("\t")
            checker+=int(contents[0] == task_name and len(contents) == 3)
    if checker == 1: #Is this task not started at all? Or maybe it has already been started and stopped? Then just get out and tell me so.
        pass
    else:
        print(f"Couldn't stop {task_name}, since it is not found in an unfinished state.")
        file_displayer()
        return
    
    start_time = pickle.load(open(f'start_time_{task_name}.pickle', 'rb')) # Getting the start time for the task
    stop_time = datetime.now().strftime(fmt)
    duration = round((datetime.strptime(stop_time, fmt) - datetime.strptime(start_time, fmt)).total_seconds() / 60, 2)  
    
    with open('task_list.txt', 'r') as f:
        for i, line in enumerate(f):
            if i > 0: # So that I don't have to worry about the column headers line
                if(f"{task_name}\t{start_time}\t" == line):
                    with open('task_list.txt', 'a') as f2:
                        f2.write(f"{stop_time}\t{duration}\n")
                    break

    #Printing the file just for me to see it.
    print(f"{task_name} stopped.")
    file_displayer()
    
#    subprocess.call("cd C:\\Users\\venki\\Desktop\\time_tracker", shell=True)
#    subprocess.call(f"rm start_time_{task_name}.pickle", shell = True)
    subprocess.call(f"del .\start_time_{task_name}.pickle", shell=True)
    
list_start() #Opening the file afresh
start_task("Task_02") # This should start task 2
start_task("Task_02") # This should lead to stopping at the proper point 
start_task("Task_03") # This should stop task 2 and start task 3
stop_task("Task_04") # This should lead to stopping at the proper point
start_task("Task_04") #This should stop task 3 and start task 4
start_task("Task_03") # THis should stop task 4 and start task 3 again! 