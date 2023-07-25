import os, shutil, PTN, subprocess
import time
import datetime
from datetime import date
import patoolib
from MainFun import Move_download_media, keep_download_media, watch_folders, folder_movies, folder_shows, plex, video_extensions, lOG_FILE, log_folder

NowTime = datetime.datetime.now()


def file_time(file_path): 
        c_time = os.path.getctime(file_path)
        dt_c = datetime.datetime.fromtimestamp(c_time)
        delta = NowTime- dt_c
        return delta

def read_download(ps, paths):
    file_path = os.path.join(paths, ps)
    if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in video_extensions and file_time(file_path).days > Move_download_media:
        sorting_file(file_path)
    else:
        if not os.path.isfile(file_path):
                for subfile in os.listdir(file_path):
                        subfile_path = os.path.join(file_path, subfile)
                        if os.path.isfile(subfile_path) and file_time(file_path).days > Move_download_media:
                                if subfile_path.endswith('.rar'):
                                        if not os.path.exists(file_path+'/temp'):
                                                os.makedirs(file_path+'/temp')
                                        for item in os.listdir(file_path):
                                                item_path = os.path.join(file_path, item)
                                                temp_item_path = os.path.join(file_path+'/temp', item)
                                                if os.path.isfile(item_path):
                                                        shutil.copy2(item_path, temp_item_path)
                                        rar_file_path = None
                                        for root, _, files in os.walk(file_path+'/temp'):
                                                for file in files:
                                                        if file.endswith('.rar'):
                                                                rar_file_path = os.path.join(root, file)
                                                                break
                                        patoolib.extract_archive(rar_file_path, outdir=file_path+'/temp')
                                        files = [os.path.join(file_path+'/temp', file) for file in os.listdir(file_path+'/temp')]
                                        subfile_path = max(files, key=os.path.getctime)
                                        sorting_file(subfile_path)
                        elif os.path.isfile(subfile_path) and os.path.splitext(subfile_path)[1].lower() in video_extensions and file_time(file_path).days > Move_download_media:
                                sorting_file(subfile_path)


def sorting_file(file_path): 
    filename = os.path.basename(file_path)
    parsing = PTN.parse(filename)
    try:
        title = parsing['title'].title()
    except:
        title = None
    try:
        year = parsing['year']
    except:
        year = None
    try:
        season = parsing['season']
    except:
        season = None
    try:
        episode = parsing['episode']
    except:
        episode = None
    try:
        codec = parsing['codec']
    except:
        codec = None
    if title:
        if not 'preview' in title.lower() and not 'sample' in title.lower():
            if season == None and year != None:
                Movie(file_path, title, year, codec)
            if season != None:
                TVShows(file_path, title, season, episode, codec)
                              
def Movie(file_path, title, year, codec):
    source_path = file_path
    destination_folder = os.path.join(folder_movies, f'{title} ({year})')
    destination_path = os.path.join(destination_folder, f'{title} ({year}).mkv')
    if not os.path.exists(destination_path):
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        if codec == 'H.265' or codec == 'H.264':
            shutil.copy2(source_path, destination_path)
            plex.library.update()
        else:
            convert_to_h264(source_path, destination_path, destination_folder)

def TVShows(file_path, title, season, episode, codec):
    source_path = file_path
    destination_show_folder = os.path.join(folder_shows, title)
    destination_season_folder = os.path.join(destination_show_folder, f'Season {season}')
    destination_path = os.path.join(destination_season_folder, f'{title} - S{season:02d}E{episode:02d}.mkv')
    if not os.path.exists(destination_path):
        if not os.path.exists(destination_show_folder):
            os.makedirs(destination_show_folder)
        if not os.path.exists(destination_season_folder):
            os.makedirs(destination_season_folder)
        if codec == 'H.265' or codec == 'H.264':
            shutil.copy2(source_path, destination_path)
            plex.library.update()
        else:
            convert_to_h264(source_path, destination_path, destination_show_folder)
                                       
def convert_to_h264(input_file, destination_path, destination_folder):    
    command = ["ffmpeg", "-y", "-i", input_file, "-c:v", "libx265", "-crf", "20", "-preset", "medium", "-c:a", "copy", destination_path]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
        plex.library.update()
        return destination_path 
    except subprocess.CalledProcessError as e:
        return None
 
def Clean_data(paths):
    empty_FILE_count = 0
    empty_dir_count = 0
    for path in os.listdir(paths):
        # check if current path is a file
        file_path = os.path.join(paths, path)
        if os.path.isfile(file_path):
            if file_time(file_path).days > keep_download_media:
                os.remove(file_path)
                empty_FILE_count = empty_FILE_count+1
        else:
            subfolder_path = os.path.join(paths, path)
            if os.path.isfile(subfolder_path):
                if file_time(file_path).days > keep_download_media:
                    os.remove(subfolder_path)
                    empty_FILE_count = empty_FILE_count+1
            else:
                for subfile in os.listdir(subfolder_path):
                    subfile_path = os.path.join(subfolder_path, subfile)
                    if os.path.isfile(subfile_path):
                        if file_time(file_path).days > keep_download_media:
                            os.remove(subfile_path)
                            empty_FILE_count = empty_FILE_count+1
                    else:
                        for sp in os.listdir(subfile_path):
                            subSubfile_path = os.path.join(subfile_path, sp)
                            if os.path.isfile(subSubfile_path):  
                                if file_time(file_path).days > keep_download_media:
                                    os.remove(subSubfile_path)
                                    empty_FILE_count = empty_FILE_count+1                              
        for path in os.listdir(paths):
            # check if current path is a file
            file_path = os.path.join(paths, path)
            if not os.path.isfile(file_path):
                for folder in os.listdir(file_path):
                    subFolder = os.path.join(file_path, folder)
                    if not os.path.isfile(subFolder)and len(os.listdir(subFolder)) == 0:
                        empty_dir_count = empty_dir_count+1
                        os.rmdir(subFolder)    
                    if not os.path.isfile(file_path)and len(os.listdir(file_path)) == 0:
                        empty_dir_count = empty_dir_count+1
                        os.rmdir(file_path)            
    if empty_FILE_count > 1:
        print('DELETED ',empty_FILE_count,'OLD FILES', paths,'AT', NowTime, file=open(lOG_FILE, 'a'))
    if empty_dir_count > 1:
        print('DELETED ',empty_dir_count,'EMPTY DIR IN', paths,'AT', NowTime, file=open(lOG_FILE, 'a'))
        
def Clean_Logs():
            ls_log_folder  =  os.listdir(folder_movies) 
            for Log_File in ls_log_folder:
                Log_path = os.path.join(log_folder, Log_File)
if os.path.isfile(lOG_FILE): 
    os.remove(lOG_FILE)
    print('Stated at ',NowTime, file=open(lOG_FILE, 'a'))
    
count = 0
while True:
    count = count+1
    for paths in watch_folders:
        path_ls = os.listdir(paths)
        for ps in path_ls:
            read_download(ps, paths)
        print('DONE WITH FILE', NowTime, paths, file=open(lOG_FILE, 'a'))
        #Clean_data(paths) 
        print("done")
    plex.library.optimize()
    print('PLEX OPTIMIZE', NowTime, file=open(lOG_FILE, 'a'))
    print('DONE WITH FLOW ROUND',count , NowTime, file=open(lOG_FILE, 'a')) 
    #Clean_Logs()  
    time.sleep(10800)
