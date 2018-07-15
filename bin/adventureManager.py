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
    del adventure_list[:]
    names = os.listdir("../adventures")
    for filename in names:
        adventure_list.append(filename[0:-5])


# load all savegames from the save directory
def load_all_savegames():
    global savegame_list
    del savegame_list[:]
    saves = os.listdir("../save")
    for filename in saves:
        savegame_list.append(filename[0:-5])


# load a given adventure
def load_adventure(adventure_name):
    global adventure
    filename = "../adventures/" + adventure_name + ".json"
    with open(filename) as myfile:
        try:
            json_buffer = json.load(myfile)
            if (len(json_buffer['adventure']['name']) >0 and len(json_buffer['adventure']['author']) > 0):
                adventure = json_buffer
            else:
                return "Sorry, the chosen file is currupt!"
        except:
            return "Sorry, file has the wrong format!"


# makes a savegame
def save_game():
    data = {}
    data['name'] = adventure['adventure']['name']
    data['filename'] = adventure['adventure']['filename']
    data['chapter'] = str(current_id)
    data['inventory'] = inventory
    global savegame
    savegame = "../save/" + data['name'] + " Chapter " + data['chapter'] + ".json"
    with open(savegame, 'w') as new_file:
            json.dump(data, new_file)


# load a given adventure
def load_savegame(file_name):
    global adventure
    global inventory
    filename = "../save/" + file_name + ".json"
    with open(filename) as myfile:
        save = json.load(myfile)
        load_adventure(save['filename'].replace(".json", ""))
        set_next_chapter(save['chapter'])
        inventory = save['inventory']



# deletes a savegame
def delete_savegame(filename):
    file_path = "../save/" + filename + ".json"
    os.remove(file_path)
    load_all_savegames()


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


# returns requirements for next chapters, if none return list is empty
def do_followers_have_requirements():
    global return_list
    return_list = list()
    story_controle = adventure['adventure']['chapter'][str(current_id)]['trigger']['story_control']
    if "|" in story_controle:
        follower_ids = get_follower()
        controle_split = story_controle.partition("|")
        if(controle_split[0] == "require"):
            requirements = controle_split[2].split(",")
            i = 0
            y = 0
            while i < len(requirements):
                insert_list = [follower_ids[y], requirements[i]]
                return_list.append(insert_list)
                i = i + 1
                y = y + 1
    return return_list


# checks if the adventure is over
def check_if_end(id):
    if(adventure['adventure']['chapter'][id]['trigger']['story_control'] == "end"):
        return True
    else:
        return False


# returns the adventure details
def get_adventure_details():
    details = {"name": adventure['adventure']['name'], "author:": adventure['adventure']['author'], "description": adventure['adventure']['description']}
    return details


# returns the chapter details
def get_chapter_details():
    details = {"name": adventure['adventure']['chapter'][str(current_id)]['name'], "text:": adventure['adventure']['chapter'][str(current_id)]['text']}
    return details


# returns the savegame details
def get_savegame_details(filename):
    global data
    data = {}
    filename = "../save/" + filename + ".json"
    with open(filename) as myfile:
        save = json.load(myfile)
        data['name'] = save['name']
        data['filename'] = save['filename']
        data['chapter'] = save['chapter']
    print data
    return data


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


# returns the inventory
def get_inventory():
    return inventory

# returns the name of a given chapter
def give_chapter_name(id):
    return adventure['adventure']['chapter'][str(id)]['name']

"""others"""
def open_adventures_folder():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../adventures')
    os.startfile(filename)

