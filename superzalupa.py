import os
from tkinter import *
from tkinter import messagebox

files = [f for f in os.listdir() if f.endswith('.PBG')]
badfiles = ('.PBG', '.pbg', '.PY', '.py', '.mp3', '.MP3', '.jpg', '.JPG', '.jpeg', '.JPEG', '.mpeg', '.MPEG', '.mp4', '.MP4', '.webm', '.WEBM', '.bmp', '.BMP')
print('\nНайдено подходящих файлов Mazatrol: ' + str(len(files)))
files2 = [f for f in os.listdir() if not f.endswith('.py') and not f.endswith(badfiles)]
if 'output_mazatrol' in files2:
	files2.remove('output_mazatrol')
if 'output_fanuc' in files2:
	files2.remove('output_fanuc')
print('Найдено подходящих файлов Fanuc: ' + str(len(files2)))
print('_'*80)
times = 0
err = []

def mazak(self, i):
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
		print(fileold, ('{:.>'+symbols+'}').format('не скопирован'))
		err.append(i)

def fanuc(self, i):
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
			print(i, ('{:.>'+symbols2+'}').format('НЕ СКОПИРОВАН!'))
			err.append(i)
	except(PermissionError):
		symbols2 = str(78 - len(i))
		print('Ошибка! В директории присутствует лишняя папка: '+'"'+str(i)+'"')
		print(i, ('{:.>'+symbols2+'}').format('НЕ СКОПИРОВАН!'))
		err.append(i)
		pass
		
class huita:
	def __init__(self):
		self.btn = Button(root, text='{: ^79}'.format('Переименовыватель Mazatrol'), font='Candara 12')
		self.btn.bind('<Button-1>', self.stmaz)
		self.btn.pack()

	def stmaz(self, event):
		print('{: ^79}'.format('Выбран режим Mazatrol'))
		global times
		times =  0
		global files
		for i in files:
			mazak(self, i)
		print('_'*80)
		print('{: >79}'.format('Ошибки: '  + str(err)))
		print('{: >79}'.format('Принято файлов: ' + str(len(files))))
		print('{: >79}'.format('Обработано файлов: ' + str(times)))
		messagebox.showinfo('Успех!', 'Успешно скопировано ' + str(times) + ' файлов из принятых ' + str(len(files)) + '.' + '\nПодробности в терминале.')
		
class huita2:
	def __init__(self):
		self.btn = Button(root, text='{: ^79}'.format('Переименовыватель Fanuc'), font='Candara 12')
		self.btn.bind('<Button-1>', self.stfan)
		self.btn.pack()
	def stfan(self, event):
		print('{: ^79}'.format('Выбран режим Fanuc'))
		global times
		times =  0
		global files2
		for i in files2:
			fanuc(self, i)
		print('_'*80)
		print('{: >79}'.format('Ошибки: '  + str(err)))
		print('{: >79}'.format('Принято файлов: ' + str(len(files2))))
		print('{: >79}'.format('Обработано файлов: ' + str(times)))
		messagebox.showinfo('Успех!', 'Успешно скопировано ' + str(times) + ' файлов из принятых ' + str(len(files2)) + '.' + '\nПодробности в терминале.')
		
root = Tk()
root.title('ПЕРЕИМЕНОВЫВАТЕЛЬ-КОПИР')
root.geometry('320x135')
root.resizable(False, False)
root['bg']='pink'
wind = Label(root, text='{: ^79}'.format('Переименовыватель-копир 3000 версия 0.00003'), font='Candara 10')
wind2 = Label(root, text=('Найдено подходящих файлов Mazatrol: ' + str(len(files))), font='Candara 11', bg='pink')
wind3 = Label(root, text=('Найдено подходящих файлов Fanuc: ' + str(len(files2))), font='Candara 11', bg='pink')
wind.pack()
wind2.pack()
wind3.pack()
obj = huita()
obj2 = huita2()
root.mainloop()