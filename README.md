I recently bought a Coros Vertix 2 watch to track my running and other activities. One function of the watch is it can connect to bluetooth headphones to play music. It's slightly inconvenient though since you have to manually transfer mp3 files to the watch. I created this script to automatically sync the mp3 files on the watch with a folder on my laptop every time I connect the watch with USB.

To use this script, first edit the source_path and the target_path variables within the script. The source_path is the directory on your computer. The destination path is the directory of the Music folder on your watch.

You can then run the script manually with:
python3 coros_music_sync.py

Or you can set up a cronjob to run the script automatically. On Mac this is done by editing the crontab file in your home directory:

<p>cd ~/<br>
nano crontab -e</p>

Add the following line to the file replacing "PATH" with your path. This runs the script once every minute. If you want to run at a different interval, you can find the setting you want at [crontab.guru](https://crontab.guru/)
<p>* * * * * python3 /PATH/coros_music_sync.py</p>

Save the file with CTRL+O and CTRL+X

The script should now automatically run every minute. If the watch is not plugged in, the target directory doesn't exist and the script will exit. If the watch is plugged in, it scans the source directory for any mp3 files that don't exist on the watch and copies them over. It then scans the watch for any files that aren't in the source directory and deletes them.
