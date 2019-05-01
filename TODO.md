# TODO list


## API Endpoints

API Endpoint base url is: `https://api.1fichier.com/`

✖️ Change properties of a file (v1/file/chattr.cgi)

✖️ Share a folder (v1/folder/share.cgi)

✖️ Move a folder (v1/folder/mv.cgi)

✖️ Remove a folder (v1/folder/rm.cgi)

✖️ Show / set account options (v1/user/info.cgi)

✖️ FTP: Send processing request (v1/ftp/process.cgi)

✖️ FTP: List accounts (v1/ftp/users/ls.cgi)

✖️ FTP: Create an account (v1/ftp/users/add.cgi)

✖️ FTP: Remove an account (v1/ftp/users/rm.cgi)


✔️ List remote uploads (v1/remote/ls.cgi)

✔️ Retrieve info about single remote upload job (v1/remote/info.cgi)

✔️ Create a remote upload job (v1/remote/request.cgi)


✔️ List folders (in a folder) (v1/folder/ls.cgi)

✔️ List files in a folder (v1/file/ls.cgi)

✔️ Retrieve a download link (v1/download/get_token.cgi)

✔️ Upload a file via with information from `v1/upload/get_upload_server.cgi`


✔️ Retrieve file information (v1/file/info.cgi)

✔️ Anti-Virus scan (v1/file/scan.cgi; not planned due to lack of requirement; need it? Give a valid reason and open a ticket) (a valid reason? because i wanted to)

✔️ Remove files (v1/file/rm.cgi)

✔️ Move files (v1/file/mv.cgi)

✔️ Copy files (v1/file/cp.cgi)

## Features of the API

✔️ Upload (also unauthed; the only feature so far that works with no login)

✔️ Download

✔️ Nice mode for "smart thinking" in certain modes instead of complaining

✔️ Resolve a (folder) path ('/Folder/subfolder/subfolderagain')

✔ Create file and folder objects (unfinished)

✖️ Managing files (listing, deleting, moving)