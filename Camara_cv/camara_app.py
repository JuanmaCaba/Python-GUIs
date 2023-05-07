import cv2 as cv
import numpy as np
import os
import shutil
from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


#Function to activate the camera window. It will check the path given and if its valid it will execute the rest of the function
def camara(path):
    if path:
        show_stuff("Pulse la letra (p) para tomar una foto y la letra (d) para salir de la cámara")
        vid = cv.VideoCapture(0)

        while True:
            isTrue,frame = vid.read()
            cv.imshow("camara", frame)

            # Obtain the pressed key
            key = cv.waitKeyEx(1)
            
            if key in [ord("d"), ord("D")]:
                break
            elif key in [ord("p"), ord("P")]: #Once P or p is pressed it will take that especific frame and save it in the path specified by the user. It will show a new frame with the text: "Foto tomada!" for one sec so the user know the picture was taken correctly.
                numero = str(randint(0,10000000000000))
                foto_path = os.path.join(path, (numero+".png"))
                cv.imwrite(foto_path, frame)
                new_frame = cv.putText(frame, text="Foto tomada!", org=(30,30), fontFace=cv.FONT_HERSHEY_COMPLEX, fontScale=0.9, color=(0,255,0), thickness=2)
                cv.imshow("camara", new_frame)
                cv.waitKey(1000)

        vid.release()
        cv.destroyAllWindows()
    else:
        show_stuff("Por favor, seleccione una dirección para guardar sus fotos")


#UI Functions------------------------------------------------------------------------------------------------------------------------------

#This func will be called any time the app opens to empty the temp directory.
def reset_temp():
    for file in os.listdir(r"C:\Users\user\Desktop\cv_photos\temp"):
        os.remove(os.path.join(r"C:\Users\user\Desktop\cv_photos\temp", file))


img_dir = [] #In this list the script will be saving the original image and all the temp directory's images paths.

#Func to search for a directory to save user's pictures. First it will try to call the lineEdit of the Edit_window, if it doesn't find it an AtributeError will rise and it will call the lineEdito of the MainWindow.
def browse_dir(self):
    fname = QFileDialog.getExistingDirectory(self, "Save File", r"C:\Users\user\Desktop")
    try:
        self.lineEdit_savepath.setText(fname)
    except AttributeError:
        self.lineEdit_campath.setText(fname)

#Same func but to look for a specific file path
def browse_file(self):
    fname = QFileDialog.getOpenFileName(self, "Open File", r"C:\Users\user\Desktop", "PNG files and JPG files (*.png *.jpg)")
    self.line_file.setText(fname[0])#fname(example) = ('C:/Users/user/Desktop/cv_photos/park.jpg', 'PNG files and JPG files (*.png *.jpg)') We need the first tuple element.

    

#Func to save a file in a specific directory.
def save(self):
    try:
        dir_name = img_dir[-1] #The last image path in our img_dir list will be the picture the user will want to save.
        random_num = str(randint(0,10000000000000))+".png"
        dst_path = (self.lineEdit_savepath.text())

        if dst_path:#Check if the path given is valid to save the edited picture
            final_path = os.path.join(dst_path, random_num)#Create a new path joining the path selected and a random number+extension generator
            shutil.copy(dir_name, final_path)
            show_stuff("Archivo correctamente guardado")
        else:
            show_stuff("Por favor, seleccione una dirección para guardar sus fotos")

    except IndexError:
        show_stuff("Por favor, compruebe si se ha cargado correctamente la foto en el editor") #If img_dir is empty it means the user didnt upload any picture to the editor, so when calling img_dir[-1] it will give an IndexError


#Simple func to change the widget(screen)
def change_screen(page, widget):
    widget.setCurrentIndex(widget.currentIndex() + page)


#This func will remove the last element in img_dir list and in the temp directory. Then it will call the change_load_self() func to show in the editor the previous last img in img_dir list again.
def undo(self):
    if len(img_dir) <= 1:
        show_stuff("Esta es la imagen original")
        return
    else:
        os.remove(img_dir[-1])
        img_dir.pop(-1)
        change_load_image(self)
        self.pushButton_rotate.setEnabled(True)


#This func will look for all the imgs in the temp directory and will add the last one to the img_dir list. Then, it will call the change_load_image() func to show that last img in the editor. 
def add_img_dir(self):
    number = str(os.listdir(r"C:\Users\user\Desktop\cv_photos\temp")[-1])
    new_path = os.path.join(r"C:\Users\user\Desktop\cv_photos\temp",number)
    img_dir.append(new_path)
    change_load_image(self)


