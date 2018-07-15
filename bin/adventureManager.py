"""manages the adventure import, savefiles and handling """
"""import and global variable declaration"""
import json
import os

adventure_list = list()
savegame_list = list()
adventure = list()
current_id = 5
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

"""getter and setter"""
# returns the adventure_list
def get_adventure_list():
    return tuple(adventure_list)


# returns the savegame_list
def get_savegame_list():
    return tuple(savegame_list)


# give the actual chapter text
def get_chapter_text():
    return adventure['adventure']['chapter'][str(current_id)]['text'];

# give the actual chapters follower
def get_follower():
    return adventure['adventure']['chapter'][str(current_id)]['follower'];


"""others"""
def open_adventures_folder():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../adventures')
    os.startfile(filename)

