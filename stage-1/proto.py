#!/usr/bin/python3
import os
import time
import getpass
import datetime
from web3 import Web3
from colorama import init, Fore
init(autoreset=True)

def test_connection():
    w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/SMfUKiFXRNaIsjRSccFuYCq8Q3QJgks8'))
    if not w3.is_connected():
        print("Failed to connect to an Ethereum node. Please check your node URL.")
        exit()

def success(input):
    output = str(input)
    green_banner = Fore.LIGHTGREEN_EX + "[+] " + output + Fore.RESET
    print(green_banner)

def error(input):
    output = str(input)
    red_banner = Fore.RED + "[-] " + output + Fore.RESET
    print(red_banner)

def info(input):
    output = str(input)
    magenta_banner = Fore.MAGENTA + "[!] " + output + Fore.RESET
    print(magenta_banner)

def general(input):
    output = str(input)
    yellow_banner = Fore.LIGHTYELLOW_EX + output + Fore.RESET
    print(yellow_banner)

def banner():
    banner_frame="""
         ___                                    ____  
        / _ )___ ___ __  _____ _____    _____ _/ / /  
       / _  / -_) _ `/ |/ / -_) __/ |/|/ / _ `/ / /   
      /____/\__/\_,_/|___/\__/_/  |__,__/\_,_/_/_/    
       / _ \_______  / /____  _______  / /           
      / ___/ __/ _ \/ __/ _ \/ __/ _ \/ /            
     /_/  /_/  \___/\__/\___/\__/\___/_/  

    A Blockchain-based storage system for important Documents. 
    Make it much easier for you and your client to 
    traces the history of your important stuff.
        """
    yellow_banner = Fore.LIGHTYELLOW_EX + banner_frame + Fore.RESET
    print(yellow_banner)

def read_credentials(file_path):
    credentials = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 6: #Remember to change this thing everytime we add something new in the database
                username, password, id, name, content, age = [part.strip() for part in parts]
                credentials.append((username, password, id, name, content, age))
    return credentials

def get_content_for_username(credentials, input_username):
    age_list = []
    name_list = []
    content_list = []
    for username, password, id, name, content, age in credentials:
        if username == input_username:
            content_list.append(content)
            age_list.append(age)
            name_list.append(name)
    return name_list, content_list, age_list

def get_all_available_contract(credentials):
    owner_list = []
    name_list = []
    content_list = []
    for username, password, id, name, content, age in credentials:
        owner_list.append(username)
        content_list.append(content)
        name_list.append(name)
    return owner_list, name_list, content_list

def writetofile(username, password):
    id_value = input("Enter ID: ")
    name = input("Enter Name: ")
    content = input("Enter Content: ")
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    with open("credentials.txt", "a") as file:
        file.write(f"{username}|{password}|{id_value}|{name}|{content}|{current_date}\n")  

def is_duplicate(username, password):
    with open("credentials.txt", "r") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 6:
                stored_username, stored_password, id, name, content, age = parts
                if username == stored_username:
                    return True
    return False

def login(input_username, input_password, credentials):
    for username, password, id, name, content, age in credentials:
        if username == input_username and password == input_password:
            success("Login Successful")
            time.sleep(1)
            os.system('clear')
            banner()
            return True
    error("Access Denied")
    print("")
    return False

def register():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    if not is_duplicate(username, password):
        re_password = getpass.getpass("Re-enter Password: ")
        if password == re_password:
            id_value = ""
            name = ""
            content = ""
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            with open("credentials.txt", "a") as file:
                file.write(f"{username}|{password}|{id_value}|{name}|{content}|{current_date}\n")
            success("Registration successful.")
            time.sleep(1)
            os.system("clear")
            banner()
        else:
            error("Password not match!")
            exit()
    else:
        error("Data can't be processed")
        exit()

def entry_point():
    print("Welcome to Beaverwall Protocol")
    print("1. Login")
    print("2. Register")
    print("")
    print("0. Forgot Password")
    choose = int(input(">> "))
    return choose

def menu(credentials,username,password):
    print("")
    print("1. Register Document")
    print("2. Document Possession")
    print("3. View Available Contract")
    print("4. Transfer Ownership")
    print("4. Destroy")
    choose = int(input(">>"))
    if choose == 1:
        writetofile(username,password)
    elif choose == 2:
        names,assets,ages = get_content_for_username(credentials, username)
        if len(names) - 1 == 0:
            print("")
            info("You currently don't have any document stored.")
            print("")
        else:
            for name,asset,age in zip(names,assets,ages):
                if len(name) != 0:
                    print("")
                    success("Document Record")
                    print(f'Asset Name      : {name}')
                    print(f'Contract Address: {asset}')
                    print(f'Created at      : {age}')
    elif choose == 3:
        owners,names,assets = get_all_available_contract(credentials)
        if len(names) - 1 == 0:
            print("")
            info("No Contract are currently available")
            print("")
        else:
            for owner,name,asset in zip(owners,names,assets):
                if len(name) != 0:
                    print("")
                    success("Document Record")
                    print(f'Current Onwer   : {owner}')
                    print(f'Asset Name      : {name}')
                    print(f'Contract Address: {asset}')                
    else:
        error("Please input a valid option! [1-3]")

def process():
    credentials_file = 'credentials.txt'
    credentials = read_credentials(credentials_file)
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    if login(username, password, credentials):
        while True:
            credentials_file = 'credentials.txt'
            credentials = read_credentials(credentials_file)
            menu(credentials,username,password)

def main():
    # test_connection()
    banner()
    option = entry_point()
    if option == 1:
        process()
    elif option == 2:
        register()
        process()
    elif option == 0:
        error("Hubungi psikolog segera! -Kiinzu")
        exit()
    else:
        error("Invalid")
        exit()

if __name__ == "__main__":
    main()