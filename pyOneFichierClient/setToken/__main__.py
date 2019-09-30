import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'1F.t')

if len(sys.argv) == 2:
	the_token = sys.argv[1]
else:
	try:
		the_token = input('Token: ')
	except KeyboardInterrupt:
		try:
			the_token = input('\nToken, last chance: ')
		except KeyboardInterrupt:
			print()
			sys.exit(1)
		
		

with open(path,'w') as f:
	f.write(the_token)