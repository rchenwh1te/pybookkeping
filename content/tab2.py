import PySimpleGUI as sg
import sqlite3
import os

sg.theme('LightGrey3')

tree = sg.TreeData()

accico = b'''
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAPElEQVQ4jWNgQAX/icA4AV5JYsB/
NDbJLvmPRpPlgvloBtHfBTB6Nq1dMGoArQyASVBkAMUuQHcJwYQEABxMTO+JsI9+AAAAAElFTkSu
QmCC
'''

dbdir = os.getcwd()

if not os.path.isdir(dbdir+'/data'):
	os.mkdir(dbdir+'/data')

dbdir += '/data'
conn = sqlite3.connect(dbdir+'/database.db')

sql = conn.cursor()

sql.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Accounts' ''')

if sql.fetchone()[0]==1:
	pass
else:
	sql.execute('''CREATE TABLE "Accounts" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Parent"	TEXT,
	"Value"	TEXT,
	"Name" TEXT,
	"Vals"	TEXT
	);''')
	sql.execute('''INSERT INTO Accounts (Parent,Name,Value,Vals)VALUES('','All','0','Main')''')
	conn.commit()

#bottom = [sg.Button('Remove'),sg.Button('Propertries')]
right_click_menu = ['&Right', ['Add Account',['Income','Outcome'], 'Delete', 'Rename...', '---', 'Properties','---','Refresh']]

tab = [[sg.Tree(data=tree,
	headings=['Type','Balance'],
	auto_size_columns=True,
	num_rows=21,
	col0_width=30,
	key='tree',
	show_expanded=True,
	right_click_menu=right_click_menu,
	enable_events = True)]]
	
def AddAccount(t,sql=sql,conn=conn):
	sql.execute('SELECT "name" FROM Accounts')
	result = sql.fetchall()

	textCol = [[sg.Text('Account name:')],
	[sg.Text('Account parent:')],
	[sg.Text('Sum:')]]
	inCol = [[sg.In(key='-NAME-')],
	[sg.Combo(result,key='-CBX-')],
	[sg.In(key='-SUM-')]]
	acc_layout = [[sg.Column(textCol),sg.Column(inCol)],[sg.Button('OK'),sg.Button('Cancel')]]
	newAccWin = sg.Window('New Account',acc_layout)
	while True:
		eve1,val1 = newAccWin.read()
		if eve1 == 'Cancel' or eve1 == sg.WIN_CLOSED:
			newAccWin.close()
			break
		
		elif eve1 == 'OK':
			temp = list(val1['-CBX-'])
			parent = temp[0]
			sql.execute('SELECT ID FROM Accounts WHERE name="'+parent+'"')
			temp = sql.fetchall()
			temp = [x[0] for x in temp]
			result = str(temp[0])
			
			sql.execute('''INSERT INTO Accounts (Parent,Name,Value,Vals)VALUES("''' + result + '''","''' + val1['-NAME-'] + '''","''' + val1['-SUM-'] + '''","''' + t + '''")''')
			conn.commit()
			newAccWin.close()
			
def DeleteAccount(acc,sql=sql):
	sql.execute('DELETE FROM Accounts WHERE ID="'+acc+'"')
	
def update_tree(window):
	accounts = None
	accounts = sg.TreeData()
	
	sql.execute('SELECT * FROM Accounts')
	result = sql.fetchall()
	#print(result)
	for key,parent,val,name,kind in result:
		accounts.Insert(str(parent),str(key),name,[kind,val],icon=accico)
	window.Element('tree').Update(accounts)
