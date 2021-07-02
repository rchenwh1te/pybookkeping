import PySimpleGUI as sg
import sqlite3
import os

sg.theme('LightGrey3')

'''
Date
In
Account
Description
Status
VAT Rate
Amount
VAT
Net
Total
'''

dbdir = os.getcwd()

if not os.path.isdir(dbdir+'/data'):
	os.mkdir(dbdir+'/data')

dbdir += '/data'
conn = sqlite3.connect(dbdir+'/database.db')

sql = conn.cursor()

sql.execute('''SELECT * FROM Transactions WHERE InOut="Out"''')
control = []
result = [sql.fetchall()]
data = [list(i) for i in result[0]]
if data == control:
	data = [[]]
	
headers = ['Serial No.','Date','In\Out','Account','Description','Status','VAT Rate','Amount','VAT','Net','Total']

while len(data[0]) < len(headers):
	data[0].append('')

outtable = [[sg.Table(values=data,
headings=headers,
auto_size_columns=True,
justification='center',
num_rows=25,
alternating_row_color='lightblue',
key='outtable',
display_row_numbers=False)]]

textcol = [[sg.Text('Date:')],
[sg.Text('Account:')],
[sg.Text('Description:')],
[sg.Text('Status:')],
[sg.Text('Amount:')],
[sg.Text('VAT Rate:')]]

incol = [[sg.In(key='-OUTDATE-'), sg.CalendarButton('Pick Date')],
[sg.In(key='outacc')],
[sg.In(key='outdesc')],
[sg.In(key='outstat')],
[sg.In(key='outamount')],
[sg.In(key='outvat'),sg.T('%'),sg.Button('Add outgoing transaction')]]

form = [[sg.Column(textcol),sg.Column(incol)]]

right = [sg.Column(form)]
left = [sg.Column(outtable)]

tab = [right,left]

def add(window,values,sql=sql,conn=conn):
	control = []
	date = values['-OUTDATE-'].split(' ')[0]
	account = values['outacc']
	sql.execute('SELECT * FROM Accounts WHERE name="'+account+'"')
	result = sql.fetchall()
	if len(result) < 1:
		sg.popup_error('No account "'+account+'".')
	else:
		description = values['outdesc']
		status = values['outstat']
		amount = values['outamount']
		vatRate = values['outvat']
		vat = float(float(amount)*float(vatRate)/100)
		net = float(amount)-vat
		sql.execute("INSERT INTO Transactions (DATE, InOut, Account, Description, Status, VATRate, Amount, VAT, NET, Total) VALUES ('"+str(date)+"','Out','"+str(account)+"','"+str(description)+"','"+str(status)+"','"+str(vatRate)+"','"+str(amount)+"','"+str(vat)+"','"+str(net)+"','"+str(amount)+"')")
		conn.commit()
		#Refresh immediately
		sql.execute('''SELECT * FROM Transactions WHERE InOut="Out"''')
		result = [sql.fetchall()]
		data = [list(i) for i in result[0]]
		#Check if there is no data avilable
		if data == control:
			data = [[]]

		while len(data[0]) < len(headers):
			data[0].append('')
			
		window['outtable'].Update(values=data)
