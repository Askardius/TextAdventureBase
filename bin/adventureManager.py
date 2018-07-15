"""manages the adventure import, savefiles and handling """
"""import and global variable declaration"""
import json
import os

adventure_list = list()
savegame_list = list()
adventure = list()
current_id = 0
inventory = list()



"""init function, data import and data manipulation"""
# init function to initialise everything at the start
def init_logic():
    load_all_adventures()
    load_all_savegames()


# loads all adventures from the adventures directory
def load_all_adventures():
    global adventure_list
    names = os.listdir("../adventures")
    for filename in names:
        adventure_list.append(filename[0:-5])
    print adventure_list


# load all savegames from the save directory
def load_all_savegames():
    global savegame_list
    saves = os.listdir("../save")
    for filename in saves:
        savegame_list.append(filename[0:-5])
    print savegame_list


# load a given adventure
def load_adventure(adventure_name):
    global adventure
    filename = "../adventures/" + adventure_name + ".json"
    with open(filename) as myfile:
        adventure = json.load(myfile)


"""getter and setter"""
# sets the next chapter active, also triggers inventory check
def set_next_chapter(id):
    global current_id
    current_id = id
    check_inventory()


# checks the actual chapter if inventory changes happen and if makes them
def check_inventory():
    inventory_now = adventure['adventure']['chapter'][str(current_id)]['trigger']['inventory']
    if(inventory_now  != None):
        inventory_splitted = inventory_now.partition("|")
        if(inventory_splitted[0] == "add"):
            inventory.append(inventory_splitted[2])
        elif(inventory_splitted[0] == "remove"):
            for item in inventory:
                if(item == inventory_splitted[2]):
                    inventory.remove(inventory_splitted[2])
    print inventory


# checks if a required item is in the inventory
def check_inventory_for(item):
    global answer
    answer = False
    for current_item in inventory:
        if(current_item == item):
            answer = True
    return answer


# returns requirements for next chapters, if none returnes list is empty
def do_followers_have_requirements():
    global return_list
    return_list = list()
    story_controle = adventure['adventure']['chapter'][str(current_id)]['trigger']['story_control']
    if "|" in story_controle:
        controle_split = story_controle.partition("|")
        if(controle_split[0] == "require"):
            i = 2
            while i < len(controle_split):
                return_list.append(controle_split[i])
                i = i + 1
    return return_list


# returns the adventure details
def get_adventure_details():
    details = {"name": adventure['adventure']['name'], "author:": adventure['adventure']['author']}
    return details


# returns the chapter details
def get_chapter_details():
    details = {"name": adventure['adventure']['chapter'][str(current_id)]['name'], "text:": adventure['adventure']['chapter'][str(current_id)]['text']}
    return details


# returns the adventure_list
def get_adventure_list():
    return tuple(adventure_list)


# returns the savegame_list
def get_savegame_list():
    return tuple(savegame_list)


# give the actual chapter text
def get_chapter_text():
    return adventure['adventure']['chapter'][str(current_id)]['text']

# give the actual chapters follower
def get_follower():
    global follower_list
    follower_list = list()
    if(adventure['adventure']['chapter'][str(current_id)]['follower']["0"] != None):
        follower_list.append(adventure['adventure']['chapter'][str(current_id)]['follower']["0"])
    if (adventure['adventure']['chapter'][str(current_id)]['follower']["1"] != None):
        follower_list.append(adventure['adventure']['chapter'][str(current_id)]['follower']["1"])
    if (adventure['adventure']['chapter'][str(current_id)]['follower']["2"] != None):
        follower_list.append(adventure['adventure']['chapter'][str(current_id)]['follower']["2"])
    return follower_list


"""others"""
def open_adventures_folder():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../adventures')
    os.startfile(filename)

load_adventure("adventure1")
get_chapter_details()
#get_follower()
#set_next_chapter(8)
#do_followers_have_requirements()