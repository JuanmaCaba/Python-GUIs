from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
import fishing_game_dev as game
from pygame import mixer
import sys
sys.path.append(r'screens')
import screens.recursos


########### Using Pygame for the background music on loop
mixer.init()
mixer.music.load(r"the-beat-of-nature-122841.mp3")
mixer.music.set_volume(0.25)
mixer.music.play(-1)

#A little improvised function to mute and unmute the music 
music_count = []
def start_stop_music(self):
    music_count.append("")
    if len(music_count)%2 == 0:
        mixer.music.set_volume(0.25)
        self.pushButton_sound.setIcon(QtGui.QIcon(r"screens\Daco_4550678.png"))
    else:
        mixer.music.set_volume(0)
        self.pushButton_sound.setIcon(QtGui.QIcon(r"screens\Daco_5639330.png"))


#First window (player selection)
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(r"screens\main.ui", self)
        
        self.pushButton_new_player.clicked.connect(lambda: game.new_player(self.player_name.text(), widget))
        
        self.pushButton_sel_player.clicked.connect(lambda: game.sel_playing_player(self.player_name.text(), widget))
        
        self.pushButton_sound.clicked.connect(lambda: start_stop_music(self))
  
#Second window (actions)
class Actions(QDialog):
    button_clicked = pyqtSignal()
    def __init__(self, ):
        super().__init__()
        loadUi(r"screens\window_actions.ui", self)

        self.pushButton_sound.clicked.connect(lambda: start_stop_music(self))
        
        self.pushButton_fishbag.clicked.connect(self.emit_button_clicked_signal)
        self.pushButton_fishbag.clicked.connect(lambda: game.change_screen(1,widget))
        
    
        self.pushButton_guardar.clicked.connect(lambda: game.guardar())
        self.pushButton_guardar.clicked.connect(lambda: set_enabled(self))

        self.pushButton_menu.setEnabled(False)
        self.pushButton_menu.clicked.connect(lambda: game.change_screen(-1, widget))
        self.pushButton_menu.clicked.connect(lambda: set_disabled(self))
        
        self.pushButton_pescar.setEnabled(False)
        self.pushButton_pescar.clicked.connect(lambda: game.fishing(str(set_location(self))))

        self.pushButton_stats.clicked.connect(lambda: game.show_stuff("Nombre: {}\nCaña: {}\nOro: {}".format(game.playing_player["name"], game.playing_player["caña"], game.playing_player["oro"])))

        self.radioButton_rio.clicked.connect(lambda: set_location(self))
        self.radioButton_lago.clicked.connect(lambda: set_location(self))
        self.radioButton_oceano.clicked.connect(lambda: set_location(self))

        self.pushButton_improverod.clicked.connect(lambda: game.improve_rod())
        self.pushButton_improverod.setToolTip("Cada caña mejorará tus probabilidades de conseguir peces más raros y de mejor calidad!")

        
    def emit_button_clicked_signal(self):
        self.button_clicked.emit()
    
def set_enabled(self):
    self.pushButton_menu.setEnabled(True)
def set_disabled(self):
    self.pushButton_menu.setEnabled(False)
        
def set_location(self):
    if self.radioButton_rio.isChecked():
        self.pushButton_pescar.setEnabled(True)
        location = "Río"
    if self.radioButton_lago.isChecked():
        self.pushButton_pescar.setEnabled(True)
        location = "Lago"
    if self.radioButton_oceano.isChecked():
        self.pushButton_pescar.setEnabled(True)
        location = "Océano"
    return location


#Third window (Selling menu)
class Sell(QDialog):
    def __init__(self, actions_dialog):
        super().__init__()
        loadUi(r"screens\sell.ui", self)    
        self.actions_dialog = actions_dialog
        self.actions_dialog.button_clicked.connect(lambda: game.show_fishbag(self))

        self.pushButton_sound.clicked.connect(lambda: start_stop_music(self))

        self.pushButton_back.clicked.connect(lambda: game.change_screen(-1, widget))
        
        self.pushButton_vender.clicked.connect(lambda: game.sell(self))
        self.pushButton_vender.clicked.connect(lambda: game.show_fishbag(self))

        self.pushButton_sel_all.clicked.connect(lambda: game.all_sell(self))
     
    

if __name__ == "__main__":
    app = QApplication([])
    widget = QStackedWidget()
    main_window = MainWindow()
    actions_window = Actions()
    sell_window = Sell(actions_window) 
    widget.addWidget(main_window)
    widget.addWidget(actions_window)
    widget.addWidget(sell_window)
    widget.setFixedHeight(670)
    widget.setFixedWidth(708)
    widget.show()
    
    app.exec_()



