"""controls the game logic and data manipulation"""
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
    names = os.listdir("adventures")
    for filename in names:
        adventure_list.append(filename[0:-5])
    print adventure_list


# load all savegames from the save directory
def load_all_savegames():
    global savegame_list
    saves = os.listdir("save")
    for filename in saves:
        savegame_list.append(filename[0:-5])
    print savegame_list


# load a given adventure
def load_adventure(adventure_name):
    global adventure
    filename = "adventures/" + adventure_name + ".json"
    with open(filename) as myfile:
        adventure = json.load(myfile)
    print adventure['adventure']['chapter']['0']['text'];



"""getter and setter"""
# returns the adventure_list
def get_adventure_list():
    return adventure_list


# returns the savegame_list
def get_savegame_list():
    return savegame_list


# give the actual chapter text
def get_chapter_text():
    return adventure['adventure']['chapter'][current_id]['text'];

# give the actual chapters follower
def get_chapter_text():
    return adventure['adventure']['chapter'][current_id]['follower'];