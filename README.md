## cli tool to remux *.mkv files to *.mp4 using ffmpeg

> Must have [ffmpeg](https://www.ffmpeg.org/download.html) installed and added to PATH

```
usage: remuxer.py [-h] [-i] [-o [OUTPUT]] [-r]

Remux *.mkv files to mp4 using ffmpeg

options:
  -h, --help            show this help message and exit
  -i , --input          Input folder with .mkv files
  -o [OUTPUT], --output [OUTPUT]
                        Optional output folder for converted .mp4 files, will default to the same as the input directory
  -r, --remove          Remove .mkv file after conversion
```