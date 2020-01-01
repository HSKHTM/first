from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui import Ui_MainWindow
import sys,random
import math,os
import decimal


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.button1_click)
        self.ui.pushButton_2.clicked.connect(self.button2_click)
        self.ui.pushButton_3.clicked.connect(self.button3_click)
        self.pix = QPixmap('pic.png')
        self.ui.label.setPixmap(self.pix)
        self.ui.textBrowser.setFontPointSize(10)
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

    def createActions(self):
        root = QFileInfo(__file__).absolutePath()
        self.openAct = QAction(QIcon(root + '/images/open.png'), "&Open...",
                               self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.button1_click)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application", triggered=self.close)

    def createMenus(self):
        self.ui.fileMenu = self.menuBar().addMenu("&File")
        self.ui.fileMenu.addAction(self.openAct)
        self.ui.fileMenu.addSeparator()
        self.ui.fileMenu.addAction(self.exitAct)

    def createToolBars(self):
        self.ui.fileToolBar = self.addToolBar("File")
        self.ui.fileToolBar.addAction(self.openAct)

    def createStatusBar(self):
        self.ui.statusbar.showMessage("Ready")

    def splitString(self,S):
        S = S.upper()
        S = S.replace(" ", "")

        LST = [""]
        m = 0
        S_len = len(S)
        i = 0
        while (i < S_len):
            if ((S[i] >= "A" and S[i] <= "Z")):
                LST[m] += S[i]
            else:
                m += 1
                LST.append("")
                while (i < S_len and (S[i].isdigit() or S[i] == "." or S[i] == "-" or S[i] == "+")):
                    LST[m] += S[i]
                    i += 1
                else:
                    if (i < S_len and not S[i].isdigit()):
                        m += 1
                        LST.append(S[i])
            i += 1
        if (LST[-1] == "\n"):
            return LST[0:-1]
        else:
            return (LST)

    def get_line_info(self,S):
        init_parmeters = self.splitString(S)
        # print(init_parmeters)
        return init_parmeters

    def Def_Group(self, STR, t1, t2, SA):  # "CCW_ARC" , a , a_new , Sa
        D = []
        if (STR == "CW_ARC"):
            if ((t1 - SA) >= 0):
                D = [t2, t1]
            else:
                D = [0, t1, t2, 360]
        elif (STR == "CCW_ARC"):
            if ((t1 + SA) >= 360):
                D = [0, t2, t1, 360]
            else:
                D = [t1, t2]

        return (D)

    def Switch_Code_Type(self,code, num):
        if (code == "X" or code == "Y"):
            return "L_LINE"
        if (code + num == "G01" or code + num == "G1" or code + num == "G00" or code + num == "G0"):
            return "L_LINE"
        if (code + num == "G02" or code + num == "G2"):
            return "CW_ARC"
        if (code + num == "G03" or code + num == "G3"):
            return "CCW_ARC"

    def Get_Line_Para(self,cmd, X_old, Y_old):
        x = X_old
        y = Y_old

        if ("G" in cmd):
            cmd.pop(0)
            cmd.pop(0)
        L = len(cmd) - 1

        Find_X = -1
        m = 0
        while (m < L):
            if (cmd[m] == "X"):
                Find_X = m + 1  # ["X","654654","Y","454"]
            m += 1
        if (Find_X >= 0):
            x = float(cmd[Find_X])
        else:
            x = X_old

        Find_Y = -1
        m = 0
        while (m < L):
            if (cmd[m] == "Y"):
                Find_Y = m + 1
            m += 1
        if (Find_Y >= 0):
            y = float(cmd[Find_Y])
        else:
            y = Y_old

        return [x, y]

    def Get_CW_Arc_Para(self,CMD, X_old, Y_old):
        cmd = CMD
        cmd.pop(0)
        cmd.pop(0)
        L = len(cmd) - 1
        x = []
        y = []
        i = []
        j = []
        r = []
        a_old = []
        a_new = []

        Find_X = -1
        m = 0
        while (m < L):
            if (cmd[m] == "X"):
                Find_X = m + 1
            m += 1
        if (Find_X >= 0):
            x = float(cmd[Find_X])
        else:
            x = X_old

        Find_Y = -1
        m = 0
        while (m < L):
            if (cmd[m] == "Y"):
                Find_Y = m + 1
            m += 1
        if (Find_Y >= 0):
            y = float(cmd[Find_Y])
        else:
            y = Y_old

        Find_I = -1
        m = 0
        while (m < L):
            if (cmd[m] == "I"):
                Find_I = m + 1
            m += 1
        if (Find_I >= 0):
            i = float(cmd[Find_I])
        else:
            i = 0

        Find_J = -1
        m = 0
        while (m < L):
            if (cmd[m] == "J"):
                Find_J = m + 1
            m += 1
        if (Find_J >= 0):
            j = float(cmd[Find_J])
        else:
            j = 0

        Find_R = -1
        m = 0
        while (m < L):
            if (cmd[m] == "R"):
                Find_R = m + 1
            m += 1
        if (Find_R >= 0):
            r = float(cmd[Find_R])
        else:
            r = (i * i + j * j) ** 0.5

        # find center
        x_c = X_old + i
        y_c = Y_old + j
        # print("CENTER:",x_c,y_c)

        # find first angle
        X0 = X_old - x_c
        Y0 = Y_old - y_c
        a_old = math.atan2(Y0, X0) * 180 / math.pi

        if(a_old < 0):
            a_old = 360 + a_old

        # find second angle
        x_d = x - x_c
        y_d = y - y_c
        a_new = math.atan2(y_d, x_d) * 180 / math.pi

        if (a_new < 0):
            a_new = 360 + a_new

        # find spin angle
        S_a = round(decimal.Decimal(a_new - a_old))
        a_old = round(decimal.Decimal(a_old))
        a_new = round(decimal.Decimal(a_new))

        # find rect
        rect_X_c = round(decimal.Decimal(x_c - math.fabs(r)), 4)
        rect_Y_c = round(decimal.Decimal(y_c + math.fabs(r)), 4)
        rect_W = round(decimal.Decimal(2 * r), 4)
        rect_H = round(decimal.Decimal(2 * r), 4)

        x = round(float(decimal.Decimal(x)), 4)
        y = round(float(decimal.Decimal(y)), 4)

        # print(rect_X_c,rect_Y_c,rect_H,rect_W,a_old,S_a)
        return [float(rect_X_c), float(rect_Y_c), float(rect_H), float(rect_W), a_old, a_new, x, y]

    def draw_gcode(self):
        pass

    def drawline(self):
        qp = QPainter(self.ui.label.pixmap())
        qp.drawPixmap()
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(100, 100, 100, 100)
        qp.drawLine(300, 300, 400, 400)
        self.update()
    def draw_arc(self):
        pass

    def button1_click(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'e:\\', "GCODE files (*.tab *.2nc *.cnc *.txt *.nc *.ngc)")
        if fname[0]!="":
            filename = fname[0]
            str_name = '#' +os.path.split(filename)[1]
            self.ui.statusbar.showMessage(os.path.split(filename)[1]+ " is opened")
            working = open(filename, 'r')
            lines = working.readlines()
            self.ui.textBrowser.setText('')
            self.ui.textBrowser.setFontPointSize(14)
            self.ui.textBrowser.append(str_name)
            font = QFont('Tahoma', 8)
            font.setBold(False)
            self.ui.textBrowser.setFontPointSize(8)
            for line in lines:
                self.ui.textBrowser.append(line.replace("\n", ''))
            working.close()
            File = open(fname[0], "r")
            G_CODE = File.readlines()
            CMD_LIST = []
            qp = QPainter(self.ui.label.pixmap())
            qp.setRenderHint(QPainter.Antialiasing)
            rect = QRect(self.ui.label.rect())
            pen = QPen(Qt.black, 1, Qt.SolidLine)
            qp.setPen(pen)
            for line in G_CODE:
                CCMMDD = self.get_line_info(line)
                CMD_LIST.append(CCMMDD)
                # print(CCMMDD)

			
			# X_OLD FUNCTION
            X_old = 0
            Y_old = 0

            X_new = X_old
            Y_new = Y_old
            #ANALYZE DATA
            DATA = []
            X_max = 0
            Y_max = 0
            X_min = 0
            Y_min = 0

            ###take parameters from first line in CMD_LIST
            First_CMD = CMD_LIST[0]
            Code_Type = self.Switch_Code_Type(First_CMD[0], First_CMD[1])
            X_old = X_new
            Y_old = Y_new

            if (Code_Type == "L_LINE"):
                [X_new, Y_new] = self.Get_Line_Para(First_CMD, X_old, Y_old)
                X_min = X_new
                X_max = X_new
                Y_min = Y_new
                Y_max = Y_new

                DATA.append([1 , X_new, Y_new , X_new , Y_new ])

            elif (Code_Type == "CW_ARC"):
                [X, Y, H, W, a, Sa, X_new, Y_new] = self.Get_CW_Arc_Para(First_CMD, X_old, Y_old)
                X_min = X_new
                X_max = X_new
                Y_min = Y_new
                Y_max = Y_new

                DATA.append([2 , X , Y , H , W , a , Sa])

            elif (Code_Type == "CCW_ARC"):
                [X, Y, H, W, a, Sa, X_new, Y_new] = self.Get_CW_Arc_Para(First_CMD, X_old, Y_old)
                X_min = X_new
                X_max = X_new
                Y_min = Y_new
                Y_max = Y_new

                DATA.append([3 , X , Y , H , W , a ,Sa])

            ### POP THE FIRST LINE
            CMD_LIST.pop(0)


            for CMD in CMD_LIST:
                if (CMD[0] == ""):
                    continue

                Code_Type = self.Switch_Code_Type(CMD[0], CMD[1])
                X_old = X_new
                Y_old = Y_new

                if (Code_Type == "L_LINE"):
                    [X_new, Y_new] = self.Get_Line_Para(CMD, X_old, Y_old)

                    if X_new > X_max:
                        X_max = X_new
                    if Y_new > Y_max:
                        Y_max = Y_new
                    if X_new < X_min:
                        X_min = X_new
                    if Y_new < Y_min:
                        Y_min = Y_new

                    DATA.append([1 , X_old, Y_old , X_new , Y_new ])

                    #####qp.drawLine(X_old, -Y_old , X_new , -Y_new )

                elif(Code_Type == "CW_ARC"):
                    [X, Y, H, W, a, a_new, X_new, Y_new] = self.Get_CW_Arc_Para(CMD, X_old, Y_old)
                    if (a_new < a):
                        Sa = a - a_new
                    else:
                        Sa = a + 360 - a_new

                    a2 = a - Sa

                    D = self.Def_Group(Code_Type, a, a2, Sa)

                    F_Sin_Values = []
                    for aa in D:
                        F_Sin_Values.append(float(round(decimal.Decimal(math.sin(math.radians(aa))), 4)))
                    for aa in [90, 270]:
                        F_Sin_Values.append(float(round(decimal.Decimal(math.sin(math.radians(aa))), 4)))

                    YY_min = min(F_Sin_Values) - Y + H/2
                    Y_min = min(Y_min, YY_min)
                    YY_max = max(F_Sin_Values) + Y + H/2
                    Y_max = max(Y_max, YY_max)

                    D = self.Def_Group(Code_Type , a , a2 , Sa)

                    F_Cos_Values = []
                    for aa in D:
                        F_Cos_Values.append(float(round(decimal.Decimal(math.cos(math.radians(aa))), 4)))
                    for aa in [90, 270]:
                        F_Cos_Values.append(float(round(decimal.Decimal(math.cos(math.radians(aa))), 4)))

                    XX_min = min(F_Cos_Values) - X + H/2
                    X_min = min(X_min, XX_min)
                    XX_max = max(F_Cos_Values) + X + H/2
                    X_max = max(X_max, XX_max)
                    DATA.append([2 , X , Y , H , W , a , Sa])
                    #qp.drawArc(X * 3, Y * -3, H * 3, W * 3, a * 16, -Sa * 16)
                    # qp.drawArc(X*2, -Y*2, H*2, W*2, a * 16, -Sa * 16)

                elif (Code_Type == "CCW_ARC"):
                    [X, Y, H, W, a, a_new, X_new, Y_new] = self.Get_CW_Arc_Para(CMD, X_old, Y_old)

                    if (a_new > a):
                        Sa = a_new - a
                    else:
                        Sa = 360 - a_new + a

                    a2 = a + Sa

                    D = self.Def_Group(Code_Type, a, a2, Sa)

                    F_Sin_Values = []
                    for aa in D:
                        F_Sin_Values.append(float(round(decimal.Decimal(math.sin(math.radians(aa))), 4)))
                    for aa in [90, 270]:
                        F_Sin_Values.append(float(round(decimal.Decimal(math.sin(math.radians(aa))), 4)))

                    YY_min = min(F_Sin_Values) - Y + H/2
                    Y_min = min(Y_min, YY_min)
                    YY_max = max(F_Sin_Values) + Y + H/2
                    Y_max = max(Y_max, YY_max)

                    D = self.Def_Group(Code_Type, a, a2, Sa)

                    F_Cos_Values = []
                    for aa in D:
                        F_Cos_Values.append(float(round(decimal.Decimal(math.cos(math.radians(aa))), 4)))
                    for aa in [0, 180]:
                        F_Cos_Values.append(float(round(decimal.Decimal(math.cos(math.radians(aa))), 4)))

                    XX_min = min(F_Cos_Values) - X + H/2
                    X_min = min(X_min, XX_min)
                    XX_max = max(F_Cos_Values) + X + H/2
                    X_max = max(X_max, XX_max)



                    DATA.append([3, X , Y , H , W , a , Sa])
                    #qp.drawArc(X * 3, Y * -3, H * 3, W * 3, a * 16, Sa * 16)
                    # qp.drawArc(X*2,-Y*2, H*2, W*2, a * 16, Sa * 16)

            #factor
            print(X_min,X_max,Y_min,Y_max)
            Rect_drawing = QRect(X_min, -Y_max, X_max - X_min, Y_max - Y_min)
            Drawing_Width = X_max - X_min
            Drawing_Height = Y_max - Y_min

            Window_Width = 731
            Window_height = 541

            X_Factor =  Window_Width/Drawing_Width
            Y_factor = Window_height/Drawing_Height
            factor = min(X_Factor,Y_factor)*0.98
            #factor=1

            #TRANSLATE
            rect_after_factor=QRect(X_min*factor, -Y_max*factor,( X_max - X_min)*factor, (Y_max - Y_min)*factor)
            qp.translate(rect_after_factor.center())
            qp.translate(rect.center()-rect_after_factor.center()*2-QPoint(100,10))

            #DRAWING
            for LINE in DATA:
                if (LINE[0] == 1):
                    qp.drawLine(LINE[1] * factor, -LINE[2] * factor, LINE[3] * factor, -LINE[4] * factor)
                elif (LINE[0] == 2):
                    qp.drawArc(LINE[1] * factor, -LINE[2] * factor, LINE[3] * factor, LINE[4] * factor, LINE[5]*16,
                               -LINE[6]*16)
                elif (LINE[0] == 3):
                    qp.drawArc(LINE[1] * factor, -LINE[2] * factor, LINE[3] * factor, LINE[4] * factor, LINE[5]*16,
                               LINE[6]*16)
            self.ui.textBrowser.scrollToAnchor(str_name)
            self.update()


    def button2_click(self):
        pass

    def closeEvent(self, event):
        print('mainwindow is closed')
    def button3_click(self):
        self.pix = QPixmap('pic1.png')
        self.ui.label.setPixmap(self.pix)
        # self.qp.end()
        self.update()






if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
