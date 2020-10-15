from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

textFilePath = ""
keyFilePath = ""
saveFilePath = ""

MAGIC = 'ADFGVX'

secretAlphabet = "cizj64tayd5gpsk7rv1qxh98flb20o3mwneu"


class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno,self).__init__(*args,*kwargs)
        self.setWindowTitle("Maszyna szyfrująca/deszyfrująca ADFGVX")

        #########NAPISY#########
        
        titleText = QLabel()
        titleText.setText("Podaj tekst i klucz lub wybierz pliki")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Arial',30))
        
        self.subtitleText = QLabel()
        self.subtitleText.setText("")
        self.subtitleText.setAlignment(Qt.AlignCenter)
        self.subtitleText.setFont(QFont('Arial',20))
        
        self.opisText = QLabel()
        self.opisText.setText("Aleksander Stęplewski 140784 \n Działa na literach i cyfrach, bez znaków polskich ani specjalnych. \n Spacje zostają usuwane przy szyfrowaniu. \n Przyjmuje tylko pliki .txt")
        self.opisText.setAlignment(Qt.AlignCenter)
        self.opisText.setFont(QFont('Arial',15))
        
        self.dzialanieText = QLabel()
        self.dzialanieText.setText("Maszyna do szyfru ADFGVX")
        self.dzialanieText.setAlignment(Qt.AlignCenter)
        self.dzialanieText.setFont(QFont('Arial',35))
        
        self.messageField = QLineEdit()
        self.messageField.setPlaceholderText("Podaj tekst lub szyfr")
        
        self.keyField = QLineEdit()
        self.keyField.setPlaceholderText("Podaj klucz")
        
        textFieldsLayout = QHBoxLayout()
        textFieldsLayout.addWidget(self.messageField)
        textFieldsLayout.addWidget(self.keyField)
        textFieldsLayoutW = QWidget()
        textFieldsLayoutW.setLayout(textFieldsLayout)
        
        ######PRZYCISKI#######
        
        encryptButton = QPushButton()
        encryptButton.setText("Szyfruj")
        encryptButton.clicked.connect(self.encryptClicked)
        
        decryptButton = QPushButton()
        decryptButton.setText("Deszyfruj")
        decryptButton.clicked.connect(self.decryptClicked)
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(encryptButton)
        buttonsLayout.addWidget(decryptButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)
        
        textSelectButton = QPushButton()
        textSelectButton.setText("Wybierz plik tekstu")
        textSelectButton.clicked.connect(self.textSelectClicked)
        
        keySelectButton = QPushButton()
        keySelectButton.setText("Wybierz plik klucza")
        keySelectButton.clicked.connect(self.keySelectClicked)
        
        saveButton = QPushButton()
        saveButton.setText("Zapisz pole tekstu do pliku")
        saveButton.clicked.connect(self.saveClicked)

        selectLayout = QHBoxLayout()
        selectLayout.addWidget(textSelectButton)
        selectLayout.addWidget(keySelectButton)
        selectLayoutW = QWidget()
        selectLayoutW.setLayout(selectLayout)
        
        saveLayout = QHBoxLayout()
        saveLayout.addWidget(saveButton)
        saveLayoutW = QWidget()
        saveLayoutW = QWidget()
        saveLayoutW.setLayout(saveLayout)
        
        #######WIDGETY#########
        
        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(self.opisText)
        mainMenu.addWidget(self.dzialanieText)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(self.subtitleText)
        mainMenu.addWidget(textFieldsLayoutW)
        mainMenu.addWidget(buttonsLayoutW)
        mainMenu.addWidget(selectLayoutW)
        mainMenu.addWidget(saveLayoutW)
        

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)
        
    ######FUNKCJE########
    
    def encrypt(self):
        print("encrypt")
        
        message = self.messageField.text()
        message = message.lower()
        keyword = self.keyField.text()
        keyword = keyword.lower()
        
        #szyfrowanie ADFGVX
        key = []
        for c in keyword:
            if c not in key: key.append(c)
            
        n = len(key)
        k = sorted(range(n), key = lambda i: key[i])
        
        s = []
        for c in message:
            if c.isalpha() or c.isdigit():
                row, col = divmod(secretAlphabet.index(c),6)
                s += [MAGIC[row], MAGIC[col]]
                
        return ''.join(s[j] for i in k for j in range(i, len(s), n))
        
    def decrypt(self):
        print("decrypt")
        
        message = self.messageField.text()
        message = message.upper()
        keyword = self.keyField.text()
        keyword = keyword.lower()
        
        #deszyfrowanie ADFGVX
        key = []
        for c in keyword:
            if c not in key: key.append(c)
        
        n = len(key)
        k = sorted(range(n), key=lambda i: key[i])
        
        m = len(message)
        x = [j for i in k for j in range(i, m, n)]
        
        y = ['']*m
        for i, c in zip(x, message): y[i] = c
        
        s = []
        for i in range(0, m, 2):
            row, col = y[i:i+2]
            s.append(secretAlphabet[6 * MAGIC.index(row) + MAGIC.index(col)])
        
        return ''.join(s)
        
    
    def encryptClicked(self):
        self.subtitleText.setText("Szyfruje " + self.messageField.text() + " kluczem " + self.keyField.text())
        try:
            self.messageField.setText(self.encrypt())
        except:
            print("cos poszlo nie tak")
    
    def decryptClicked(self):
        self.subtitleText.setText("Deszyfruje " + self.messageField.text() + " kluczem " + self.keyField.text())
        try:
            self.messageField.setText(self.decrypt())
        except:
            print("cos poszlo nie tak")
        
    def textSelectClicked(self):
        textFilePath = filedialog.askopenfilename()
        self.subtitleText.setText("Biorę tekst z: " + textFilePath)
        try:
            f = open(textFilePath, "r")
            text = f.read()
            f.close()
            self.messageField.setText(text)
        except:
            print("zamknieto")
        
    def keySelectClicked(self):
        keyFilePath = filedialog.askopenfilename()
        self.subtitleText.setText("Biorę klucz z: " + keyFilePath)
        try:
            f = open(keyFilePath, "r")
            key = f.read()
            f.close()
            self.keyField.setText(key)
        except:
            print("zamknieto")
        
    def saveClicked(self):
        self.subtitleText.setText("Zapisuje")
        saveFilePath = filedialog.asksaveasfilename()
        try:
            f = open(saveFilePath, "w")
            f.write(self.messageField.text())
            f.close
        except:
            print("zamknieto")
        


########MAIN##########

app = QApplication(sys.argv)
window = Okno()
#window.setFixedSize(800,600)
window.setStyleSheet("background-color: rgb(236,236,236)")
window.show()
app.exec_()
