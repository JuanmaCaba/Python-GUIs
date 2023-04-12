import csv
import random
from PyQt5.QtWidgets import *



fish_bag = []
player_list = []
fishes = []
cañas = []
#We load de data base from the csv files.
def cargar():
#Fish bag
    with open(r"data_base\fish_bag.csv", newline="",encoding="utf-8" ) as fish_bag_file:
        reader = csv.DictReader(fish_bag_file)
        for fish in reader:                              
            fish_bag.append(fish)


    #Players list
    with open (r"data_base\player_data.csv", newline="",encoding="utf-8" ) as player_data_file:
        reader = csv.DictReader(player_data_file)
        for player in reader:
            player_list.append(player)



    #Fishes info
    with open (r"data_base\fish_info.csv", newline="",encoding="utf-8" ) as fish_info_file:
        reader = csv.DictReader(fish_info_file)
        for fish in reader:
            fishes.append(fish)

    #Rods list
    with open(r"data_base\rod_data.csv", newline="",encoding="utf-8" ) as rod_data_file:
        reader = csv.DictReader(rod_data_file)
        for caña in reader:                              
            cañas.append(caña)

    
cargar()    

playing_player = {}#This variable will hold our playing player data while using it.




#////New Player////
#Creates a new player checking the player_list data base
def new_player(name, widget):
    if name != "":
        playing_player.update({"name":name, "caña":"Caña Básica", "oro":0})
        if player_list:
            for jugador in player_list: 
                if name == jugador["name"]:
                    show_stuff("Ya existe un jugador con ese nombre")
                    playing_player.clear()  
                    break  
                elif jugador == player_list[-1]:
                    change_screen(1, widget) 
                    break           
        else:       
            change_screen(1, widget)
    else:
        show_stuff("El nombre debe contener al menos 1 carácter")
   
        
        

#Selects player checking the player list data base

def sel_playing_player(name, widget):
    if name != "":
        playing_player.clear()
        for player in player_list:
            if name == player["name"]:
                playing_player.update(player)
                change_screen(1, widget)
                break
        if not playing_player:
            show_stuff("No existe un jugador con ese nombre") 
    else:
        show_stuff("El nombre debe contener al menos 1 carácter")
   
#Fishing functions

#2 random functions that receives the playing_player rod bonus and calculates a random value to define the fish quality and rarity.   
def quality(caña):
    prob = random.randint(1,1000)+int(caña)
    if prob <= 600:
        return "Normal"
    if prob > 600 and prob <= 870:
        return "Buena"
    if prob > 870 and prob <= 980:
        return "Notable"
    if prob > 980:
        return "Excelente"


def rarity(caña):
    prob = random.randint(1,1000)+int(caña)
    if prob <= 600:
        return "Común"
    if prob > 600 and prob <= 899:
        return "Raro"
    if prob > 899 and prob <= 999:
        return "Épico"
    if prob > 999:
        return "Legendario"


#It searches through the fish_info data base and copy all the fishes that match the location selected by the player and the rarity created almost randomly. Returns all the matches in a list called fish_pool
def set_fish_pool(location):
    fish_pool = []
    for caña in cañas:
        if caña["name"] == playing_player["caña"]:
                rareza = rarity(caña["bonus"])    
    for fish in fishes:
        if fish["location"] == location and fish["rarity"] == rareza:
            fish_pool.append(fish)
    return fish_pool


#In this function, a fish will be pulled out from the fish_pool and it will append 2 new characteristics: Quality and player_name. 
def fishing(location):
    chance = random.randint(1,10)
    if chance <= 7:
        fish_pool = set_fish_pool(location)
        fish = random.choice(fish_pool)
        for caña in cañas:
            if caña["name"] == playing_player["caña"]:
                calidad = quality(caña["bonus"])
        fish["quality"] = calidad
        fish["player name"] = playing_player["name"]
        if fish["quality"] == "Buena":
            fish["price"] = round(int(fish["price"]) * 1.25)
        elif fish["quality"] == "Notable":
            fish["price"] = round(int(fish["price"]) * 1.5)
        elif fish["quality"] == "Excelente":
            fish["price"] = round(int(fish["price"]) * 2)
        fish_bag.append(fish)
        show_stuff("Genial!! Has pescado:\n{} ({}) de calidad {}".format(fish["name"], fish["rarity"], fish["quality"]))
    else:
        show_stuff("Lástima! No has pescado nada :(")



