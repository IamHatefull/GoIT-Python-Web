from pathlib import Path
import shutil, threading
import concurrent.futures


#Directory which have to be sorted
BASE_DIR = 'E:\Libfolder'

#Dictionary with all extentions we can recognize
EXTENTIONS = {
    'images' : ['.jpeg', '.png', '.jpg', '.svg'],
    'videos' : ['.avi', '.mp4', '.mov', '.mkv'],
    'documents' : ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'music' : ['.mp3', '.ogg', '.wav', '.amr'],
    'arkhives' : ['.zip', '.gz', '.tar']
}

#Lists for files paths. File with suitable extention will be added to suitable list
images = []
video = []
documents = []
music = []
arkhives = []


#function which move all files from list into destination directory.
def move_files(file_path_list: list, destination_dir: str):
    for file_path in file_path_list:
        path_list = str(file_path).split('\\')
        path_list.insert(-1, destination_dir)
        check_dir = path_list
        destination_path = '\\'.join(path_list)
        check_dir.pop(-1)
        check_path = '\\'.join(check_dir)

        if not Path(check_path).is_dir():
            Path(check_path).mkdir()
        
        shutil.move(file_path, destination_path)

    file_path_list.clear()


#Add all file paths with suitable extention to suitable list. Example: '.jpeg', '.png', '.jpg', '.svg' -> images[]
#As arguments you need to pass list of paths(images), path to directory you want to sort and name of list as string('images')
def add_to_path_list(path_list_name: list, path: Path, extention_type: str):
    source = Path(path)

    for obj in source.iterdir():
        name = obj.name

        #Check if objeckt is directory. If it is and needed for moving files, then skip it.
        #If directory is empty, then remove it.

        if obj.is_dir():
            if name == 'images' or name == 'documents' or name == 'audio' or name == 'video' or name == 'archives':
                continue
            if obj.stat().st_size == 0:
                obj.rmdir()
                continue
            new_path = f'{path}\\{obj.name}'
            add_to_path_list(path_list_name, new_path, extention_type)

        extention = obj.suffix

        if extention in EXTENTIONS[extention_type]:
            path_list_name.append(obj)
            

    
    
if __name__ == "__main__":
    print('started main')

    with concurrent.futures.ThreadPoolExecutor(max_workers= 5) as executor:
        result = executor.map(add_to_path_list, (images, video, documents, music, arkhives), (BASE_DIR, BASE_DIR, BASE_DIR, BASE_DIR, BASE_DIR), ('images','video', 'documents', 'music', 'arkhives'))

    print(images)
    print(video)
    print(documents)
    print(music)
    print(arkhives)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        result = executor.map(move_files,(images, video, documents, music, arkhives), ('images','video', 'documents', 'music', 'arkhives'))

    print('End of main!')