#This func will put the img selected by the path provided in the editor Graphics displayer (QGraphicsView). Then it will unlock all the editing buttons so the user can start editing.
def load_image(self):
    imagen = QImage(self.line_file.text())
    if imagen.isNull():
        show_stuff("La imagen no se ha cargado correctamente.")
        return
    img_dir.append(self.line_file.text())
    #Set the scene and the img inside
    pic = QGraphicsPixmapItem(QPixmap.fromImage(imagen))
    self.graphicsView.setScene(QGraphicsScene())
    self.graphicsView.scene().addItem(pic)
    self.graphicsView.fitInView(pic, Qt.KeepAspectRatio)
    #Unlock the buttons
    self.pushButton_blurr.setEnabled(True)
    self.pushButton_gray.setEnabled(True)
    self.pushButton_invertcolors.setEnabled(True)
    self.pushButton_laplace.setEnabled(True)
    self.pushButton_edges.setEnabled(True)
    self.pushButton_rotate.setEnabled(True)
    self.pushButton_flipV.setEnabled(True)
    self.pushButton_flipH.setEnabled(True)
    self.pushButton_undo.setEnabled(True)
    

#This func will change the img displayed in the editor without adding it to img_dir 
def change_load_image(self):
    imagen = QImage(img_dir[-1])
    if imagen.isNull():
        show_stuff("La imagen no se ha cargado correctamente.")
        return
    pic = QGraphicsPixmapItem(QPixmap.fromImage(imagen))
    self.graphicsView.setScene(QGraphicsScene())
    self.graphicsView.scene().addItem(pic)
    self.graphicsView.fitInView(pic, Qt.KeepAspectRatio)


#Simple func to pop up a msg box.
def show_stuff(msg):
    message = QMessageBox()
    message.setText(str(msg))
    message.setWindowTitle("Atención!")
    message.show()
    message.exec_()


#Camara Edition Functions------------------------------------------------------------------------------------------------------------------

#All the camara editing functions will call the temp_name_generator() to create a name for every img that goes inside the temp directory.
def temp_name_generator():
    numero = str(len(os.listdir(r"C:\Users\user\Desktop\cv_photos\temp")))
    foto_path = os.path.join(r"C:\Users\user\Desktop\cv_photos\temp", (numero+".png"))
    return foto_path


#All functions below have almost the same structure and will use the open cv2 python lib to edit and work with imgs. Func name is self-explanatory.
#First, CV will read the img given and will apply a certain modification or effect to that img. Then it will call the temp_name_generator() and store the name in a variable called img_name. After that it will save the edited img in the img_name path. Finally it will call the add_img_dir() func to add that path in the img_dir list.
def blurr_image(self, path):
    img = cv.imread(path)
    blurred = cv.GaussianBlur(img, (5,5), 0)
    img_name = temp_name_generator()
    cv.imwrite(img_name, blurred)
    add_img_dir(self)



def gray_scale(self, path):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_name = temp_name_generator()
    cv.imwrite(img_name, gray)
    add_img_dir(self)
    


def invert_colors(self, path):
    img = cv.imread(path)
    inverted = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_name = temp_name_generator()
    cv.imwrite(img_name, inverted)
    add_img_dir(self)



def laplace(self, path):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    laplace = cv.Laplacian(gray, ddepth=cv.CV_64F)
    laplace = np.uint8(np.absolute(laplace))
    img_name = temp_name_generator()
    cv.imwrite(img_name, laplace)
    add_img_dir(self)


def edges(self, path):
    img = cv.imread(path)
    edges = cv.Canny(img, 125, 175)
    img_name = temp_name_generator()
    cv.imwrite(img_name, edges)
    add_img_dir(self)
    

def flip(self, path, flip_code):
    img = cv.imread(path)
    flipped = cv.flip(img, flip_code)
    img_name = temp_name_generator()
    cv.imwrite(img_name, flipped)
    add_img_dir(self)


def rotate (self, path, angle=0):
    try:
        angle = int(angle)
        img = cv.imread(path)
        dimensions = (width, height) = (img.shape[:2])[::-1]

        rotation_point = (width//2, height//2)
        
        rotated_matrix = cv.getRotationMatrix2D(rotation_point, angle, 1.0)

        rotated_img = cv.warpAffine(img, rotated_matrix, dimensions)
        img_name = temp_name_generator()
        cv.imwrite(img_name, rotated_img)
        add_img_dir(self)
        self.pushButton_rotate.setEnabled(False)
    except ValueError:
        show_stuff("Introduzca un ángulo de rotación válido")
    

    
    