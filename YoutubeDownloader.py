from __future__ import unicode_literals
import os
import sys
import threading
from yt_dlp import YoutubeDL
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


# The main GUI window for the YouTube Downloader
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Graphics.ui", self)  # Load the UI design file
        self.show()  # Display the GUI window
        self.setWindowTitle("Youtube Downloader")  # Set window title
        self.std_download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))  # Default download path
        self.button_set.clicked.connect(self.set_button)  # Connect the "Set" button to its handler
        self.button_download.clicked.connect(self.download_button)  # Connect the "Download" button to its handler
        self.input_path.setText(self.std_download_path)  # Set default download path in the input field
        self.radio_single.setChecked(True)  # Default to single video download
        self.progress_bar.setValue(0)  # Initialize the progress bar to 0%
        self.cancel_flag = False  # Flag to handle cancellation of downloads

    # Opens a directory picker for the user to set a custom download folder
    def set_button(self):
        file_name = QFileDialog.getExistingDirectory()
        if file_name:  # If a directory is selected, update the path
            self.input_path.setText(file_name)

    # Starts the download process when the "Download" button is clicked
    def download_button(self):
        """Handles the download button click."""
        self.cancel_flag = False  # Reset the cancel flag
        url = self.input_url.text()  # Get the YouTube URL from the input field
        save_path = self.input_path.text()  # Get the save path from the input field
        quality = self.combo_quality.currentText()  # Get the selected quality option

        # Reset progress bar and display initial message
        self.progress_bar.setValue(0)
        self.label_done.setText("Starting download...")

        # Simulate initial progress for better user experience
        self.progress_bar.setValue(5)

        # Start the download process in a separate thread
        download_thread = threading.Thread(
            target=self.download_thread, args=(url, save_path, quality), daemon=True
        )
        download_thread.start()

    # Handles the actual download process in a separate thread
    def download_thread(self, url, save_path, quality):
        playlist = not self.radio_single.isChecked()  # Check if the user selected playlist download
        video_format = self.check_video.isChecked()  # Check if the user selected video format

        try:
            # Create a downloader instance and start the download
            downloader = Download(
                url, save_path, quality, video_format, playlist, self.update_progress, self.cancel_flag
            )
            song_title = downloader.download()  # Download and get the song title
            self.input_url.setText("")  # Clear the URL field
            self.label_done.setText(f"Downloaded: {song_title}")  # Display the downloaded song title
            self.show_notification(f"Downloaded: {song_title}")  # Show a pop-up notification
        except Exception as e:
            self.input_url.setText("")  # Clear the URL field
            self.label_done.setText(f"Error: {str(e)}")  # Display error message

    # Dynamically updates the progress bar based on download progress
    def update_progress(self, progress):
        """Update the progress bar dynamically."""
        self.progress_bar.setValue(progress)

    # Displays a pop-up notification to the user
    def show_notification(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Notification")
        msg.exec_()


# Handles the core downloading logic using yt-dlp
class Download(object):
    def __init__(self, url, save_path, quality, video_format, playlist, progress_callback, cancel_flag):
        self.url = url  # URL of the video/playlist to download
        self.save_path = save_path  # Path to save the downloaded file
        self.qualities = {"Best": "320", "Semi": "192", "Worst": "128"}  # Audio quality options
        self.video_format = video_format  # True if the user wants to download video
        self.quality = self.qualities.get(quality, "192")  # Selected quality
        self.playlist = playlist  # True if the user selected playlist download
        self.progress_callback = progress_callback  # Function to update progress
        self.cancel_flag = cancel_flag  # Flag to cancel the download

    # Download options for video format
    @property
    def video_opts(self):
        return {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "noplaylist": not self.playlist,
            "progress_hooks": [self.hook],  # Hook for progress updates
        }

    # Download options for audio format
    @property
    def song_opts(self):
        return {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": self.quality,
                }
            ],
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "noplaylist": not self.playlist,
            "progress_hooks": [self.hook],  # Hook for progress updates
        }

    # Hook function for updating progress and handling cancellation
    def hook(self, d):
        """Progress hook for yt-dlp."""
        if self.cancel_flag:  # Stop download if the cancel flag is set
            raise Exception("Download canceled by user.")
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes", None) or d.get("total_bytes_estimate", None)
            if total:
                percentage = downloaded / total * 100
                self.progress_callback(int(percentage))
        elif d["status"] == "finished":
            self.progress_callback(100)

    # Starts the download process and returns the song title
    def download(self):
        options = self.video_opts if self.video_format else self.song_opts
        with YoutubeDL(options) as download_object:
            info = download_object.extract_info(self.url, download=False)  # Fetch metadata
            song_name = info.get("title", "Unknown Title")  # Get song title
            download_object.download([self.url])  # Start download
            return song_name


# Main entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setWindowIcon(QtGui.QIcon("logo.ico"))
    sys.exit(app.exec_())
