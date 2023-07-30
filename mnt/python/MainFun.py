
from plexapi.server import PlexServer
import plexapi.video as videos
from pyarr import SonarrAPI
IMDB_API_KEY = 'pk_n6m6p1r0d51yftj0k'

video_extensions = ['.mp4', '.mkv']

keep_download_media = 2
Move_download_media = 1

Radarr = 'http://192.168.1.111:7877'
Radarr_Token = 'b275adb168dd488ba5b308ca85417da8'
quality_profile_id = '4'

Sonarr_Url = 'http://192.168.1.99:8990'
Sonarr_Key = '122f5eddf4f74caeb0573cec53979897'
Sonarr = SonarrAPI(Sonarr_Url, Sonarr_Key)

Plex_url = 'http://192.168.1.99:32400'
Plex_token = 'nHH-GvyPB9cpKzNHGpxq'
plex = PlexServer(Plex_url, Plex_token)

watch_folders = [r"/home/jamie/Plex/Production_Dir/downloading/Movies/Media", 
                 r"/home/jamie/ConfigVMs/utorrent/mData",
                 r"/home/jamie/Plex/Production_Dir/downloading/Movies/Torrents"]


folder_movies = r"/home/jamie/MediaContent/Movies"
folder_shows = r"/home/jamie/MediaContent/TvShows"

lOG_FILE = 'Log/File_Flow.txt'
log_folder = r"Log/"

test_download = r"/home/jamie/MediaContent/testingDownload"