from .exceptions import NotFoundError

class FichierFile(object):
	def __init__(self, client, data):
		self.data = data
		self.client = client
		self.url = data['url']
		self.filename = data['filename']
		self.data = data['date']
		self.checksum = data['checksum']
		self.content_type = data['content-type']
		self.has_pass = bool(data['pass'])
		self.restricted = bool(data['acl'])
		self.cdn = bool(data['cdn'])
	
	def get_download_link(self, inline = False, cdn = False, restrict_ip = False, passw = None, 
		no_ssl = False, folder_id = None, filename = None, sharing_user = None):
			return self.client.get_download_link(self.url, inline, cdn, restrict_ip, passw, no_ssl, folder_id, filename, sharing_user)

class subfolders_object(object):
	def __init__(self, client, data):
		self.data = data
		self.client = client
		
	def list(self):
		for folder in self.data:
			print(folder['name'])
		
	def get_list(self):
		return [k['name'] for k in self.data]
		
	def get_subfolder(self, name, only_subfolders = False):
		folder_id = None
		for subfolder in self.data:
			if name == subfolder['name']:
				folder_id = subfolder['id']
				
		if folder_id:
			return self.client.get_folder(folder_id, only_subfolders = only_subfolders)
		else:
			raise NotFoundError ('Folder not found')
			
class FichierFolder(object):
	def __init__(self, client, data):
		self.data = data
		self.subfolders = subfolders_object(client, data.get('sub_folders',[]))
		self.files = [FichierFile(client, file) for file in data.get('items',[])]