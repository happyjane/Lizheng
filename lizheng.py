import get
import push

#read the offset from the offset,txt
try:
	with open('offset.txt') as f:
		offset = int(f.read())

except IOError as err:
	print('File error: ' + str(err))

#to avoid the mistake that offset is equal to the biggest id
try:
	#print offset
   	offset = get.getData(offset)
   	with open('offset.txt', 'w') as f:
   		f.write(str(offset))

except IOError as err:
	print('File error: ' + str(err))

except:
	pass

