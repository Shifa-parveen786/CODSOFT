def task():
    tasks = [] 
    print("----Welcome to the To Do List App---- ")

    total_task = int(input("Enter the number of tasks you want to add: "))
    for i in range(1, total_task + 1):
        task_name = input(f"Enter the name of task {i}: ")
        tasks.append(task_name)

    print(f"Today's tasks are\n{tasks}")

    while True:
        operation = int(input("Enter your choice:\n1-Add\n2-Update\n3-Delete\n4-View\n5-Exit/Stop\n"))
        if operation == 1:
            add = input("Enter the task you want to add: ")
            tasks.append(add)
            print(f"Task '{add}' added successfully.")
        elif operation == 2:
            updated_val = input("Enter the task you want to update: ")
            if updated_val in tasks:
                up = input("Enter new task: ")
                ind = tasks.index(updated_val)
                tasks[ind] = up
                print(f"Updated task '{updated_val}' to '{up}' successfully.")
            else:
                print(f"Task '{updated_val}' not found.")
        elif operation == 3:
            del_val = input("Enter the task you want to delete: ")
            if del_val in tasks:
                ind = tasks.index(del_val)
                del tasks[ind]
                print(f"Task '{del_val}' deleted successfully.")
        elif operation == 4:
            print(f"Total tasks are:\n{tasks}")

        elif operation == 5:
            print("Closing the To Do List App. Goodbye!")
            break

        else:
            print("Invalid operation. Please try again.")

task()