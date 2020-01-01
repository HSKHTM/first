import main ,gui
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui import Ui_MainWindow
class draw():
	def paintEvent(self, event):
		qp = QPainter(main.ui.widget)
		qp.begin(self)
		self.drawText(event, qp)
		qp.end()

	def drawText(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setFont(QFont('Decorative', 10))
		qp.drawText(event.rect(), Qt.AlignCenter, self.text)
		self.ui.widget.hide()