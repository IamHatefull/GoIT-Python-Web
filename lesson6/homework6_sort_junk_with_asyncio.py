from asyncio import run, gather
import asyncio

from aiopath import AsyncPath
import shutil



#Directory which have to be sorted
BASE_DIR = 'E:\Libfolder'

#Dictionary with all extentions we can recognize
EXTENTIONS = {
    'images' : ['.jpeg', '.png', '.jpg', '.svg'],
    'video' : ['.avi', '.mp4', '.mov', '.mkv'],
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
async def move_files(file_path_list: list, destination_dir: str):
    for file_path in file_path_list:
        path_list = str(file_path).split('\\')
        path_list.insert(-1, destination_dir)
        check_dir = path_list
        destination_path = '\\'.join(path_list)
        check_dir.pop(-1)
        check_path = '\\'.join(check_dir)

        if not await AsyncPath(check_path).is_dir():
            AsyncPath(check_path).mkdir()
        
        shutil.move(file_path, destination_path)

    file_path_list.clear()


#Add all file paths with suitable extention to suitable list. Example: '.jpeg', '.png', '.jpg', '.svg' -> images[]
#As arguments you need to pass list of paths(images), path to directory you want to sort and name of list as string('images')
async def add_to_path_list(path_list_name: list, path: AsyncPath, extention_type: str):
    source = AsyncPath(path)

    async for obj in source.iterdir():
        name = obj.name

        #Check if objeckt is directory. If it is and needed for moving files, then skip it.
        #If directory is empty, then remove it.

        if await obj.is_dir():
            if name == 'images' or name == 'documents' or name == 'audio' or name == 'video' or name == 'arkhives':
                continue
            if await obj.stat() is False:
                obj.rmdir()
                continue
            new_path = f'{path}\\{obj.name}'
            await add_to_path_list(path_list_name, new_path, extention_type)

        extention = obj.suffix

        if extention in EXTENTIONS[extention_type]:
            path_list_name.append(obj)
            

async def main():
    await asyncio.gather(add_to_path_list(images, BASE_DIR, "images"), add_to_path_list(video, BASE_DIR, "video"), add_to_path_list(documents, BASE_DIR, "documents"), add_to_path_list(music, BASE_DIR, "music"),add_to_path_list(arkhives, BASE_DIR, "arkhives"))
    await asyncio.gather(move_files(images, "images"), move_files(video, "video"), move_files(documents, "documents"), move_files(music, "music"), move_files(arkhives, "arkhives"))
    
if __name__ == "__main__":
    print('started main')

    asyncio.run(main())

    print('End of main!')