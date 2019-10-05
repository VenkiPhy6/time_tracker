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

list_start()