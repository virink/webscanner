#!/bin/env python
#-*- encoding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import sqlite3
import os
import urllib2
import thread
import Queue
import time


VERSION = "Ver 1.0"
TITLE = "VScanner - WebScanner " + VERSION
Baidu_spider = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
DATABASE = "data.db"
scanlist = []
is_start = False
oknum = 0
queue = None
data = None

class Data:

	conn = None
	cursor = None

	def __init__(self):
		if os.path.exists(DATABASE):
			self.conn = sqlite3.connect(DATABASE)
			self.cursor = self.conn.cursor()

	def create_table(self, table):
		sql = "CREATE TABLE " + table + " (\"Id\" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \"path\" TEXT(512) NOT NULL, \"num\" INTEGER INTEGER NOT NULL DEFAULT 0);"
		self.cursor.execute(sql)

	def drop_table(self, table):
		if table not in TABLES:
			self.cursor.execute("drop table if exists " + table)
		self.conn.commit()

	def select_list(self, table):
		try:
			ruselt = []
			cursor = self.cursor.execute("SELECT path from " + table)
			ruselt = self.cursor.fetchall()
			return ruselt
		except Exception, e:
			print e

	def update_num(self, table, path):
		try:
			self.cursor.execute("UPDATE "+ table + " set num=num+1 where path='" + path + "'")
			self.conn.commit
		except Exception, e:
			print e

	def insert_path(self, table, path):
		try:
			self.cursor.execute("insert into " + table + "(path) values('" + path + "')")
			self.conn.commit()
		except Exception, e:
			print e

	def insert_path_more(self, table, queue):
		try:
			while not queue.empty():
				path = queue.get()
				self.cursor.execute("insert into " + table + "(path) values('" + path + "')")
			self.conn.commit()
		except Exception, e:
			print e

	# def delete_path(self, table, path):
	# 	try:
	# 		self.cursor.execute("DELETE from " + table + " where path='" + path + "'")
	# 		self.conn.commit()
	# 	except Exception, e:
	# 		print e

	def __del__(self):
		if self.cursor or self.conn:
			self.cursor.close()
			self.conn.commit()
			self.conn.close()


def input_txt(name):
	queue = Queue.Queue()
	data = Data()
	f = open(name,'r')
	l = f.readlines()
	for i in l:
		queue.put(i[:-1])
	data.insert_path_more("custom",queue)

def reqhttp(domain):
	timeout = timeVar.get()
	while not q.empty():
		progressVar.set("Progress : "+str(oknum)+"/"+str(num))
		path = q.get()
		url = "%s%s" % (domain, path)
		opener = urllib2.build_opener()
		urllib2.install_opener(opener)
		headers = {} 
		headers['User-Agent'] = Baidu_spider
		request = urllib2.Request(url, headers=headers) 
		try:
			response = urllib2.urlopen(request, timeout=timeout)
			content = response.read()
			if len(content) and response.code is not 200:
				resultlist.insert(END, "Status [%s]  - Path: %s" % (response.code, path))
			response.close()
			oknum += 1
			time.sleep(1)
		except urllib2.HTTPError as e:
			print e.code, path
			pass
	thread.exit_thread()

def startScan(domain):
	for i in xrange(int(threadVar.get())):
		thread.start_new_thread(reqhttp, (domain))

# tk
window = None
num = 0

