'''Interactive demo for OneFichierClient
'''

#Get the tokenfilename (relying on OS)
import sys
import platform
from os import environ
system = platform.system()
BASE_FNAME = '1F.t'
if system == 'Windows':
	token_path = environ['USERPROFILE'] + '\\' + BASE_FNAME
elif system == 'Linux':
	token_path = environ['HOME'] + '/' + BASE_FNAME
else:
	print(f'Your system ({system}) is currently not supported. Sorry.')
	sys.exit(1)

try:
	with open(token_path) as f:
		x = f.read().strip()
		
	from .OneFichierAPI import FichierClient
except FileNotFoundError:
	print(f'Ooops! - ERR - You seem to be missing the token file ({token_path!r}).\nYou can set it by running >python3 -m pyOneFichierClient.setToken later or by confirming the next question with yes.\nYou will need to run the command again once set.')
	x = input('Set token now? (Y/N): ')
	if x.lower() == 'y':
		from .setToken import __main__
		sys.exit(0)
	sys.exit(1)

try:
	input('Hit enter to use authed version, hit CTRL+C for anonymous version')
	client = FichierClient(x, be_nice = True)
except KeyboardInterrupt:
	print()
	client = FichierClient()

def test_remote_upload_info():
	remote_uploads = client.list_remote_uploads()
	#~ Available option: only_data: Boolean (returns only the data part [list] of the response)

	remote_upload_id = remote_uploads['data'][0]['id']

	remote_upload_info = client.remote_upload_info(remote_upload_id)
	#~ Available option: only_data: Boolean (returns only the data part [result list] of the response)

	print(remote_upload_info)

def test_create_remote_upload():
	remote_upload = client.remote_upload_create([input('Type a link: ')], 
		headers = {'X-Forwarded-For':'84.183.213.105'})

	print(remote_upload)

def test_create_remote_upload_x():
	times = 2
	try:
		times_str = input('How many links do you have? [int] ')
		times = int(times_str)
	except KeyboardInterrupt:
		pass
	except ValueError:
		print('Error: Not a numeric value')
		return
	
	upload_list = []
	for i in range(0, times):
		upload_list.append(input(f'Type link #{i+1}: '))
	remote_upload = client.remote_upload_create(upload_list, 
		headers = {'X-Forwarded-For':'84.183.213.105'})

	print(remote_upload)
	
def test_upload():
	upload = client.upload_file('TESTFILE.dat')
	print(upload)

def test_download():
	download_url = client.get_download_link(input('Type a 1fichier link: '), cdn = True, restrict_ip = 2)
	print(download_url)

def test_listfolders():
	pass
	
def test_download_file_from_dir():
	folder = client.get_folder()
	subfolder = folder.subfolders.get_subfolder('Degrassi NC')
	#~ print(subfolder.subfolders.list())
	print(subfolder.files[0].get_download_link())
	#~ folder_list = 
	#~ for folder in folder_list:
		#~ name = folder['name']
		#~ if 'email' in folder:
			#~ email = folder['email']
			#~ print(f'{name} ({email})')
		#~ else:
			#~ print(f'{name}')
			
def test_resolvepath():
	folder = client.resolve_path('/Fox.com/New Girl')
	print(folder.data)



if __name__ == '__main__' or __package__ == 'pyOneFichierAPI':
	print('1fichier (unofficial) API client - testing module - v0.1')
	print('This is a testing CLI, not an end-user CLI, any wanted changes are to be done in direct source editing')
	print('Purpose: Demonstrate the client and show/explain any users how to use it')


	globals()['action_remotecreate'] = test_create_remote_upload
	globals()['action_remotecreatex'] = test_create_remote_upload_x
	globals()['action_remoteinfo'] = test_remote_upload_info
	globals()['action_upload'] = test_upload
	globals()['action_download'] = test_download
	globals()['action_listfld'] = test_listfolders
	globals()['action_dlfromdir'] = test_download_file_from_dir
	globals()['action_resolvepath'] = test_resolvepath

	print('type "help" for a list of testcommands, "exit" (+Enter) or hit CTRL+C to exit')
	print()
	while True:
		try:
			c = input('Input testcommand>> ')
			if c == 'help':
				print('NOTE: Only the command with (A) works without authorization')
				print('--HELP--')
				print('remoteinfo')
				print('remotecreate')
				print('remotecreatex - Upload as many links as you\'d like.')
				print('upload (A)')
				print('download')
				print('listfld')
				print('dlfromdir - download a file from a directory')
				print('resolvepath')
			elif f'action_{c}' in globals():
				try:
					globals()[f'action_{c}']()
				except Exception as e:
					print('Caught', type(e).__name__, f'- {e}')
			elif c == 'exit':
				break
			else:
				print('Not a valid command')
			print()
		except (KeyboardInterrupt, EOFError):
			print()
			break
