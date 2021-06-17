import requests
import json

url = "http://localhost:3002/posts/"
head = {"Content-Type":"application/json"}
table_head = ["id","name","age"]
head_width = [5,24,6]

def showCase():
    print("\n\n")
    print("\t"*3 + "+" + "#"*70 + "+")
    print("\t"*3 + "|" + "*"*70 + "|")
    print("\t"*3 + "|*" + " "*68 + "*|")
    print("\t"*3 + "|*" + "WELCOME TO PERSON DATABASE".center(68) + "*|")
    print("\t"*3 + "|*" + " "*68 + "*|")
    print("\t"*3 + "|" + "*"*70 + "|")
    print("\t"*3 + "+" + "#"*70 + "+")
    print("\n")

    print("\t\t0.To exit")
    print("\t\t1.To show database table")
    print("\t\t2.To create a new person and add to the table")
    print("\t\t3.To update person database table")
    print("\t\t4.To delete the details of a person")
    print("\n")

def connect(url):
    try:
        requests.head(url, headers={"Connection":"Close"})
    except requests.exceptions.RequestException:
        print("Failed to connect \n exitting !!")
        exit(1)

def ask_input():
    print("\n")
    number = input("Enter a number take action (1,2,3,4,0): ")
    print("\n")
    return number

def print_table_head():
    for item, width in zip(table_head, head_width): #print out head
        print(item.ljust(width), end = "| ")
    print("\n"+"--"*20)
    print()

def list_data():
    print_table_head()
    reply = requests.get(url)
    dictionary = reply.json()
    if len(dictionary) == 0:
        print("It's empty")
    else:
        for entry in dictionary:
            for item, width in zip(entry, head_width):
                print(str(entry[item]).ljust(width), end = "| ")
            print("\n")

def is_legit_id(id):
    reply = requests.get(url)
    reply = reply.json()
    for entry in reply:
        if  entry["id"] == id:
            return False
    return True

def ask_id():
    while True:
        id = input("Enter id(press enter to return): ")    
        if id == "":
            return 0    
        if id.isdigit():
                return int(id)
        print("Please Enter an Integer")

def ask_name():
    while True:
        name = input("Enter the name: ")
        if name.isalpha or name.isspace:
            return name
        else:
            print("PGive characters, not symbols!!")

def ask_age():
    while True:
        age = input("Enter age: ")
        if age.isdigit() and 0 < int(age) < 130:            
            return int(age)
        print("Please Enter your age !!")

def create_data():
    while 1:
        id = ask_id()
        if id == 0:
            return 0
        if is_legit_id(id):
            name = ask_name()
            age = ask_age()
            return {"id":id, "name":name, "age":age}
        print("This id has already been used !!!")

def update_data(id_num):
    try:
        if id_num == "":
            return 0
        id_num = int(id_num)
        reply = requests.get(url).json()
        for entry in reply:
            if entry["id"] == id_num:
                id = id_num
                name = ask_name()
                age = ask_age()
                return {"id":id, "name":name, "age":age}
        print("No such Id")
        return None
    except ValueError:
        print("Id should be an Integer")
        return None
    except requests.exceptions.RequestException:
        print("Id not found in the database")
        return None

def delete(id_num):
    try:
        if id_num == "":
            return 0
        id_num = int(id_num)
        reply = requests.get(url).json()
        for entry in reply:
            if entry["id"] == id_num:
                return id_num
        print("No such Id")
        return None
    except ValueError:
        print("Id should be an Integer")
        return None
    except requests.exceptions.RequestException:
        print("Id not found in the database")
        return None


def run():
    while True:
        connect(url)
        choice = ask_input()
        if choice == "1":
            list_data()

        elif choice == "2":            
            data_to_send = create_data()
            if data_to_send != 0:
                requests.post(url, headers = head, data = json.dumps(data_to_send))
                print("Creation successfull\n")
            print("Going back...")

        elif choice == "3":
            identified = False
            while not identified:
                id_num = input("Enter the id to update(press enter to return): ")
                if id_num == "":
                    print("Going back..")
                    break
                url_extended = url+id_num
                data_to_send = update_data(id_num)
                if data_to_send is not None:
                    requests.put(url_extended, headers = head, data = json.dumps(data_to_send))
                    identified = True
                    print("Updated")

        elif choice == "4":
            deleted = False
            while not deleted:
                id_str = input("Enter id to delete(press enter to return): ")
                if id_str == "":
                    print("Going back..")
                    break
                id = delete(id_str)
                if id != None:
                    url_extended = url+str(id)
                    requests.delete(url_extended, headers={"Connection":"Close"})
                    deleted = True
                    print("Deleted")

        elif choice == "0":
            print("Bye Bye")
            print("\n")
            exit()

showCase()
run()