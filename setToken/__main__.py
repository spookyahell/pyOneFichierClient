import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'1F.t')

if len(sys.argv) == 2:
	the_token = sys.argv[1]
else:
	the_token = input('Token: ')

with open(path,'w') as f:
	f.write(the_token)