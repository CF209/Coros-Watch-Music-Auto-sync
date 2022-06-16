I recently bought a Coros Vertix 2 watch to track my running and other activities. One function of the watch is it can connect to bluetooth headphones to play music. It's slightly inconvenient though since you have to manually transfer mp3 files to the watch. I created this script to automatically sync the mp3 files on the watch with a folder on my laptop every time I connect the watch with USB.

To use this script, first edit the source_path and the target_path variables within the script. The source_path is the directory on your computer. The destination path is the directory of the Music folder on your watch.

You can then run the script manually with:
```bash
python3 coros_music_sync.py
```

Or you can set up a cronjob to run the script automatically. On Mac this is done by editing the crontab file with:
```bash
crontab -e
```

Add the following line to the file replacing "PATH" with your path. This runs the script once every minute. If you want to run at a different interval, you can find the setting you want at [crontab.guru](https://crontab.guru/)
```bash
* * * * * python3 /PATH/coros_music_sync.py
```

Save the file with ":x"

The script should now automatically run every minute. If the watch is not plugged in, the target directory doesn't exist and the script will exit. If the watch is plugged in, it scans the source directory for any mp3 files that don't exist on the watch and copies them over. It then scans the watch for any files that aren't in the source directory and deletes them.

To automatically download mp3 files from a Spotify playlist, you can automatically use [https://github.com/spotDL/spotify-downloader](https://github.com/spotDL/spotify-downloader)

To use spotDL, install it with:
```bash
pip3 install spotdl
brew install ffmpeg
```

You can then run it with this command entering your own output directory and spotify playlist URL:
```bash
spotdl --output /OUTPUT-PATH/ PLAYLIST-URL
```

I set up another cronjob to automatically run the script. I added these lines with crontab -e:
```bash
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
0,15,30,45 * * * * /Library/Frameworks/Python.framework/Versions/3.7/bin/spotdl --output /Users/chris/Music/Coros/spotdl https://open.spotify.com/playlist/2TaVlCCRsgE987W8baaC8i
```

This runs spotDL every 15 minutes. I had to also add the PATH line to get ffmpeg to work

With this setup, I can now add songs to this spotify playlist from anywhere and my computer will automatically download them. Then when I plug in my watch to charge, the songs will automatically transfer over to the watch.

Issues:
 - Removing songs from the spotify playlist won't remove them from your computer
 - SpotDL only works with music. I need a different way to download podcasts
