#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu March 30 1:50

@author: Greg Bauman
"""

#TODO
#Create good comments for tabs, create new file to speak to instrement, use
#folder on other computer as ex to set mag field using utilities
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import bcwidgets
import functions

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'NMR Control Panel'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 1800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        print("making table")
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.scans = 0
        self.Nscans = 0
        self.currentVoltage = 10
        self.currChannel = 0
        
        # Initialize tab screen
        print("Making tabs")
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Single")
        self.tabs.addTab(self.tab2,"Multiple")
        self.tabs.addTab(self.tab3,"Utilities")
        self.tabs.addTab(self.tab4,"Coil Utilities")
        
        # Create first tab
        firstTab = QVBoxLayout()
        
        self.label1 = QLabel()
        self.label1.setText("Single NIFID Controls")
        firstTab.addWidget(self.label1)
        
        self.label2 = QLabel()
        self.label2.setText("NFID Scan Number: " + str(self.scans))
        firstTab.addWidget(self.label2)
        
        self.NFID = QPushButton("Run NFID")
        self.NFID.clicked.connect(self.on_click)
        firstTab.addWidget(self.NFID)
        
        #Create Tab1----------------------------------------------------------
        
        #Create three  Vboxs
        box1 = QVBoxLayout()
        box2 = QVBoxLayout()
        box3 = QVBoxLayout()
        
        #Create the 16 horizontal lines for the 3 Vboxs
        print("Making Boxes")
        box1h1 = QHBoxLayout()
        box1h2 = QHBoxLayout()
        box1h3 = QHBoxLayout()
        box1h4 = QHBoxLayout()
        box1h5 = QHBoxLayout()
        box1h6 = QHBoxLayout()
        box1h7 = QHBoxLayout()
        
        box2h1 = QHBoxLayout()
        
        box3h1 = QHBoxLayout()
        box3h2 = QHBoxLayout()
        box3h3 = QHBoxLayout()
        box3h4 = QHBoxLayout()
        box3h5 = QHBoxLayout()
        box3h6 = QHBoxLayout()
        box3h7 = QHBoxLayout()
        box3h8 = QHBoxLayout()
        
        #Box1
        self.singSweep = QPushButton("Fit Single Sweep")
        box1h1.addWidget(self.singSweep)
        
        self.nameLabel = QLabel()
        self.nameLabel.setText("Name")
        box1h1.addWidget(self.nameLabel)
        
        self.name = QLineEdit()
        self.name.setFixedWidth(40)
        box1h1.addWidget(self.name)
        
        self.voltsLabel = QLabel()
        self.voltsLabel.setText("Amp (mV)")
        box1h2.addWidget(self.voltsLabel)
        
        self.volts = QSpinBox()
        box1h2.addWidget(self.volts)
        
        self.freqLabel = QLabel()
        self.freqLabel.setText("Freq")
        box1h2.addWidget(self.freqLabel)
        
        self.freq = QSpinBox()
        box1h2.addWidget(self.freq)
        
        self.phaseLabel = QLabel()
        self.phaseLabel.setText("Phase")
        box1h3.addWidget(self.phaseLabel)
        
        self.phase = QSpinBox()
        box1h3.addWidget(self.phase)
        
        self.T2Label = QLabel()
        self.T2Label.setText("T2")
        box1h3.addWidget(self.T2Label)
        
        self.T2 = QSpinBox()
        box1h3.addWidget(self.T2)
        
        self.relativePhaseLabel = QLabel()
        self.relativePhaseLabel.setText("Relative Phase")
        box1h4.addWidget(self.relativePhaseLabel)
        
        self.phase = QSpinBox()
        box1h4.addWidget(self.phase)
        
        self.testParams = QPushButton("Test Params")
        box1h5.addWidget(self.testParams)
        
        self.setFitParams = QPushButton("Set Parmas to Fit")
        box1h5.addWidget(self.setFitParams)
        
        self.show = QCheckBox()
        self.show.setText("Show")
        box1h6.addWidget(self.show)
        
        self.FFTGraph = QPushButton()
        self.FFTGraph.setText("FTT Graph")
        box1h6.addWidget(self.FFTGraph)
        
        self.show2 = QCheckBox()
        self.show2.setText("Show")
        box1h6.addWidget(self.show2)
        
        self.RGraph = QPushButton()
        self.RGraph.setText("R Graph")
        box1h6.addWidget(self.RGraph)
        
        self.show3 = QCheckBox()
        self.show3.setText("Show")
        box1h7.addWidget(self.show3)
        
        self.rawGraph = QPushButton()
        self.rawGraph.setText("Raw Graph")
        box1h7.addWidget(self.rawGraph)
        
        self.rawFTT = QPushButton()
        self.rawFTT.setText("Raw Ftt")
        box1h7.addWidget(self.rawFTT)
        
        #box 2
        self.fitTypeLabel = QLabel()
        self.fitTypeLabel.setText("Fit Type to Use")
        box2h1.addWidget(self.fitTypeLabel)
        
        self.fitType = QComboBox()
        self.fitType.addItems(["Poly", "Exp", "SineX", "SineXY"])
        box2h1.addWidget(self.fitType)
        
        self.flag = QCheckBox("Flag")
        box2h1.addWidget(self.flag)
        
        #box3
        self.NFIDP1Label = QLabel()
        self.NFIDP1Label.setText("Frequency (HZ)")
        box3h1.addWidget(self.NFIDP1Label)
        
        self.NFIDP1 = QSpinBox()
        box3h1.addWidget(self.NFIDP1)
         
        self.NFIDP2Label = QLabel()
        self.NFIDP2Label.setText("Pulse Length (S)")
        box3h2.addWidget(self.NFIDP2Label)
        
        self.NFIDP2 = QSpinBox()
        box3h2.addWidget(self.NFIDP2)
        
        self.NFIDP3Label = QLabel()
        self.NFIDP3Label.setText("RF Amplitude (V)")
        box3h3.addWidget(self.NFIDP3Label)
        
        self.NFIDP3 = QSpinBox()
        box3h3.addWidget(self.NFIDP3)
        
        self.NFIDP4Label = QLabel()
        self.NFIDP4Label.setText("B Field (V)")
        box3h4.addWidget(self.NFIDP4Label)
        
        self.NFIDP4 = QSpinBox()
        box3h4.addWidget(self.NFIDP4)
        
        self.NFIDP5Label = QLabel()
        self.NFIDP5Label.setText("Readout Time")
        box3h5.addWidget(self.NFIDP5Label)
        
        self.NFIDP5 = QSpinBox()
        box3h5.addWidget(self.NFIDP5)
        
        self.NFIDP6Label = QLabel()
        self.NFIDP6Label.setText("Additional Mute Sime (S)")
        box3h6.addWidget(self.NFIDP6Label)
        
        self.NFIDP6 = QSpinBox()
        box3h6.addWidget(self.NFIDP6)
        
        self.NFIDP7Label = QLabel()
        self.NFIDP7Label.setText("Lowpass Filter (HZ)")
        box3h7.addWidget(self.NFIDP7Label)
        
        self.NFIDP7 = QSpinBox()
        box3h7.addWidget(self.NFIDP7)
        
        self.NFIDP8Label = QLabel()
        self.NFIDP8Label.setText("Signil Range")
        box3h8.addWidget(self.NFIDP8Label)
        
        self.NFIDP8 = QSpinBox()
        box3h8.addWidget(self.NFIDP8)
        
        print("adding boxes")
        box1.addLayout(box1h1)
        box1.addLayout(box1h2)
        box1.addLayout(box1h3)
        box1.addLayout(box1h4)
        box1.addLayout(box1h5)
        box1.addLayout(box1h6)
        box1.addLayout(box1h7)
        
        box2.addLayout(box2h1)
        
        box3.addLayout(box3h1)
        box3.addLayout(box3h2)
        box3.addLayout(box3h3)
        box3.addLayout(box3h4)
        box3.addLayout(box3h5)
        box3.addLayout(box3h6)
        box3.addLayout(box3h7)
        box3.addLayout(box3h8)
        
        
        firstTab.addLayout(box1)
        firstTab.addLayout(box2)
        firstTab.addLayout(box3)
        firstTab.addStretch()
        self.tab1.setLayout(firstTab)
        
        #Create Tab 2---------------------------------------------------------
        secondTab = QVBoxLayout()
        
        tab2box1 = QVBoxLayout()
        
        self.tab2TopLabel = QLabel("SpinDown/ Pump Rate/ NMR Loss")
        secondTab.addWidget(self.tab2TopLabel)
        
        self.NFIDscanNum = QLabel("NFIDscanNum: " + str(self.Nscans))
        secondTab.addWidget(self.NFIDscanNum)
        
        #create 
        box1Part1 = QVBoxLayout()
        box1Line1 = QHBoxLayout()
        self.startSpinDownPB = QPushButton("Start Spin Down")
        box1Line1.addWidget(self.startSpinDownPB)
        self.waitCheck = QCheckBox()
        box1Line1.addWidget( self.waitCheck)
        self.waitLabel = QLabel("Wait 1 Hour Before Spin Down")
        box1Line1.addWidget(self.waitLabel)
        
        box1Line2 =QHBoxLayout()
        self.TimeLabel = QLabel("Time Interval (hrs)")
        self.hours = QSpinBox()
        box1Line2.addWidget( self.TimeLabel)
        box1Line2.addWidget(self.hours)
        
        self.AbortLabel = QLabel("ABORT to stop (Lower Left COmmand Window)")
        
        box1Part1.addLayout(box1Line1)
        box1Part1.addLayout(box1Line2)
        box1Part1.addWidget(self.AbortLabel)
        
        box1part2 = QHBoxLayout()
        box1part2Left = QHBoxLayout()
        box1part2Right = QHBoxLayout()
        self.fitSpinButton = QLabel("Fit Spin Down Data")
        
        self.FirstScanNumLabel = QLabel("First Scan Num")
        self.FirstScanNum = QSpinBox()
        
        self.LastScanNumLabel = QLabel("Last Scan Num")
        self.LastScanNum = QSpinBox()
        
        self.NMRLossLabel = QLabel("NMR Loss (not %)")
        self.NMRLoss = QSpinBox()
        
        box1part2Left.addWidget(self.fitSpinButton)
        
        box1part2Right.addWidget(self.FirstScanNumLabel)
        box1part2Right.addWidget(self.FirstScanNum)
        box1part2Right.addWidget(self.LastScanNumLabel)
        box1part2Right.addWidget(self.LastScanNum)
        box1part2Right.addWidget(self.NMRLossLabel)
        box1part2Right.addWidget(self.NMRLoss)
        
        box1part2.addLayout(box1part2Left)
        box1part2.addLayout(box1part2Right)
        
        tab2box1.addLayout(box1Part1)
        tab2box1.addLayout(box1part2)
        
        tab2box2 = QVBoxLayout()
        
        tab2box2Line1 = QHBoxLayout()
        self.startNMRLoss = QPushButton("Start NMR Loss")
        self.SweepNumsLabel = QLabel("Number of Sweeps")
        self.SweepNums = QSpinBox()
        tab2box2Line1.addWidget(self.startNMRLoss)
        tab2box2Line1.addWidget(self.SweepNumsLabel)
        tab2box2Line1.addWidget(self.SweepNums)
        
        tab2box2Line2 = QHBoxLayout()
        self.fitNMRLoss = QPushButton("Fit NMR Loss Data")
        self.firstScanNumLabel = QLabel("First Scan Num.")
        self.firstScan = QSpinBox()
        tab2box2Line2.addWidget(self.fitNMRLoss)
        tab2box2Line2.addWidget(self.firstScanNumLabel)
        tab2box2Line2.addWidget(self.firstScan)
        
        tab2box2Line3 = QHBoxLayout()
        self.showTabel = QPushButton("Show Tabel")
        self.lastScanNumLabel= QLabel("Last Scan Num.")
        self.lastScan = QSpinBox()
        tab2box2Line3.addWidget(self.showTabel)
        tab2box2Line3.addWidget(self.lastScanNumLabel)
        tab2box2Line3.addWidget(self.lastScan)
        
        tab2box2.addLayout(tab2box2Line1)
        tab2box2.addLayout(tab2box2Line2)
        tab2box2.addLayout(tab2box2Line3)
        
        tab2box3 = QVBoxLayout()
        
        tab2box3Line1 = QHBoxLayout()
        self.startPumpRate = QPushButton("Start Pump Rate")
        self.timeIntervalLabel= QLabel("Time Interval")
        self.timeInterval = QSpinBox()
        tab2box3Line1.addWidget(self.startPumpRate)
        tab2box3Line1.addWidget(self.timeIntervalLabel)
        tab2box3Line1.addWidget(self.timeInterval)
        
        tab2box3Line2 = QHBoxLayout()
        self.fitPumpRate = QPushButton("Fit Pump Rate")
        self.firstPumpLabel= QLabel("First Scan Num.")
        self.firstPump = QSpinBox()
        tab2box3Line2.addWidget(self.fitPumpRate)
        tab2box3Line2.addWidget(self.firstPumpLabel)
        tab2box3Line2.addWidget(self.firstPump)
        
        tab2box3Line3 = QHBoxLayout()
        self.rateTabel = QPushButton("Rate Tabel")
        self.lastPumpLabel= QLabel("Last Scan Num.")
        self.lastPump = QSpinBox()
        tab2box3Line3.addWidget(self.rateTabel)
        tab2box3Line3.addWidget(self.lastPumpLabel)
        tab2box3Line3.addWidget(self.lastPump)
        
        tab2box3.addLayout(tab2box3Line1)
        tab2box3.addLayout(tab2box3Line2)
        tab2box3.addLayout(tab2box3Line3)
        
        secondTab.addLayout(tab2box1)
        secondTab.addLayout(tab2box2)
        secondTab.addLayout(tab2box3)
        secondTab.addStretch()
        self.tab2.setLayout(secondTab)
        
        
        #Create Tab 3----------------------------------------------------------
        thirdTab = QVBoxLayout()
        tab3box1 = QVBoxLayout()
        
        tab3box1Line1 = QHBoxLayout()
        self.setMagnetField = QPushButton("Set Field")
        self.newVoltLabel = QLabel("New Voltage")
        self.newVoltage = QDoubleSpinBox()
        self.newVoltage.setSingleStep(.1)
        self.newVoltage.setValue(0)
        print(self.newVoltage.value())
        #self.setMagnetField.clicked.connect(functions.AO_example_nidaqmx)
        self.setMagnetField.clicked.connect(lambda: functions.setMagnetField(self.newVoltage.value()))
        tab3box1Line1.addWidget(self.setMagnetField)
        tab3box1Line1.addWidget(self.newVoltLabel)
        tab3box1Line1.addWidget(self.newVoltage) 
        self.currentVoltLabel = QLabel("Current Voltage" + str(self.currentVoltage))
        tab3box1.addLayout(tab3box1Line1)
        tab3box1.addWidget(self.currentVoltLabel)
        
        tab3box2 = QHBoxLayout()
        self.NMRHistoryTable = QPushButton("NMR History Table")
        self.saveHistoryFile = QPushButton("Save History File")
        tab3box2.addWidget(self.NMRHistoryTable)
        tab3box2.addWidget(self.saveHistoryFile)
        
        tab3box3 = QHBoxLayout()
        self.killWaves = QPushButton("Kill Data Waves")
        self.startLabel = QLabel("Start")
        self.start = QSpinBox()
        self.endLabel = QLabel("End")
        self.end = QSpinBox()
        tab3box3.addWidget(self.killWaves)
        tab3box3.addWidget(self.startLabel)
        tab3box3.addWidget(self.start)
        tab3box3.addWidget(self.endLabel)
        tab3box3.addWidget(self.end)
        
        tab3box4 = QHBoxLayout()
        self.bSweepButton = QPushButton("B-Sweep AFP Panel")
        self.fSweepButton = QPushButton("f-Sweep AFP Panel")
        tab3box4.addWidget(self.bSweepButton)
        tab3box4.addWidget(self.fSweepButton)
        
        tab3box5 = QVBoxLayout()
        tab3box5Line1 = QHBoxLayout()
        tab3box5Line2 = QHBoxLayout()
        self.NFIDInit = QPushButton("NFID Init")
        self.genInit = QPushButton("General Init")
        self.DIOInit = QPushButton("DIO Init")
        self.NIDAQReset = QPushButton("NIDAQ Reset")
        self.NIDAQError = QPushButton("NIDAQ Error")
        tab3box5Line1.addWidget(self.NFIDInit)
        tab3box5Line1.addWidget(self.genInit)
        tab3box5Line2.addWidget(self.DIOInit)
        tab3box5Line2.addWidget(self.NIDAQReset)
        tab3box5Line2.addWidget(self.NIDAQError)
        tab3box5.addLayout(tab3box5Line1)
        tab3box5.addLayout(tab3box5Line2)
        
        tab3box6 = QVBoxLayout()
        tab3box6Line1 = QHBoxLayout()
        tab3box6Line2 = QHBoxLayout()
        self.setDIO = QPushButton("Set DIO Channel")
        self.channelSetLabel= QLabel("Set Channel")
        self.setChannel = QSpinBox()
        self.setValueLabel = QLabel("Value(0/1)")
        self.setVale = QSpinBox()
        self.readDIO = QPushButton("Read DIO Channel")
        self.channelReadLabel= QLabel("Read Channel")
        self.readChannel = QSpinBox()
        self.readChannelValue = QLabel("Read Label is" +str(self.currChannel))
        tab3box6Line1.addWidget(self.setDIO)
        tab3box6Line1.addWidget(self.channelSetLabel)
        tab3box6Line1.addWidget(self.setChannel)
        tab3box6Line1.addWidget(self.setValueLabel)
        tab3box6Line1.addWidget(self.setVale)
        tab3box6Line2.addWidget(self.readDIO)
        tab3box6Line2.addWidget(self.channelReadLabel)
        tab3box6Line2.addWidget(self.readChannel)
        tab3box6Line2.addWidget(self.readChannelValue)
        tab3box6.addLayout(tab3box6Line1)
        tab3box6.addLayout(tab3box6Line2)
        
        tab3box7 = QVBoxLayout()
        tab3box7Line1 = QHBoxLayout()
        tab3box7Line2 = QHBoxLayout()
        tab3box7Line3 = QHBoxLayout()
        
        self.write = QPushButton("Write")
        self.read = QPushButton("Read")
        self.deviceNameLabel = QLabel("Device Name")
        self.deviceName = QLineEdit()
        self.str1Label = QLabel("String")
        self.str1 = QLineEdit()
        self.str2Label= QLabel("String")
        self.str2 = QLineEdit()
        self.responseLabel = QLabel("Response")
        self.response = QLineEdit()
        tab3box7Line1.addWidget(self.write)
        tab3box7Line1.addWidget(self.read)
        tab3box7Line2.addWidget(self.deviceNameLabel)
        tab3box7Line2.addWidget(self.deviceName)
        tab3box7Line2.addWidget(self.str1Label)
        tab3box7Line2.addWidget(self.str1)
        tab3box7Line3.addWidget(self.str2Label)
        tab3box7Line3.addWidget(self.str2)
        tab3box7Line3.addWidget(self.responseLabel)
        tab3box7Line3.addWidget(self.response)
        
        tab3box7.addLayout(tab3box7Line1)
        tab3box7.addLayout(tab3box7Line2)
        tab3box7.addLayout(tab3box7Line3)
        
        thirdTab.addLayout(tab3box1)
        thirdTab.addLayout(tab3box2)
        thirdTab.addLayout(tab3box3)
        thirdTab.addLayout(tab3box4)
        thirdTab.addLayout(tab3box5)
        thirdTab.addLayout(tab3box6)
        thirdTab.addLayout(tab3box7)
        thirdTab.addStretch()
        self.tab3.setLayout(thirdTab)
        
        
        #Create Tab 4----------------------------------------------------------
        fourthTab = QVBoxLayout()
        
        tab4box1 = QVBoxLayout()
        tab4box2 = QVBoxLayout()
        tab4Inputs = QHBoxLayout()
        
        self.NFIDNumLabel =QLabel("NFIDscanNum: " + str(self.Nscans))
        fourthTab.addWidget(self.NFIDNumLabel)
        
        self.warning = QLabel("Make Sure that you change the Field First!!!")
        tab4box1.addWidget(self.warning)
        
        self.QSweep = QPushButton("Q sweep")
        tab4box1.addWidget(self.QSweep)
        
        self.startFreqLabel = QLabel("Q Start Freq.")
        tab4Inputs.addWidget(self.startFreqLabel)
        
        self.QStartFreq = QSpinBox()
        tab4Inputs.addWidget(self.QStartFreq)
        
        self.QStopFreqLabel = QLabel("Q Stop Freq.")
        tab4Inputs.addWidget(self.QStopFreqLabel)
        
        self.QStepFreq = QSpinBox()
        tab4Inputs.addWidget(self.QStepFreq)
        
        self.QStepFreqLabel = QLabel("Q Step Freq.")
        tab4Inputs.addWidget(self.QStepFreqLabel)
        
        self.QStepFreq = QSpinBox()
        tab4Inputs.addWidget(self.QStepFreq)
        tab4box2.addLayout(tab4Inputs)
        
        self.comments = QLabel("See 'LoopInductance()' at the end of the code")
        tab4box2.addWidget(self.comments)
        
        fourthTab.addLayout(tab4box1)
        fourthTab.addLayout(tab4box2)
        fourthTab.addStretch()
        self.tab4.setLayout(fourthTab)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        
    @pyqtSlot()
    def on_click(self):
        print("click")
            
app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())