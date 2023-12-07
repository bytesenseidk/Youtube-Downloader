# Youtube Downloader
 Fast PyQt5 Youtube download application 

# Description
- Download Video or Sound
- Download Singles & Playlists
- Multiple Quality-Options Available
 
![yt_dl](https://user-images.githubusercontent.com/50791042/185397447-e67f6700-392d-4272-9898-01e73c232e97.png)

# FFMpeg Setup
Windows Install:
1. FFmpeg download link Windows 10: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
2. Extract files to a folder named FFmpeg
- FFmpeg:
  - bin
  - doc
  - presets
    - LICENCE
    - README
3. Copy or clip folder to C-Drive or desired folder
4. Open PowerShell as admin
5. Type this command (Depends on your save path for the folder "FFmpeg"):
    - setx /m PATH "C:\FFmpeg\bin;%PATH%"
    - If done right, PowerShell will show this message:
        - SUCCESS: Specified value was saved.
6. Test version number:
    1. Restart PowerShell
    2. Type: 
        - ffmpeg -version

# Application Compilation to Executable
Compile to exe:
1. Open terminal, download repository and cd into download directory:
    - git clone https://github.com/bytesenseidk/Youtube-Downloader.git
    - cd Youtube-Downloader
2. Install pyinstaller: 
    - pip install pyinstaller
3. Install requirements:
    - pip install -r requirements.txt
4. Compile script:
    - pyinstaller --onefile --windowed --icon=logo.ico YoutubeDownloader.py
5. Executable file will be located inside "dist" folder.

# Authors
[Byte Sensei](https://github.com/bytesenseidk)

# Version History
- 0.1:
  * Initial build
- 0.2:
  * PyQt5 GUI Integtation
   
# Licence
This project is licenced under the Mozilla Public License 2.0 - see the [LICENCE](https://github.com/LarsRosenkilde/MusicPlayer/blob/master/LICENCE) for details

