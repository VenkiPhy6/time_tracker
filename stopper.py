from datetime import datetime
import pickle
import subprocess
import sys

def file_displayer():
    print("This is the current task list:")
    with open('task_list.txt', 'r') as file:
        for line in file:
            print(line, end = '')
    print("\n")

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
    
    subprocess.call(f"del .\start_time_{task_name}.pickle", shell=True)
    
task_name = sys.argv[1]
stop_task(task_name)