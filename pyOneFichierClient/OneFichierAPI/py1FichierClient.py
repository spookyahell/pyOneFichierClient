import requests
from subprocess import call
from copy import deepcopy
from .exceptions import FichierResponseNotOk, FichierSyntaxError, InsufficientInfoError, NotAuthorized
from json.decoder import JSONDecodeError
import re
import json
from .objects import FichierFile, FichierFolder

s = requests.Session()
#~ s.verify = False


class FichierClient(object):
    
    def __init__(self, APIkey = None, be_nice = False):
        if APIkey:
            self.auth = {'Authorization':f'Bearer {APIkey}','Content-Type':'application/json'}
            self.auth_nc = {'Authorization':f'Bearer {APIkey}'}
            self.authed = True
        else:
            self.authed = False
            self.auth = {'Content-Type':'application/json'}
        self.be_nice = be_nice
        
    def _raise_unauthorized(self):
        raise NotAuthorized('You are using a very limited version of the API, and the feature you are trying to use requires an APIkey.')
            
    def _APIcall(self, url, json = None, method = 'POST'):
        if method == 'POST':
            r = s.post(url, json = json, headers = self.auth)
        elif method == 'GET':
            r = s.get(url, headers = self.auth)
        else:
            raise FichierSyntaxError(f'Method {method} not available/implemented')
        if r.ok:
            try:
                o = r.json()
            except JSONDecodeError:
                raise FichierResponseNotOk(f'1fichier returned malformed json')
            if 'status' in o:
                if o['status'] == 'OK':
                    return r.json()
                else:
                    message = r.json()['message']
                    raise FichierResponseNotOk(f'Response from 1fichier: {message!r}')
            else:
                #~ No status available, assume response is okay
                return o
                
        else:
            raise FichierResponseNotOk(f'HTTP Response code from 1fichier: {r.status_code} {r.reason}')
            
            
        
    def resolve_path(self, path):
        #~ print(f'Resolving {path!r}...')
        if not path.startswith('/'):
            raise FichierSyntaxError('Paths must start from root, aka start with a forward slash ("/")')
        folder_paths = path.split('/')
        del folder_paths[0]
        folder = self.get_folder()
        for idx, folder_path in enumerate(folder_paths):
            if idx+1 < len(folder_paths):
                folder = folder.subfolders.get_subfolder(folder_path, only_subfolders = True)
            else:
                folder = folder.subfolders.get_subfolder(folder_path)
        
        return folder
            
        
            
        #~ if folder_paths[1] =
        
        
        
    
    def list_remote_uploads(self, only_data = False):
        o = self._APIcall('https://api.1fichier.com/v1/remote/ls.cgi')
        if o is not None:
            if only_data:
                return o['data']
            else:
                return o
        else:
            return
            
            
    def remote_upload_info(self, id = None, only_data = False):
        if not self.authed:
            self._raise_unauthorized()
        if id is None:
            raise InsufficientInfoError('We need an id of an exisiting remote upload via "id" param')
        o = self._APIcall('https://api.1fichier.com/v1/remote/info.cgi', json = {'id':id})
        if o is not None:
            if only_data:
                return o['result']
            else:
                return o
        else:
            return
            
            
    def remote_upload_create(self, urls = None, headers = None):
        if not self.authed:
            self._raise_unauthorized()
        if urls is None:
            raise InsufficientInfoError('We need a list of urls to upload via "urls" param')
            
        upload_info = {'urls':urls}
        if headers:
            upload_info.update({'headers':headers})
        o = self._APIcall('https://api.1fichier.com/v1/remote/request.cgi', json = upload_info)
        if o is not None:
            #~ if only_data:
                #~ return o['result']
            #~ else:
            return o
        else:
            return
            
    def _get_folders(self, id = 0):
        if not self.authed:
            self._raise_unauthorized()
        params = {'folder_id':id}
        o = self._APIcall('https://api.1fichier.com/v1/folder/ls.cgi', json = params)
        return o
        
    def _get_files(self, id = 0):
        if not self.authed:
            self._raise_unauthorized()
            
        params = {'folder_id':id}
        o = self._APIcall('https://api.1fichier.com/v1/file/ls.cgi', json = params)
        
        return o
    
    def get_folder(self, id = 0, only_subfolders = False):
        o = self._get_folders(id)
        
        if not only_subfolders:
            o.update(self._get_files(id))
        
        return FichierFolder(self, o)
        
        
            
    def get_download_link(self, url, inline = False, cdn = False, restrict_ip = False, passw = None, 
        no_ssl = False, folder_id = None, filename = None, sharing_user = None):
        if not self.authed:
            self._raise_unauthorized()
        if restrict_ip:
            if not cdn:
                if self.be_nice:
                    cdn = True
                else:
                    raise FichierSyntaxError('Restricting IPs is only for CDN links')
        params = {
            'url' : url,
            'inline' : int(inline),
            'cdn' : int(cdn),
            'restrict_ip':  int(restrict_ip),
            'no_ssl' : int(no_ssl),
        }
        if passw:
            params['pass'] = passw
        if folder_id is not None:
            if filename is None:
                raise FichierSyntaxError('Also need a filename to go along with that')
            params.update({'folder_id' : folder_id, 'filename' : filename})
            if folder_id == 0:
                if sharing_user is None:
                    raise FichierSyntaxError('sharing_user not specified but required')
                params.update({'sharing_user' : sharing_user})
        #~ print(params)
        o = self._APIcall('https://api.1fichier.com/v1/download/get_token.cgi', json = params)
        return o['url']
            
    def upload_file(self, file_path):
        o = self._APIcall('https://api.1fichier.com/v1/upload/get_upload_server.cgi', method = 'GET')
        up_srv = o['url']
        id = o['id']
        
        multiple_files = [('file[]', ('TESTFILE.dat', open('TESTFILE.dat', 'rb'), 'application/octet-stream'))]
        
        up_u = f'https://{up_srv}/upload.cgi?id={id}'
        if self.authed is True:
            r = s.post(up_u, files = multiple_files, headers = self.auth_nc, allow_redirects = False)
        else:
            r = s.post(up_u, files = multiple_files, allow_redirects = False)
        if not 'Location' in r.headers:
            raise FichierResponseNotOk('Missing Locatiion header in response')
        loc = r.headers['Location']
        
        r = s.get(f'https://{up_srv}{loc}')
        
        x = re.search('<td class="normal"><a href="(.+)"', r.text)
        if x:
            return x.group(1)
        else:
            raise FichierResponseNotOk('Missing download link')
        
    def get_file_info(self, url, passw = None, folder_id = None, filename = None, sharing_user = None):
        if not self.authed:
            self._raise_unauthorized()
        params = {
            'url' : url
        }
        if passw:
            params['pass'] = passw
        if folder_id is not None:
            if filename is None:
                raise FichierSyntaxError('Also need a filename to go along with that')
            params.update({'folder_id' : folder_id, 'filename' : filename})
            if folder_id == 0:
                if sharing_user is None:
                    raise FichierSyntaxError('sharing_user not specified but required')
                params.update({'sharing_user' : sharing_user})

        o = self._APIcall('https://api.1fichier.com/v1/file/info.cgi', json = params)
        return o

    def virus_scan(self, url):
        if not self.authed:
            self._raise_unauthorized()
        params = {
            'url' : url
        }
  
        o = self._APIcall('https://api.1fichier.com/v1/file/scan.cgi', json = params)
        return o

    def remove_file(self, urls, codes=None):
        if not self.authed:
            self._raise_unauthorized()
        if codes:
            try:
                params = {
                    'files': [{'url': urls[i], 'code': codes[i]} for i in range(len(urls))]
                }
            except IndexError:
                raise FichierSyntaxError('If codes specified, it must be at least the length of the url list')
        else:
            params = {
                'files': [{'url': i} for i in urls]
            }

        o = self._APIcall('https://api.1fichier.com/v1/file/rm.cgi', json = params)
        return {'status': o['status'], 'removed': o['removed']}

    def move_file(self, urls, destination_folder = None, destination_user = '', rename = ''):
     
        if not destination_folder and destination_user:
            raise FichierSyntaxError('If destination_folder unspecified or 0, destination_user must be specified')

        if rename and len(urls) > 1:
            raise FichierSyntaxError('Cannot rename multiple urls at once')

        params = {
            'urls': urls
        }

        if destination_folder:
            params.update({'destination_folder_id': destination_folder})
        else:
            params.update({'destination_folder_id': 0, 'destination_user': destination_user})
   
        if rename:
            params.update({'rename': rename})
   
        o = self._APIcall('https://api.1fichier.com/v1/file/mv.cgi', json=params)
        return {'status': o['status'], 'moved': o['moved']}

    def copy_file(self, urls, destination_folder = None, destination_user = '', rename = '', passw = ''):
     
        if not destination_folder and destination_user:
            raise FichierSyntaxError('If destination_folder unspecified or 0, destination_user must be specified')

        if rename and len(urls) > 1:
            raise FichierSyntaxError('Cannot rename multiple urls at once')

        params = {
            'urls': urls
        }

        if destination_folder:
            params.update({'folder_id': destination_folder})
        else:
            params.update({'folder_id': 0, 'sharing_user': destination_user})
   
        if rename:
            params.update({'rename': rename})
   
        if passw:
            params.update({"pass": passw})
   
        o = self._APIcall('https://api.1fichier.com/v1/file/cp.cgi', json=params)
        return {'status': o['status'], 'copied': o['copied']}