import PySimpleGUI as sg
import sqlite3
import content

sg.theme('LightGrey3')

tab1_layout = [list(content.tab1.tab)]

tab2_layout = list(content.tab2.tab)

tab3_layout = list(content.tab3.tab)

tab4_layout = list(content.tab4.tab)

group = [[sg.Tab('Summary',tab1_layout)],
[sg.Tab('Accounts',tab2_layout)],
[sg.Tab('Income',tab3_layout)],
[sg.Tab('Outgoings',tab4_layout)]
]

layout = [[sg.TabGroup(group)],[#sg.Button('Export data'),
sg.Button('Close')]]

window = sg.Window('Bookkeeping',layout)
window.Finalize()
content.tab2.update_tree(window)
while True:
	event,values = window.read()
	if event == 'Close' or event == sg.WIN_CLOSED:
		break
	elif event == 'Income':
		content.tab2.AddAccount(t='in')
		content.tab2.update_tree(window)
	elif event == 'Outcome':
		content.tab2.AddAccount(t='out')
		content.tab2.update_tree(window)
	elif event == 'Delete':
		sel=str(window.Element('tree').SelectedRows[0])
		content.tab2.DeleteAccount(acc=sel)
		content.tab2.update_tree(window)
	elif event == 'Refresh':
		content.tab2.update_tree(window)
	elif event == 'Pick Date':
		d = sg.popup_get_date()
		for month,day,year in date:
			date = day+'/'+month+'/'+year
		window['-DATE-'].Update(date)
	elif event == 'Add incoming transaction':
		content.tab3.add(window=window,values=values)
	elif event == 'Add outgoing transaction':
		content.tab4.add(window=window,values=values)
	window.refresh()
