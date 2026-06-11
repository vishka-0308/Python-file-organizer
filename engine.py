import os
import shutil
import hashlib

file_types={
    "Images": ["jpg", "jpeg", "png", "gif"],
    "Documents": ["pdf", "docx", "txt","doc"],
    "Videos": ["mp4", "avi", "mkv"],
    "Archives":["tar","zip","rar"]
}


def get_extension(filename):
    return filename.split(".")[-1]

def create_folder(folder_path,folder_name):
    new_folder=os.path.join(folder_path,folder_name)
    os.makedirs(new_folder,exist_ok=True)
    return new_folder

def get_category(extension):
    for (category,exten) in file_types.items():
        if extension in exten:
            return category
    return "Others"

def organise_files(folder_path):
    logs=[]

    for filename in os.listdir(folder_path):
        file_path=os.path.join(folder_path,filename)
        if os.path.isfile(file_path):
            extension=get_extension(filename)
            category=get_category(extension)

            destin_folder=create_folder(folder_path,category)

            shutil.move(file_path,destin_folder)

            logs.append(f"Moved {filename} to {category}")
    return logs

def get_file_hash(file_path):
    hasher=hashlib.md5()
    with open(file_path,'rb') as fp:
        while chunk:=fp.read(4096):
            hasher.update(chunk)
    
    return hasher.hexdigest()

def find_duplicates(folder_path):
    file_hashes={}
    duplicates=[]

    for root,dirs,files in os.walk(folder_path):
        for file in files:
            
            file_path = os.path.join(root,file)
            file_hash = get_file_hash(file_path)
            
            if file_hash in file_hashes:
                duplicates.append(file_path)

            file_hashes[file_hash]=file_path

    return duplicates

def move_duplicates(folder_path,duplicates):
    
    duplicate_folder=create_folder(folder_path,"Duplicates")
    
    logs=[]
    for file_path in duplicates:
        shutil.move(file_path,duplicate_folder)

        logs.append(f"Found duplicate of {file_path} and is moved to {duplicate_folder}")

    return logs