def window():
	window = Tk()
	window.title(TITLE)
	window.geometry('800x600') 
	window.resizable(width=False, height=False)

	menubar = Menu(window)
	# menu custom
	menubar.add_command(label="Custom", command=showCustom)
	# menu about
	about_menu = Menu(menubar, tearoff=0)
	about_menu.add_command(label="About", command=donothing)
	about_menu.add_command(label="Help", command=donothing)
	menubar.add_cascade(label="About", menu=about_menu)

	# Type Frame
	type_frame = Frame(window, width=800, height=50)
	global phpVar
	phpVar = IntVar()
	global jspVar
	jspVar = IntVar()
	global aspVar
	aspVar = IntVar()
	global aspxVar
	aspxVar = IntVar()
	global dirVar
	dirVar = IntVar()
	global fileVar
	fileVar = IntVar()
	global t403Var
	t403Var = IntVar()
	global t3xxVar
	t3xxVar = IntVar()
	global threadVar
	threadVar = IntVar()
	global timeVar
	timeVar = IntVar()
	threadVar.set(10)
	timeVar.set(3)
	l_thread = Label(type_frame, text="Thread : ")
	s_thread = Spinbox(type_frame, from_=0, to=100, textvariable=threadVar)
	l_time = Label(type_frame, text="Time : ")
	s_time = Spinbox(type_frame, from_=0, to=30, textvariable=timeVar)
	cb_php = Checkbutton(type_frame, text="PHP", variable=phpVar, height=1, width=12)
	cb_jsp = Checkbutton(type_frame, text="JSP", variable=jspVar, height=1, width=12)
	cb_asp = Checkbutton(type_frame, text="ASP", variable=aspVar, height=1, width=12)
	cb_aspx = Checkbutton(type_frame, text="ASP", variable=aspxVar, height=1, width=12)
	cb_dir = Checkbutton(type_frame, text="DIR", variable=dirVar, height=1, width=12)
	cb_file = Checkbutton(type_frame, text="FILE", variable=fileVar, height=1, width=12)
	cb_403 = Checkbutton(type_frame, text="Test 403", variable=t403Var, height=1, width=20)
	cb_3xx = Checkbutton(type_frame, text="Test 3xx", variable=t3xxVar, height=1, width=20)
	l_time.grid(row=0, column=0)
	s_time.grid(row=0, column=1)
	cb_php.grid(row=0, column=2)
	cb_jsp.grid(row=0, column=3)
	cb_asp.grid(row=0, column=4)
	cb_403.grid(row=0, column=5)
	l_thread.grid(row=1, column=0)
	s_thread.grid(row=1, column=1)
	cb_aspx.grid(row=1, column=2)
	cb_dir.grid(row=1, column=3)
	cb_file.grid(row=1, column=4)
	cb_3xx.grid(row=1, column=5)
	type_frame.pack()

	# Target Frame
	global domainVar
	domainVar = StringVar()
	domainVar.set('www.baidu.com')
	target_frame = Frame(window, width=800, height=2)
	l_domain = Label(target_frame, text="Domain : ")
	e_domain = Entry(target_frame, bd =2, width=80, textvariable=domainVar)
	btn_start = Button(target_frame, text ="Start", width=12, command=goScan)
	l_domain.grid(row=0, column=0)
	e_domain.grid(row=0, column=1)
	btn_start.grid(row=0, column=2)
	target_frame.pack()

	# List Frame
	list_frame = Frame(window, width=800, height=20)
	global infoVar
	global progressVar
	infoVar = StringVar()
	progressVar = StringVar()
	infoVar.set("Infomation : Ready...")
	progressVar.set("Progress : 0/0")
	l_info = Label(list_frame, textvariable=infoVar)
	l_progress = Label(list_frame, textvariable=progressVar)
	resultlist = Listbox(list_frame, width=100, height=26, selectmode=SINGLE)
	l_info.grid(row=0, column=0)
	l_progress.grid(row=0, column=1)
	resultlist.grid(row=1, column=0, columnspan=2)
	list_frame.pack()

	# mainloop & config menu
	window.config(menu=menubar)
	window.mainloop()

def donothing():
	tkMessageBox.showinfo("Message", "Do nothing")

def goScan():
	global num
	global scanlist
	is_start = True
	infoVar.set("Infomation : Staring...")
	resultlist = None
	data = Data()
	if phpVar.get():
		slist = data.select_list('php')
		num += len(slist)
		scanlist += slist
	if jspVar.get():
		slist = data.select_list('jsp')
		num += len(slist)
		scanlist += slist
	if aspVar.get():
		slist = data.select_list('asp')
		num += len(slist)
		scanlist += slist
	if aspxVar.get():
		slist = data.select_list('aspx')
		num += len(slist)
		scanlist += slist
	if dirVar.get():
		slist = data.select_list('dir')
		num += len(slist)
		scanlist += slist
	if fileVar.get():
		slist = data.select_list('file')
		num += len(slist)
		scanlist += slist
	progressVar.set("Progress : 0/"+str(num))
	global domainVar
	startScan(domainVar.get())
	

def showCustom():
	winCustom = Toplevel(width=600, height=600)
	winCustom.title("Manage Yourself Dictionary")
	winCustom.mainloop()

def showAbout():
   tkMessageBox.showinfo("About", "About\r\nAbout")

def showHelp():
   tkMessageBox.showinfo("Help", "Help\r\Help")

if __name__ == '__main__':
	queue = Queue.Queue()
	window()