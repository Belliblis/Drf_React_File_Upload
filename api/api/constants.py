from os.path import splitext, isfile, abspath, exists

allowed_files = {".doc": "application/msword", ".docx": "application/msword", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".png": "image/png", ".pdf":"application/pdf", ".zip":"application/zip"}

valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.jpeg', '.zip']

file_path = "/media/uploads/"

name ='api/media/uploads/Пример.png'

#print(exists(name))
#path = abspath(name)
#print(path)
#print(exists(path))
