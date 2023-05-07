import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import camara_app as cam
import screens.resources

cam.reset_temp()

class Edit_window(QDialog):
    def __init__(self):
        super(Edit_window, self).__init__()
        loadUi(r"C:\Users\user\Desktop\Python-projects\Camara_cv\screens\edit_window.ui", self)
        self.pushButton_buscarfile.clicked.connect(lambda: cam.browse_file(self))
        
        self.pushButton_load.clicked.connect(lambda: cam.load_image(self))

        self.pushButton_blurr.clicked.connect(lambda: cam.blurr_image(self, cam.img_dir[-1]))
       
        self.pushButton_gray.clicked.connect(lambda: cam.gray_scale(self, cam.img_dir[-1]))
       
        self.pushButton_invertcolors.clicked.connect(lambda: cam.invert_colors(self, cam.img_dir[-1]))
       
        self.pushButton_laplace.clicked.connect(lambda: cam.laplace(self, cam.img_dir[-1]))
     
        self.pushButton_edges.clicked.connect(lambda: cam.edges(self, cam.img_dir[-1]))
        
        self.pushButton_undo.clicked.connect(lambda: cam.undo(self))

        self.pushButton_flipV.clicked.connect(lambda: cam.flip(self, cam.img_dir[-1], 1))
       
        self.pushButton_flipH.clicked.connect(lambda: cam.flip(self, cam.img_dir[-1], 0))
       
        self.pushButton_rotate.clicked.connect(lambda: cam.rotate(self, cam.img_dir[-1], self.lineEdit_rotation.text()))
        
        self.pushButton_savepath.clicked.connect(lambda: cam.browse_dir(self))

        self.pushButton_save.clicked.connect(lambda: cam.save(self))

        self.pushButton_back.clicked.connect(lambda: cam.change_screen(-1, widget))

    

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(r"C:\Users\user\Desktop\Python-projects\Camara_cv\screens\main_window.ui",self)
        self.pushButton_loadfile.clicked.connect(lambda: cam.change_screen(1, widget))
        self.pushButton_camara.clicked.connect(lambda: cam.camara(self.lineEdit_campath.text()))
        self.pushButton_buscardir.clicked.connect(lambda: cam.browse_dir(self))
    





if __name__ == "__main__":
    app = QApplication([])
    widget = QStackedWidget()
    main_window = MainWindow()
    edit_window = Edit_window() 
    widget.addWidget(main_window)
    widget.addWidget(edit_window)
    widget.setFixedHeight(629)
    widget.setFixedWidth(961)
    widget.show()
    
    app.exec_()
