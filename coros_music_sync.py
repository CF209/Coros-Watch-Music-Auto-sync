import glob
import os
import shutil
import podcast.getpodcast
from datetime import date
from dateutil.relativedelta import relativedelta
from tendo import singleton

# Ensure only one instance of this script is running at the same time
# I originally had the music downloads, podcast download, and file syncing in different
# scripts, but I ran into the occasional issue where two scripts would try to access
# the same files. I also ran into the issue where the script would take a long time
# to complete and crontab would start a new instance of the script at the same time
# Adding the below line and merging all scripts into one solves these issues
me = singleton.SingleInstance()

# source_path is where music and podcasts are stored on your computer
# target_path is the "Music" folder on your Coros watch
source_path = '/Users/chris/Music/Coros'
target_path = '/Volumes/VERTIX 2/Music'

# List of Spotify playlist URLs to download
spotify_playlists = [
    'https://open.spotify.com/playlist/2TaVlCCRsgE987W8baaC8i'
]

# List of podcasts
# "podcastname": "RSS URL"
podcasts = {
    "RL": "http://feeds.wnyc.org/radiolab",
    "99": "https://feeds.simplecast.com/BqbsxVfO",
    "DD": "https://feeds.megaphone.fm/DTT3537615344"
}

# Podcast download options
opt = podcast.getpodcast.options(
    run=True,
    onlynew=True,
    deleteold=True,
    date_from=str(date.today()-relativedelta(days=30)),
    root_dir=f"{source_path}/Podcasts",
    template="{rootdir}/{date} {podcast} - {title}{ext}",
)

# Use SpotDL to download music from a spotify playlist
print("\nDownloading Music...\n")
for playlist in spotify_playlists:
    os.system(f"/usr/local/bin/spotdl --output {source_path}/Spotify {playlist}")

# Download podcasts
print("\nDownloading Podcasts...\n")
podcast.getpodcast.getpodcast(podcasts, opt)

# Sync Directories
print("\nSyncing directories...\n")
if os.path.isdir(source_path) and os.path.isdir(target_path):
    # Get list of files in source and target directories
    source_files = glob.glob(source_path + '/**/*.mp3', recursive=True)
    target_files = glob.glob(target_path + '/**/*.mp3', recursive=True)
    
    # Transfer any new files from the source directory to the target directory
    for f in source_files:
        if f.replace(source_path, '') not in [tf.replace(target_path, '') for tf in target_files]:
            path, filename = os.path.split(f)
            path = path.replace(source_path, '')
            print(f"Copying {path}/{filename} to watch")
            try:
                os.makedirs(target_path + path, exist_ok=True)
            except:
                print(f"Error creating new directory {target_path + path}")
            try:
                shutil.copy(f, target_path + path)
            except:
                print(f"Error copying file {f}")

    # Delete any old files from the target directory
    for f in target_files:
        if f.replace(target_path, '') not in [sf.replace(source_path, '') for sf in source_files]:
            print(f"Removing file {f} from watch")
            try:
                os.remove(f)
            except:
                print(f"Error removing file {f}")
            try:
                path, filename = os.path.split(f)
                if len(os.listdir(path)) == 0:
                    print(f"Removing directory {path} since it is empty")
                    os.rmdir(path)
            except:
                print(f"Error checking/removing directory {path}")
else:
    print("Path not found. Check that watch is connected and source directory exists")

