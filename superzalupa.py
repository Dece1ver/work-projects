import os
from tkinter import *
from tkinter import messagebox

files = [f for f in os.listdir() if f.endswith('.PBG') or f.endswith('.pbg')]
print('\nНайдено подходящих файлов Mazatrol: ' + str(len(files)))

badfiles = ('.PBG', '.pbg', '.PY', '.py', '.mp3', '.MP3', '.jpg', '.JPG', '.jpeg', '.JPEG', '.mpeg', '.MPEG', '.mp4', '.MP4', '.webm', '.WEBM', '.bmp', '.BMP')
files2 = [f for f in os.listdir() if not f.endswith(badfiles)]
if 'output_mazatrol' in files2:
	files2.remove('output_mazatrol')
if 'output_fanuc' in files2:
	files2.remove('output_fanuc')

print('Найдено подходящих файлов Fanuc: ' + str(len(files2)))
print('_'*80)

times = 0
err = []

def mazak(self, i): #обработчик мазаковских программ
	dir = os.getcwd()
	with open(i, 'rb') as f:
		text = f.read()
		f.seek(80)
		fileold = f.read(32)
		fileold = fileold.rstrip(b'\x00').decode()
		fileold = fileold.replace('\\', '-').replace('*', '-').replace('/', '-').strip(' ') + '.PBG'
	symbols = str(78 - len(fileold))
	try:
		os.mkdir('output_mazatrol')
	except:
		pass
	try:
		os.chdir('output_mazatrol')
		with open(fileold, 'wb') as filenew:
			filenew.write(text)
		os.chdir(dir)
		print(fileold, ('{:.>'+symbols+'}').format('скопирован!'))
		global times
		times += 1
	except:
		os.chdir(dir)
		print(fileold, ('{:.>'+symbols+'}').format('ошибка!'))
		err.append(i) 

def fanuc(self, i): #обработчик фануковских программ
	try:
		if 'output_mazatrol' in files2:
			files2.remove('output_mazatrol')
		if 'output_fanuc' in files2:
			files2.remove('output_fanuc')
		dir = os.getcwd()
		with open(i, 'rb') as f:
			text = f.read()
			f.seek(8)
			fileold = f.read(40)
			if b')' not in fileold:
				try:
					fileold.decode()
					print('Файл ' + str(i) +' не содержит названия внутри!')
				except(UnicodeDecodeError):
					print('Файл '+ str(i) + ' не поддерживается!')
			else:
				fileold = fileold.split(b')')
				fileold = fileold[0].decode()
				fileold = fileold.replace('\\', '-').replace('*', '-').replace('/', '-').strip(' ')
		symbols = str(78 - len(fileold))
		symbols2 = str(78 - len(i))
		try:
			os.mkdir('output_fanuc')
		except:
			pass
		try:
			os.chdir('output_fanuc')
			with open(fileold, 'wb') as filenew:
				filenew.write(text)
			os.chdir(dir)
			print(fileold, ('{:.>'+symbols+'}').format('скопирован!'))
			global times
			times += 1
		except:
			os.chdir(dir)
			print(i, ('{:.>'+symbols2+'}').format('ошибка!'))
			err.append(i)
	except(PermissionError):
		symbols2 = str(78 - len(i))
		print('Ошибка! В директории присутствует лишняя папка: '+'"'+str(i)+'"')
		print(i, ('{:.>'+symbols2+'}').format('ошибка!'))
		err.append(i)
		pass 
		


root = Tk()
root.title('ПЕРЕИМЕНОВЫВАТЕЛЬ-КОПИР')
#root.geometry('580x295')
root.resizable(False, False)
wind = Label(root, 
	text='Переименовыватель-копир 3000 ver.0.4', 
	font='Candara 14')
windtext = Label(root, 
	text='Программа сама сканирует при запуске файлы в папке с собой,\nПри обработке создаются переименованные копии файлов в отдельных папках для каждой стойки.', 
	font='Candara 10')

fr = Frame(root, 
	relief=GROOVE,
	bg='white', 
	bd=5)
fr2 = Frame(root, 
	relief=GROOVE,
	bg='white', 
	bd=5)

wind2 = Label(fr, 
	text=('Найдено подходящих файлов Mazatrol: ' + str(len(files))), 
	font='Candara 11',
	bg='white')
wind3 = Label(fr2, 
	text=('Найдено подходящих файлов Fanuc: ' + str(len(files2))), 
	font='Candara 11',
	bg='white')
lb = Listbox(fr, width=40)
for i in files:
	lb.insert(END, i)

lb2 = Listbox(fr2, width=40)
for i in files2:
	lb2.insert(END, i)

wind.grid(row=0, column=0, columnspan=2)
windtext.grid(row=1, column=0, columnspan=2)
fr.grid(row=2, column=0, rowspan=3, columnspan=1)
fr2.grid(row=2, column=1, rowspan=3, columnspan=1)
wind2.grid(row=3, column=0, rowspan=1, columnspan=1)
wind3.grid(row=3, column=1, rowspan=1, columnspan=1)
lb.grid(row=4, column=0, rowspan=1, columnspan=1)
lb2.grid(row=4, column=1, rowspan=1, columnspan=1)

class huita: #кнопка с вызовом мазаковской хуйни
	global err
	def __init__(self):
		self.btn = Button(fr, 
			text='Переименовыватель Mazatrol',
			command = self.stmaz, 
			font='Candara 12',
			width=30,
			padx=5, 
			pady=5)
		self.btn.grid(row=5, column=0, rowspan=1, columnspan=1)

	def stmaz(self):
		global err
		global times
		times =  0
		global files
		if files == []:
			messagebox.showerror('Хрен!', 'Нечего переименовывать!')
		else:
			print('{: ^79}'.format('Выбран режим Mazatrol'))
			for i in files:
				mazak(self, i)
			print('_'*80)
			print('{: >79}'.format('Ошибки: '  + str(err)))
			print('{: >79}'.format('Принято файлов: ' + str(len(files))))
			print('{: >79}'.format('Обработано файлов: ' + str(times)))
			err = []
			messagebox.showinfo('Готово!', 'Принято файлов: ' + str(len(files)) + '.' + '\nОбработано файлов: ' + str(times) + '.' + '\nПодробности в терминале.')	

class huita2: #кнопка с вызовом фануковской хуйни
	global err
	def __init__(self):
		self.btn = Button(fr2, 
			text='Переименовыватель Fanuc', 
			command = self.stfan,
			font='Candara 12',
			width=30,
			padx=5, 
			pady=5)
		self.btn.grid(row=5, column=1, rowspan=1, columnspan=1)
	def stfan(self):
		global err
		global times
		global files2
		times =  0
		if files2 == []:
			messagebox.showerror('Хрен!', 'Нечего переименовывать!')
		else:
			print('{: ^79}'.format('Выбран режим Fanuc'))
			for i in files2:
				fanuc(self, i)
			print('_'*80)
			print('{: >79}'.format('Ошибки: '  + str(err)))
			print('{: >79}'.format('Принято файлов: ' + str(len(files2))))
			print('{: >79}'.format('Обработано файлов: ' + str(times)))
			err = []
			messagebox.showinfo('Готово!', 'Принято файлов: ' + str(len(files2)) + '.' + '\nОбработано файлов: ' + str(times) + '.' + '\nПодробности в терминале.')

obj = huita()
obj2 = huita2()
root.mainloop()
