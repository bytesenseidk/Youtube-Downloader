
# **Youtube Downloader**  
A fast, user-friendly, and modern YouTube downloader built with Python and PyQt5.

---

## **Overview**
The **Youtube Downloader** is a sleek and intuitive application designed to download YouTube videos or audio in a variety of formats. Featuring a clean GUI and real-time progress tracking, this tool supports downloading both single videos and playlists with ease.

---

## **Key Features**
- **Video & Audio Downloads**: Choose between downloading video files or extracting high-quality audio.  
- **Playlist Support**: Download entire playlists or single videos.  
- **Multiple Quality Options**: Select from *Best*, *Semi*, or *Worst* quality to suit your needs.  
- **Progress Tracking**: A real-time progress bar keeps you updated on the download status.  
- **Modern Dark Mode**: Enjoy a sleek dark-themed interface.  
- **Cross-Platform Support**: Works on Windows, Linux, and macOS.  

---

## **Requirements**
1. **Python 3.8+**  
2. **yt-dlp** ([Installation Guide](https://github.com/yt-dlp/yt-dlp))  
3. **FFmpeg** for audio and video processing ([Setup Guide](#ffmpeg-setup)).  

---

## **FFmpeg Setup**

### **For Windows**:
1. Download the latest FFmpeg build: [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).  
2. Extract the archive into a folder (e.g., `C:\FFmpeg`).  
3. Add the `bin` directory to your system's PATH:  
   - Open PowerShell as Administrator.  
   - Run the command:  
     ```cmd
     setx /m PATH "C:\FFmpeg\bin;%PATH%"
     ```
   - You should see: **SUCCESS: Specified value was saved.**  
4. Verify installation:  
   - Restart PowerShell and type:  
     ```cmd
     ffmpeg -version
     ```

---

## **How to Use**

### **Run the Application:**
1. Clone this repository:  
   ```bash
   git clone https://github.com/bytesenseidk/Youtube-Downloader.git
   cd Youtube-Downloader
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the application:  
   ```bash
   python YoutubeDownloader.py
   ```

---

## **Compile to Executable**

### **Steps to Compile:**
1. Install PyInstaller:  
   ```bash
   pip install pyinstaller
   ```
2. Compile the script:  
   ```bash
   pyinstaller --onefile --windowed --icon=logo.ico YoutubeDownloader.py
   ```
3. The executable file will be located in the `dist` directory.

---

## **Screenshot**
![Youtube Downloader Screenshot](https://github.com/user-attachments/assets/1c422679-f07c-41d9-9519-4968bcffb606)

## **Changelog**

### **Version History**:
- **v0.1**: Initial build with basic functionality.  
- **v0.2**: PyQt5 GUI integration.  
- **v0.3**:  
  - Switched from `youtube-dl` to `yt-dlp` for improved performance and reliability.  
  - Added real-time progress tracking with a progress bar.  
  - Implemented error handling and pop-up notifications.  
  - Enhanced user experience with dark mode.  

---

## **Author**
[**Byte Sensei**](https://github.com/bytesenseidk)  

---

## **License**
This project is licensed under the **Mozilla Public License 2.0**.  
See the [LICENSE](https://github.com/bytesenseidk/Youtube-Downloader/blob/main/LICENSE) file for details.

--- 

## **Support**
If you encounter any issues or have suggestions, feel free to open an [issue](https://github.com/bytesenseidk/Youtube-Downloader/issues) or reach out via the repository.