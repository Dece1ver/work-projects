import os
files = [f for f in os.listdir() if f.endswith('.PBG')]
if files == []:
	print('{: ^79}'.format('НЕТ ПОДХОДЯЩИХ ФАЙЛОВ!'))
print('Найдено подходящих файлов: ' + str(len(files)))
print('Программа сама обработает все файлы и выдаст результат.\nЕсли программа закрылась в процессе, значит произошла ошибка!\n(Скрипт обрабатывает все файлы .PBG в папке с собой.)')
input('{: >79}'.format('Enter чтобы продолжить.'))
times = 0
err = []
def rename(i):
	dir = os.getcwd()
	with open(i, 'rb') as f:
		text = f.read()
		f.seek(80)
		fileold = f.read(30)
		fileold = fileold.rstrip(b'\x00').decode()
		fileold = fileold.replace('\\', '-').replace('*', '-').replace('/', '-').strip(' ') + '.PBG'
	symbols = str(78 - len(fileold))
	try:
		os.mkdir('Output')
	except:
		pass
	try:
		os.chdir('Output')
		with open(fileold, 'wb') as filenew:
			filenew.write(text)
		os.chdir(dir)
		print(fileold, ('{:.>'+symbols+'}').format('скопирован!'))
		global times
		times += 1
	except:
		os.chdir(dir)
		print(fileold, ('{:.>'+symbols+'}').format('НЕ СКОПИРОВАН!'))
		err.append(i)

for i in files:
	rename(i)
print('_'*80)
print('{: >79}'.format('Ошибки: '  + str(err)))
print('{: >79}'.format('Принято файлов: ' + str(len(files))))
print('{: >79}'.format('Обработано файлов: ' + str(times)))
print('')
input('{: >79}'.format('Enter чтобы закрыть.'))