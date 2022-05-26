import glob
import os
import shutil

source_path = '/Users/chris/Music/Coros'
target_path = '/Volumes/VERTIX 2/Music'


if __name__ == '__main__':
    if os.path.isdir(source_path) and os.path.isdir(target_path):
        source_files = glob.glob(source_path + '/**/*.mp3', recursive=True)
        target_files = glob.glob(target_path + '/**/*.mp3', recursive=True)
        
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
    