#This function will execute the sell operation of a certaing fish selected by the player
def sell_operations(playing_player, x):
    oro_player = int(playing_player["oro"])
    oro_player += int((fish_bag[x])["price"])
    playing_player["oro"] = oro_player
    fish_bag.pop(x)
    
    
      
#Buying a new rod. Checking the rods data base and the amount of gold the player needs to buy the next rod. (This function is a little messy)
def improve_rod():
    try:
        for index,caña in enumerate(cañas):   
            if caña["name"] == playing_player["caña"]:
                if int(playing_player["oro"]) >= int((cañas[index+1])["price"]): 
                    new_rod = (cañas[index+1])
                    playing_player["caña"] = new_rod["name"]
                    show_stuff("Acabas de obtener la {} por {} de oro".format(new_rod["name"], new_rod["price"]))
                    playing_player["oro"] = str(int(playing_player["oro"]) - int(new_rod["price"]))
                    break
                else:
                    show_stuff("Lo siento no tienes suficiente dinero.\nNecesitas al menos {} de oro más".format(int((cañas[index+1])["price"])-int(playing_player["oro"])))
                    break
    except IndexError:
        show_stuff("Ya tienes la mejor caña del juego!")
    print(playing_player)

    
#This function will refresh the player list variable and overwrite all the data files (csv) with the refreshed player and fish_bag information.
def guardar():
    if player_list:
        for player in player_list:
            if player["name"] == playing_player["name"]:
                index = player_list.index(player)
                player_list[index] = playing_player
            elif player == player_list[-1]:
                player_list.append(playing_player)
    else:
        player_list.append(playing_player)
    
    with open(r"data_base\fish_bag.csv", "w", newline="",encoding="utf-8") as fish_bag_file:
        keys = ["name","price","location","description","rarity","quality","player name"]
        writer = csv.DictWriter(fish_bag_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(fish_bag)
    
    with open(r"data_base\player_data.csv", "w", newline="",encoding="utf-8") as player_list_file:
        keys = ["name","caña","oro"]
        writer = csv.DictWriter(player_list_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(player_list)
    
    fish_bag.clear()
    player_list.clear()
    fishes.clear()

    cargar()

#This function will be called everytime a message box needs to appear.
def show_stuff(msg):
    message = QMessageBox()
    message.setText(str(msg))
    message.show()
    message.exec_()

#Change screen
def change_screen(page, widget):
    widget.setCurrentIndex(widget.currentIndex() + page)


#In this functions a checkbox will be add in the third screen for every fish in fish bag as long as that fish in particular belongs to the current player.
indexes = [] 
checkboxes = []
def show_fishbag(self):
    checkboxes.clear()
    indexes.clear()
    for i in reversed(range(self.verticalLayout_2.count())): 
        self.verticalLayout_2.itemAt(i).widget().setParent(None)
    for fish in fish_bag:
        if playing_player["name"] == fish["player name"]:
            index = fish_bag.index(fish)
            indexes.append(index)
            object = QCheckBox()
            text = "Nombre: {}. Precio: {} oro. Bioma: {}. Rareza: {}. Calidad: {}.".format(fish["name"], fish["price"], fish["location"], fish["rarity"], fish["quality"] )
            object.setText(text)
            size_policy = object.sizePolicy()
            size_policy.setVerticalPolicy(QSizePolicy.Fixed)
            size_policy.setHorizontalPolicy(QSizePolicy.Minimum)
            object.setSizePolicy(size_policy)
            object.setMinimumHeight(100)
            object.setToolTip("Descripción: {}".format(fish["description"]))
            self.verticalLayout_2.addWidget(object)
            checkboxes.append(object)
    
# Function to mark all the checkboxes (setEnabled(True))   
def all_sell(self):
    for i in range(self.verticalLayout_2.count(), 0, -1):
        checkboxes[i-1].setChecked(True)

#Selling function  
def sell(self): 
    for i in range(self.verticalLayout_2.count(), 0, -1):
            if checkboxes[i-1].isChecked():
                sell_operations(playing_player, indexes[i-1])
    show_stuff("Se han vendido correctamente los peces seleccionados.")
    



