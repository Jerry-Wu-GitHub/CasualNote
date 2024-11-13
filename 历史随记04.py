import os

os.chdir(r'D:\python\Python作品\★随记')

def unit_conversion(value, current_unit, units, rate):
    '''转换单位

参数：
value：数值 int or float
current_unit：str，value的单位，如'KB'
units：list[str]，如['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'NB', 'DB']
rate：数 int or float，进率，如1024

返回值：
tuple[数:int or float, 单位:str]

例：
>>> unit_conversion(value=241424, current_unit='B', units=['B', 'KB', 'MB'], rate=1024)
(235.765625, 'KB')'''
    while value>=rate and units.index(current_unit)<len(units)-1:
        value/=rate
        current_unit=units[units.index(current_unit)+1]
    while value<1 and units.index(current_unit)>0:
        value*=rate
        current_unit=units[units.index(current_unit)-1]
    return (value,current_unit)

units=['B','KB','MB','GB','TB','PB','EB','ZB','YB','NB','DB']
file = open('history.md', mode = 'w', encoding = 'utf-8')
file.write('# [历史随记](previous)')
for year in sorted(os.listdir('previous'), key = int, reverse = True):
	year_path = os.path.join('previous', year)
	file.write('\n\n## [%s 年](%s)\n\n'%(year, year_path))
	for month in sorted(os.listdir(year_path), key = int, reverse = True):
		month_path = os.path.join('previous', year, month)
		md_file = [f for f in os.listdir(month_path) if os.path.isfile(os.path.join(month_path, f)) and f[-3:] == '.md'][::-1]
		file.write('---\n\n### [%s 月](%s)\n*共%d项*\n\n'%(month, month_path, len(md_file)))
		for date in md_file:
			file_path = os.path.join(month_path, date)
			size = os.stat(file_path).st_size
			size = unit_conversion(value = size, current_unit = 'B', units = units, rate = 1024)
			file.write('- [%s](%s)\n$%s$\n\n'%(date.split('.')[0][5:], file_path, str(round(size[0], 2)) + size[1]))
file.close()

