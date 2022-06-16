I recently bought a Coros Vertix 2 watch to track my running and other activities. One function of the watch is it can connect to bluetooth headphones to play music. It's slightly inconvenient though since you have to manually transfer mp3 files to the watch. I created this script to automatically sync the mp3 files on the watch with a folder on my laptop every time I connect the watch with USB. I also added functions to the script for downloading podcasts and spotify playlists.

To use this script, first edit the "source_path" and the "target_path" variables within the script. The source_path is the directory on your computer. The destination path is the directory of the Music folder on your watch.

Next fill the "spotify_playlists" list with the URL of any spotify playlists you want to download, and the "podcasts" dictionary with the name and RSS URL of the podcasts you want to download. You can change some of the settings in the podcast download options as well including the template for how these files will be named, and date_from variable which I have set to download any podcasts from the last 30 days.

More info on the podcast download library can be found here:
https://gitlab.com/fholmer/getpodcast

You can then run the script manually with:
```bash
python3 coros_music_sync.py
```

Or you can set up a cronjob to run the script automatically. On Mac this is done by editing the crontab file with:
```bash
crontab -e
```

Add the following line to the file replacing "PATH" with your path. I also needed to update the PATH to get everything to work. This runs the script once every 5 minutes. If you want to run at a different interval, you can find the setting you want at [crontab.guru](https://crontab.guru/)
```bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
*/5 * * * * python3 /PATH/coros_music_sync.py
```

In order for crontab to be able to access external storage, I had to follow these steps as well:
https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/

The script should now automatically run every 5 minutes. It first downloads any missing music and podcast files. Then, if the watch is not plugged in, the target directory doesn't exist and the script will exit. If the watch is plugged in, it scans the source directory for any mp3 files that don't exist on the watch and copies them over. It then scans the watch for any files that aren't in the source directory and deletes them.

With this setup, I can now add songs to a spotify playlist from anywhere and my computer will automatically download them. Any new podcasts releases will also automatically be downloaded. Then when I plug in my watch to charge, the songs will automatically transfer over to the watch.

Issues:
 - Removing songs from the spotify playlist won't remove them from your computer
 - The Coros watch doesn't separate files by folder, so all the songs and podcasts get mixed up. If I can figure out how the Coros watch sorts files, I could edit the files to get them sorted so podcasts appear first
