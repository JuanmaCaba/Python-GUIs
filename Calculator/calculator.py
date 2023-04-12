from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("calc_app.ui", self)

        #Numberic buttons
        for i in range(10):
            button = getattr(self, f"pushButton_{i}")#La función getattr te busca un atributo dentro de una clase (en este caso self-->QMainWindow) y te devuelve su valor, el cual puedes almacenar en una variable si quieres.
            button.clicked.connect(lambda _, x=i: number_button(self, x))
        
        
        self.pushButton_dec.clicked.connect(lambda: number_button(self, "."))

        #Operations Buttons
        self.pushButton_add.clicked.connect(lambda: number_button(self, "+"))
        self.pushButton_take.clicked.connect(lambda: number_button(self, "-"))
        self.pushButton_mult.clicked.connect(lambda: number_button(self, "x"))
        self.pushButton_div.clicked.connect(lambda: number_button(self, "/"))
        self.pushButton_equal.clicked.connect(lambda: resultado(self))
        self.pushButton_delete.clicked.connect(lambda: del_func(self))
        
       
        
operations = []
def number_button(self, x):
        operations.append(str(x))
        new_operation = "".join(operations)
        self.result.setText(new_operation)


def transform():
    new_operator = []
    value = ""
    numbers = []
    if not operations:
        return new_operator
    try:
        for index,x in enumerate(operations):
            if index == 0 and x in ["+","-"]:
                numbers.append(x)   
            elif x in ["0","1","2","3","4","5","6","7","8","9","."]:
                numbers.append(x)
            elif x not in ["0","1","2","3","4","5","6","7","8","9","."] and operations[index -1] in ["+","-","x","/"]:
                numbers.append(x)
            elif x not in ["0","1","2","3","4","5","6","7","8","9","."]:
                value = "".join(numbers)
                new_operator.append(float(value))
                new_operator.append(x)
                value = ""
                numbers = []     
        value = "".join(numbers)
        new_operator.append(float(value))
    except ValueError:
        error_message = QMessageBox()
        error_message.setText("Error de sintaxis")
        error_message.show()
        error_message.exec_()
        operations.clear()
        return

    return new_operator

           
def operator():
    new_operations = transform()
    try:
        if not new_operations:
            return ""
        while len(new_operations) > 1:
            for index, value in enumerate(new_operations): 
                if value in ["x","/"]:
                    partial_result = 0
                    if value == "x":
                        partial_result = new_operations[index -1] * new_operations[index +1]
                        new_operations[index - 1] = partial_result
                        new_operations.pop(index + 1)
                        new_operations.pop(index)
                    if value == "/":
                        partial_result = new_operations[index -1] / new_operations[index +1]
                        new_operations[index - 1] = partial_result
                        new_operations.pop(index + 1)
                        new_operations.pop(index)
            
            for index,value in enumerate(new_operations):
                if value in ["+","-"]:
                    partial_result2 = 0
                    if value == "+":
                        partial_result2 = new_operations[index -1] + new_operations[index +1]
                        new_operations[index - 1] = partial_result2
                        new_operations.pop(index + 1)
                        new_operations.pop(index)
                    if value == "-":
                        partial_result2 = new_operations[index -1] - new_operations[index +1]
                        new_operations[index - 1] = partial_result2
                        new_operations.pop(index + 1)
                        new_operations.pop(index)
    except ZeroDivisionError:
        message = QMessageBox()
        message.setText("Can't divide by 0")
        message.show()
        message.exec_()
    result = round(new_operations[0], 8)
    operations.clear()
    
    return result

def del_func(self):
    operations.clear()
    self.result.setText("")


def resultado(self):
    result = operator()
    for i in str(result):
        operations.append(str(i))
    self.result.setText(str(result))
    

def main():
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()