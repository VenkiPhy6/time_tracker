from datetime import datetime
import re
import pickle
import sys
import subprocess

def file_displayer():
    print("This is the current task list:")
    with open('task_list.txt', 'r') as file:
        for line in file:
            print(line, end = '')
    print("\n")

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
                subprocess.call(f"python .\stopper.py {task_id}")
                
    #Actually adding in the task
    start_time = datetime.now().strftime(fmt)
    with open('task_list.txt', 'a') as file:
        file.write(f"{task_name}\t{start_time}\t")
    with open(f'start_time_{task_name}.pickle', 'wb') as p:
        pickle.dump(start_time, p)
    
    #Printing the file just for me to see it.
    print(f"{task_name} added.")
    file_displayer()
    
task_name = sys.argv[1]
start_task(task_name)