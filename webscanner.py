#!/bin/env python
#-*- encoding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import sqlite3
import os
import urllib2
import threading
import Queue
import time


VERSION = "Ver 1.0"
TITLE = "VScanner - WebScanner " + VERSION
Baidu_spider = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
DATABASE = "data.db"
scanlist = []
is_start = False
# tk
window = None

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

	def select_list(self, cloumn, table):
		try:
			ruselt = []
			cursor = self.cursor.execute("SELECT " + cloumn + " from " + table)
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

class Scanner:

	queue = None
	data = None

	def __init__(self):
		self.queue = Queue.Queue()

	def load_dict(self):
		pass

	def input_txt(self, name):
		queue = Queue.Queue()
		data = Data()
		f = open(name+'.txt','r')
		l = f.readlines()
		for i in l:
			queue.put(i[:-1])
		if name not in TABLES:
			name = "custom"
		data.insert_path_more(name,queue)

	def scanhttp(self, domain):
		while not q.empty():
			path = q.get()
			url = "%s%s" % (domain, path)
			opener = urllib2.build_opener()
			urllib2.install_opener(opener)
			headers = {} 
			headers['User-Agent'] = Baidu_spider
			request = urllib2.Request(url, headers=headers) 
			try:
				response = urllib2.urlopen(request)
				content = response.read()
				if len(content):
					print "Status [%s]  - path: %s" % (response.code, path)
				response.close()
				time.sleep(1)
			except urllib2.HTTPError as e:
				print e.code, path
				pass


def window():
	window = Tk()
	window.title(TITLE)
	window.geometry('800x600') 
	window.resizable(width=False, height=False)

	menubar = Menu(window)
	# menu setting
	# setting_menu = Menu(menubar, tearoff=0)
	# setting_menu.add_command(label="Setting", command=donothing)
	# menubar.add_cascade(label="Setting", menu=setting_menu)
	# menu custom
	menubar.add_command(label="Custom", command=showCustom)
	# menu about
	about_menu = Menu(menubar, tearoff=0)
	about_menu.add_command(label="About", command=donothing)
	about_menu.add_command(label="Help", command=donothing)
	menubar.add_cascade(label="About", menu=about_menu)

	# Type Frame
	Type_frame = Frame(window, width=800, height=50)
	phpVar = IntVar()
	jspVar = IntVar()
	aspVar = IntVar()
	aspxVar = IntVar()
	dirVar = IntVar()
	fileVar = IntVar()
	cb_php = Checkbutton(Type_frame, text = "PHP", variable = phpVar, height=5, width = 10)
	cb_jsp = Checkbutton(Type_frame, text = "JSP", variable = jspVar, height=5, width = 10)
	cb_asp = Checkbutton(Type_frame, text = "ASP", variable = aspVar, height=5, width = 10)
	cb_aspx = Checkbutton(Type_frame, text = "ASP", variable = aspxVar, height=5, width = 10)
	cb_dir = Checkbutton(Type_frame, text = "DIR", variable = dirVar, height=5, width = 10)
	cb_file = Checkbutton(Type_frame, text = "FILE", variable = fileVar, height=5, width = 10)
	cb_php.pack(side=LEFT)
	cb_jsp.pack(side=LEFT)
	cb_asp.pack(side=LEFT)
	cb_aspx.pack(side=LEFT)
	cb_dir.pack(side=LEFT)
	cb_file.pack(side=LEFT)
	Type_frame.pack()

	# Target Frame
	target_frame = Frame(window, width=800, height=50)
	l_domain = Label(target_frame, text="Domain : ")
	e_domain = Entry(target_frame, bd =2, width=80)
	btn_start = Button(target_frame, text ="Start", width=15, command=donothing)
	l_domain.pack(side = LEFT)
	e_domain.pack( side = LEFT)
	btn_start.pack()
	target_frame.pack()

	# List Frame

	# mainloop & config menu
	window.config(menu=menubar)
	window.mainloop()

def donothing():
   tkMessageBox.showinfo("Message", "Do nothing")

def showCustom():
	winCustom = Toplevel(width=600, height=600)
	winCustom.title("Manage Yourself Dictionary")
	winCustom.mainloop()

def showAbout():
   tkMessageBox.showinfo("About", "About\r\nAbout")

def showHelp():
   tkMessageBox.showinfo("Help", "Help\r\Help")

if __name__ == '__main__':
	# scanner = Scanner()
	window()