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
TABLES = ("php", "asp", "aspx", "jsp", "dir", "file")

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

	def delete_path(self, table, path):
		try:
			self.cursor.execute("DELETE from " + table + " where path='" + path + "'")
			self.conn.commit()
		except Exception, e:
			print e

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


class Window:

	window = None

	def __init__(self):
		self.window()

	def window(self):
		# window
		window = Tk()
		window.title(TITLE)
		window.geometry('800x600') 
		window.resizable(width=False, height=False)
		# menu
		menubar = Menu(window)
		menubar.add_command(label="Setting", command=self.donothing)
		menubar.add_command(label="Setting", command=self.donothing)
		menubar.add_command(label="Setting", command=self.donothing)
		menubar.add_command(label="Setting", command=self.donothing)
		menubar.add_command(label="Setting", command=self.donothing)
		menubar.add_command(label="About", command=self.donothing)
		window.config(menu=menubar)
		# mainloop
		window.mainloop()

	def donothing(self):
	   tkMessageBox.showinfo("Message", "Hello World")

if __name__ == '__main__':
	# scanner = Scanner()
	Window()

	