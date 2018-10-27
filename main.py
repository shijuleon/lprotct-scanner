#!/usr/bin/python

from GUI import Ui_Dialog
from PyQt4 import QtCore, QtGui
import requests, sys, hashlib
from threading import Thread
from Config import Config
import Request

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class doThings(QtGui.QMainWindow):
       	FILE_NAME = ""
	#API_KEY = "fb72b4060671a67d1a28087852e1d77ccb8003bd9d6e1349cf29d42c41ec24e2"
	MD5 = ""

	def doThings(self, Dialog):
            ui.pushButton.clicked.connect(self.getfile)
	    ui.pushButton_2.clicked.connect(self.scan)
	   
	def getfile(self):
            try:
	        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
         '',"")
		ui.textBrowser.append("File selected: %s" % fname)
		self.FILE_NAME = fname
		self.MD5 = self.getMD5(fname)
		ui.textBrowser.append("MD5: %s" % self.MD5)
            except:
                print "Invalid file selection"

	def getMD5(self, fname):
            try:
		with open(fname) as file_to_check:
			data = file_to_check.read()
			md5 = hashlib.md5(data).hexdigest()
			return md5
            except:
                print "Error: Calculating MD5"

	def scanme(self):
		t = Thread(target=scan)
		t.daemon = True
		t.start()

	def scan(self, Dialog):
            fname = self.FILE_NAME
            print fname
	    if fname == "":
	        ui.textBrowser.append("Invalid file")
            else:
                params = { 'params': {'apikey': Config.API_KEY, 'resource': self.MD5 } }
		ui.textBrowser.append("Checking if file is already present in online scanner")
                json_response = Request.requestJSON(0, params)
                #json_response = {'response_code': 0} 
                if json_response['response_code'] == 0:
		    ui.textBrowser.append("File not present in online scanner")
		    ui.textBrowser.append("Uploading file to online scanner")
                    params = { 'params': {'apikey': Config.API_KEY}, 'files': {'file': (str(fname), open(fname, 'rb')) } }
                    
		    print params
                    print params['files']['file']
                    json_response = Request.requestJSON(1, params)
                    ui.textBrowser.append(json_response['verbose_msg'])
                elif json_response['response_code'] == 1:
	            ui.textBrowser.append("File already present in online scanner. Retreiving report.")
		    json_response = Request.requestJSON(2, params)
                    ui.textBrowser.append(json_response['verbose_msg'])
                    ui.textBrowser.append("Report link: %s" % json_response['permalink'])
                    scans = json_response['scans']
	            self.writeToTable(scans)
                elif json_response['response_code'] == -1:
                    ui.textBrowser.append("Error uploading to online scanner")
        			
        def writeToTable(self, scans):
            row = len(scans)
            ui.tableWidget.setRowCount(row)
            anti = []
            results = []
            update = []

	    for key, value in scans.items():
	       	anti.append(key)
	       	results.append(value['detected'])
	       	update.append(value['update'])
            
            final = [anti, results, update]
            print final
            for i in range(0,3):
	       	current = final[i]
                for j in range(0, len(scans)):
		    write = str(current[j])
                    ui.tableWidget.setItem(j, i, QtGui.QTableWidgetItem(write))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	do = doThings()
	do.doThings(Dialog)
	Dialog.show()
	sys.exit(app.exec_())
