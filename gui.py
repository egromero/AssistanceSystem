import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, QTime, QDateTime
import datetime
from ApiMain import *


class Dashboard(QWidget):	

	def __init__(self):
		super().__init__()
		self.init_GUI()
		self.columna = 'J'

	def init_GUI(self):
		# Creamos una etiqueta para status
		#self.showFullScreen()
		date = QDate.currentDate().toString('dd/MM')
		self.label1 = QLabel('Asistencia: '+ date, self)
		self.label1.move(50,50)


		# Creamos la grilla para ubicar los Widget (botones) de manera matricial
		self.grilla = QGridLayout()

		valores = ['Mauricio Huala', 'Noemí Bontá', 'Francesco Crivelli', 'Vicente Vazquez',
		           'Ignacio Monardes', 'Bruno Caro', 'Barbara Gutierrez', 'Macarena Abarca',
		           'Jonás Oviedo', 'Florencia Buschiazzo', 'Victoria Mauro','Camilo Aravena',
		           'Admin']

		# Generamos las posiciones de los botones en la grilla y le asociamos
		# el texto que debe desplegar cada boton guardados en la lista valores

		posicion = [(i,j) for i in range(7) for j in range(2)]

		for posicion, valor in zip(posicion, valores):
		    if valor == '':
		        continue

		    boton = QPushButton(valor)

		    # A todos los botones les asignamos el mismo slot o método
		    boton.clicked.connect(self.boton_clickeado)

		    # El * permite convertir los elementos de la tupla como argumentos
		    # independientes
		    self.grilla.addWidget(boton, *posicion)

		# Creamos un Layout vertical
		vbox = QVBoxLayout()

		# Agregamos el label al layout con addWidget
		vbox.addWidget(self.label1)

		# Agregamos el layout de la grilla al layout vertical con addLayout
		vbox.addLayout(self.grilla)
		self.setLayout(vbox)

		self.move(300, 150)
		self.setWindowTitle('Verificacion')
		self.show()

		
	def pasar_dia(self):

		SPREADSHEET_ID = '1AtwgdRFTtqv-Y1kq3eUPFivaFd8nudzyO0XGKrvo4j0'
		RANGE_NAME = 'assitence1'
		gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
		idxletra = len(gsheet['values'][1])
		nxtletra = list(map(chr, range(65, 91)))[idxletra]
		self.columna = nxtletra

	def boton_clickeado(self):
		# En este método identificaremos el botón y la posición de este en la
		# grilla.

		# Sender retorna el objeto que fue clickeado
		boton = self.sender()

		# Obtenemos el identificador del elemento en la grilla
		idx = self.grilla.indexOf(boton) + 1

		self.verificacion = PasswordWindow(idx, self.columna)
		self.verificacion.show()
	



class PasswordWindow(QWidget):

	def __init__(self, user, columna):
		super().__init__()
		self.password = ''
		self.user = user
		self.columna = columna
		self.pws = {1: '0107', 2: '1503', 3: '2110', 4: '2211',
					5: '2110', 6: '0302', 7: '', 8: '0810',
					9: '0608', 10: '0405', 11: '1507', 12: '0201',
					13: '6955'}

		self.init_GUI()

	def init_GUI(self):
		#self.showFullScreen()
		# Creamos una etiqueta para status
		self.label1 = QLabel('Pincode: ', self)
		self.label1.move(50,50)
		
		# Creamos la grilla para ubicar los Widget (botones) de manera matricial
		self.grilla = QGridLayout()

		valores = ['1', '2', '3',
					'4', '5', '6',
					'7', '8', '9',
					'0', 'go', 'del','bck']

		# Generamos las posiciones de los botones en la grilla y le asociamos
		# el texto que debe desplegar cada boton guardados en la lista valores

		posicion = [(i,j) for i in range(5) for j in range(3)]

		for posicion, valor in zip(posicion, valores):
			if valor == '':
				continue

			boton = QPushButton(valor)

		# A todos los botones les asignamos el mismo slot o método
			boton.clicked.connect(self.boton_clickeado)

		# El * permite convertir los elementos de la tupla como argumentos
		# independientes
			self.grilla.addWidget(boton, *posicion)

		# Creamos un Layout vertical
		vbox = QVBoxLayout()

		# Agregamos el label al layout con addWidget
		vbox.addWidget(self.label1)


		# Agregamos el layout de la grilla al layout vertical con addLayout
		vbox.addLayout(self.grilla)
		self.setLayout(vbox)

		self.move(300, 150)
		self.setWindowTitle('Verificacion')

	def boton_clickeado(self):
		# En este método identificaremos el botón y la posición de este en la
		# grilla.

		# Sender retorna el objeto que fue clickeado
		boton = self.sender()

		# Obtenemos el identificador del elemento en la grilla
		idx = self.grilla.indexOf(boton) + 1

		if idx == 11:
			if len(self.password) == 4:
				self.verificar()
		elif idx == 12:
			self.password = self.password[:-1]
		elif idx == 13:
			self.close()
		elif not(len(self.password) > 3):
			self.password += '0' if idx == 10 else str(idx)
		

		# Con el identificador obtenemos la posición del ítem en la grilla
		posicion = self.grilla.getItemPosition(idx)

		# Actualizamos
		self.label1.setText('{}'.format(self.password))

	
	def verificar(self):
		if self.pws[self.user] == self.password:
			if self.user == 13:
				ex.pasar_dia()
				self.label1.setText('Admin')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Information)
				msg.setText("Avanzado el día")
				msg.setWindowTitle("Alerta!")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				self.close()
				return

			self.label1.setText('Asistencia Marcada')
			self.appendValues()
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Asistencia Marcada Correcta")
			msg.setWindowTitle("Alerta!")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			self.close()
		else:
			self.label1.setText('Pin Incorrecto')
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("PinPass Incorrecto, Asistencia no marcada")
			msg.setWindowTitle("Alerta!")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			self.close()

	def appendValues(self):

		SPREADSHEET_ID = '1AtwgdRFTtqv-Y1kq3eUPFivaFd8nudzyO0XGKrvo4j0'
		print('USUARIO', self.user+1, 'COLUMNA', self.columna)
		RANGE_NAME = 'assitence1!{}{}'.format(self.columna,self.user+1)
		time = QTime.currentTime().toString('hh:mm')
		score = self.checkTime(time)
		listValues = [[time],[score]]
		resource = {"majorDimension": "COLUMNS",
  					"values": listValues}

		append_value(SPREADSHEET_ID, RANGE_NAME, resource)
	
	def checkTime(self, time):
		hora, minuto = time.split(':')
		if int(hora) == 11 and int(minuto)>15:
			return 1
		elif int(hora) > 11 and int(hora) < 18:
			return 0.5
		else:
			return 0

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Dashboard()
	sys.exit(app.exec_())





