import os
from tkinter import *
from tkinter import messagebox
files = [f for f in os.listdir() if f.endswith('.PBG') or f.endswith('.pbg')] # сканер мазаковских файлов
if files == []:
	result = 'Файлов Mazatrol не найдено.'
else:
	result = 'Найдено подходящих файлов Mazatrol: ' + str(len(files))

badfiles = ('.PBG', '.PY', # список того, что пропустит фануковский сканер
	'.MP3', '.FLAC', '.WAV', '.OGG',
	'.JPG', '.JPEG', '.BMP', '.ICO', '.TIFF', '.JPE', '.OXPS', '.PSD', '.PNG', '.GIF',
	'.MPEG', '.MP4', '.WEBM', '.WMA', '.FLV', '.MOV', '3GP', '.AVI', '.VOB', 
	'.EXE', '.RAR', '.ZIP', '.7Z', '.MSI', '.INSTALL', '.APK'
	'.XLS', '.XLSX', '.WPS', '.FRW',
	'.INI', '.CFG', '.DB', '.DAT', '.TMP'
	'.DOC', '.DOCX', '.PDF', '.DJVU', '.FB2', '.EPUB' 
	'.DB', '.LNK', '.URL', '.HTML', 
	'.GP3', '.GP4', '.GP5', '.GPX') 
badfiles2 = []
for i in badfiles: # оно же в нижнем регистре
	i = i.lower()
	badfiles2.append(i) 
badfiles2 = tuple(badfiles2) 

files2 = [f for f in os.listdir() if not f.endswith(badfiles) and not f.endswith(badfiles2)] # сканер фануковских файлов
if 'Thumbs.db' in files2:
	files2.remove('Thumbs.db')
if 'output_mazatrol' in files2:
		files2.remove('output_mazatrol')
if 'output_fanuc' in files2:
		files2.remove('output_fanuc')
f_times = 0
while f_times < 5:
	for i in files2:
		try:
			with open(i, 'r') as e:
				e = e.read(1)
		except(PermissionError):
			print('Из обработки исключена папка: ' + i)
			files2.remove(i)
		except:
			print('ВНИМАНИЕ: Не удалось удалить ' + i + ' из списка обработки.')
	f_times += 1

if files2 == []:
	result2 = 'Файлов Fanuc не найдено.'
else:
	result2 = 'Найдено подходящих файлов Fanuc: ' + str(len(files2))

print('\n'+result+'\n' + result2+'\n' + '_'*80)

err=[]
times = 0

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
		print(fileold, ('{:.>'+symbols+'}').format('не скопирован!'))
		err.append(i) 

def fanuc(self, i): #обработчик фануковских программ
	try:
		dir = os.getcwd()
		with open(i, 'rb') as f:
			text = f.read()
			f.seek(2)
			fileold = f.read(55)
			if b')' not in fileold:
				try:
					fileold.decode()
					print('Файл ' + str(i) +' не содержит названия внутри!')
				except(UnicodeDecodeError):
					print('Файл '+ str(i) + ' не поддерживается!')
			else:
				fileold = fileold.split(b'(')
				fileold = fileold[1].split(b')')
				try:
					fileold = fileold[0].decode()
					fileold = fileold.replace('\\', '-').replace('*', '-').replace('/', '-').strip(' ')
				except:
					print('Файл '+ str(i) + ' не поддерживается!')
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
			print(i, ('{:.>'+symbols2+'}').format('не скопирован!'))
			err.append(i)
	except(PermissionError):
		symbols2 = str(78 - len(i))
		print('Ошибка! В обработку попала папка: '+'"'+str(i)+'"')
		print(i, ('{:.>'+symbols2+'}').format('пропуск папки!'))
		err.append(i)
	except:
		symbols2 = str(78 - len(i))
		print('Неизвестная ошибка при обработке: '+'"'+str(i)+'"')
		print(i, ('{:.>'+symbols2+'}').format('пропуск файла!'))
		err.append(i)

class huita: #кнопка с вызовом мазаковского обработчика
	global err
	errors = ''
	def __init__(self):
		self.btn = Button(fr, 
			text='Переименовать файлы Mazatrol',
			command = self.stmaz, 
			font='Candara 12',
			width=30,
			padx=5, 
			pady=5)
		self.btn.grid(row=5, column=0, rowspan=1, columnspan=1)

	def stmaz(self):
		global err
		global files
		global times
		times = 0
		if files == []:
			messagebox.showerror('Хрен!', 'Нечего переименовывать!')
		else:
			print('{: ^79}'.format('Выбран режим Mazatrol'))
			for i in files:
				mazak(self, i)
			errors = '\n'.join(err)
			print('_'*80)
			print('{: >79}'.format('Принято файлов: ' + str(len(files))))
			print('{: >79}'.format('Обработано файлов: ' + str(times)))
			if errors == '':
				print('{: >79}'.format('Ошибок нет!'))
			else:
				print('Ошибки:\n' + str(errors))
			err = []
			errors = ''
			messagebox.showinfo('Готово!', 'Принято файлов: ' + str(len(files)) + '.' + '\nОбработано файлов: ' + str(times) + '.' + '\nПодробности в терминале.')	

class huita2: #кнопка с вызовом фануковского обработчика
	global err
	errors = ''
	def __init__(self):
		self.btn = Button(fr2, 
			text='Переименовать файлы Fanuc', 
			command = self.stfan,
			font='Candara 12',
			width=30,
			padx=5, 
			pady=5)
		self.btn.grid(row=5, column=1, rowspan=1, columnspan=1)
	def stfan(self):
		global err
		global files2
		global times
		times = 0
		if files2 == []:
			messagebox.showerror('Хрен!', 'Нечего переименовывать!')
		else:
			print('{: ^79}'.format('Выбран режим Fanuc'))
			for i in files2:
				fanuc(self, i)
			errors = '\n'.join(err)
			print('_'*80)
			print('{: >79}'.format('Принято файлов: ' + str(len(files2))))
			print('{: >79}'.format('Обработано файлов: ' + str(times)))
			if errors == '':
				print('{: >79}'.format('Ошибок нет!'))
			else:
				print('Ошибки:\n' + str(errors))
			err = []
			errors = ''
			messagebox.showinfo('Готово!', 'Принято файлов: ' + str(len(files2)) + '.' + '\nОбработано файлов: ' + str(times) + '.' + '\nПодробности в терминале.')

root = Tk()
root.title('Переименовыватель-копир')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4
root.wm_geometry("+%d+%d" % (x, y))
root.resizable(False, False)
wind = Label(root, 
	text='Переименовыватель-копир 3000 ver.0.7 Limited Edition', 
	font='Candara 14')
windtext = Label(root, 
	text='При запуске программа сканирует файлы в папке с собой.\nПри обработке создаются переименованные копии файлов в отдельных папках для каждой стойки.', 
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
	text=result, 
	font='Candara 11',
	bg='white')
wind3 = Label(fr2, 
	text=result2, 
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

obj = huita()
obj2 = huita2()
root.mainloop()
