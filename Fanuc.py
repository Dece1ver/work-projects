import os

files = [f for f in os.listdir() if not f.endswith('.py')]
if 'output' in files:
	files.remove('output')
if files == []:
	print('{: ^79}'.format('НЕТ ПОДХОДЯЩИХ ФАЙЛОВ!'))
print('Найдено подходящих файлов: ' + str(len(files)))
print('Программа сама обработает все файлы и выдаст результат.\nЕсли программа закрылась в процессе, значит произошла ошибка!')
print('_'*80)
print('В данной папке не должно быть ничего кроме: \n * Управляющих программ\n * Этого скрипта\n * папки "output" (Не обязательно).')
input('{: >79}'.format('Enter чтобы продолжить.'))
times = 0
err = []

def rename(i):
	try:
		dir = os.getcwd()
		with open(i, 'rb') as f:
			text = f.read()
			f.seek(8)
			fileold = f.read(35)
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
			os.mkdir('output')
		except:
			pass
		try:
			os.chdir('output')
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

for i in files:
	rename(i)
print('_'*80)
print('{: >79}'.format('Ошибки: '  + str(err)))
print('{: >79}'.format('Принято файлов: ' + str(len(files))))
print('{: >79}'.format('Обработано файлов: ' + str(times)))
print('')
input('{: >79}'.format('Enter чтобы закрыть.'))
