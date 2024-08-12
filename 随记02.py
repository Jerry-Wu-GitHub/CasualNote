import os, datetime
from shutil import copyfile

def tuple(obj):
	if type(obj) == datetime.date:
		return (obj.year, obj.month, obj.day)
	elif type(obj) == datetime.datetime:
		return (obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second)
	else:
		return tuple(obj)


def recreate_note():
	note_path = 'note.md'
	copyfile(r'data\FixedHeader.md', note_path)
	return note_path

def save(note_path, the_day:datetime.date):
	(year, month, day) = tuple(the_day)
	dirpath = r'previous\%d\%d'%(year, month)
	if not os.path.isdir(dirpath):
		os.makedirs(dirpath)

	with open(note_path, mode = 'r', encoding = 'utf-8') as file:
		note_content = file.readlines()

	with open(dirpath + '\\' + str(the_day)+'.md', mode = 'w', encoding = 'utf-8') as file:
		is_header = True
		for i in range(1, len(note_content)):
			if is_header:
				if note_content[i-1][-4:] == '---\n':
					is_header = False
			else:
				file.write(note_content[i])


if not os.path.isfile(r'data\SeparationTime.txt'): # SeparationTime.txt 不存在
	with open(r'data\SeparationTime.txt', mode = 'w', encoding = 'utf-8') as file:
		file.write('0:0:0')

if not os.path.isfile(r'data\FixedHeader.md'): # FixedHeader.md 不存在
	file = open(r'data\FixedHeader.md', mode = 'w', encoding = 'utf-8')
	file.close()

if not os.path.isfile('note.md'): # note.md 不存在
	note_path = recreate_note()
else:
	note_path = 'note.md'


today = datetime.date.today()
now = datetime.datetime.today()
with open(r'data\SeparationTime.txt', mode = 'r', encoding = 'utf-8') as file:
	separation_time = datetime.datetime(*tuple(today), *map(int, file.readlines()[0].split(':')))
noon_of_today = datetime.datetime(*tuple(today), 12, 0, 0)
if os.path.isfile(r'data\LastStorageTime.txt'):
	with open(r'data\LastStorageTime.txt', mode = 'r', encoding = 'utf-8') as file:
		last_storage_time = datetime.datetime(*map(int, file.readlines()[0].split(' ')))
else:
	last_storage_time = datetime.datetime(*tuple(today), 0, 0, 0) - datetime.timedelta(days = 1)

print(last_storage_time)
the_day = datetime.date(*(tuple(last_storage_time)[:3]))
the_day += datetime.timedelta(days = int(separation_time > noon_of_today))
print(the_day)

if last_storage_time < separation_time and now > separation_time:
	save(note_path, the_day)
	with open(r'data\LastStorageTime.txt', mode = 'w', encoding = 'utf-8') as file:
		file.write(' '.join(map(str, tuple(now))))
	recreate_note()
