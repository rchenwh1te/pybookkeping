import PySimpleGUI as sg
import sqlite3
import os

sg.theme('LightGrey3')

dbdir = os.getcwd()

if not os.path.isdir(dbdir+'/data'):
	os.mkdir(dbdir+'/data')

dbdir += '/data'
conn = sqlite3.connect(dbdir+'/database.db')

sql = conn.cursor()

sql.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Transactions' ''')

if sql.fetchone()[0]==1:
	pass
else:
	sql.execute('''CREATE TABLE "Transactions" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Date"	TEXT,
	"InOut" TEXT,
	"Account"	TEXT,
	"Description"	TEXT,
	"Status"	TEXT,
	"VATRate"	TEXT,
	"Amount"	NUM,
	"VAT"	NUM,
	"Net"	NUM,
	"Total"	NUM
); ''')

sql.execute('''SELECT * FROM Transactions''')
	
result = sql.fetchall()
control = []
data = []
data = [list(i) for i in result]
if data == control:
	data = [[]]
headers = ['Date','In\Out','Account','Description','Status','VAT Rate','Amount','VAT','Net','Total']

if len(data[0]) < len(headers):
	data[0] = ['' for i in range(len(headers))]

tab = [sg.Table(values=data,
headings=headers,
auto_size_columns=True,
justification='center',
num_rows=32,
alternating_row_color='lightblue',
key='table',
display_row_numbers=False)]
