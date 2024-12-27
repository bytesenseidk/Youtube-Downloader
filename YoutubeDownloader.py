from __future__ import unicode_literals
import os
import sys
import threading
from yt_dlp import YoutubeDL
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Graphics.ui", self)
        self.show()
        self.setWindowTitle("Youtube Downloader")
        self.std_download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.button_set.clicked.connect(self.set_button)
        self.button_download.clicked.connect(self.download_button)
        self.input_path.setText(self.std_download_path)
        self.radio_single.setChecked(True)
        self.progress_bar.setValue(0)
        self.cancel_flag = False

    def set_button(self):
        file_name = QFileDialog.getExistingDirectory()
        if file_name:
            self.input_path.setText(file_name)

    def download_button(self):
        self.cancel_flag = False
        url = self.input_url.text()
        save_path = self.input_path.text()
        quality = self.combo_quality.currentText()
        self.progress_bar.setValue(0)

        download_thread = threading.Thread(
            target=self.download_thread, args=(url, save_path, quality), daemon=True
        )
        download_thread.start()

    def download_thread(self, url, save_path, quality):
        playlist = not self.radio_single.isChecked()
        video_format = self.check_video.isChecked()

        try:
            downloader = Download(
                url, save_path, quality, video_format, playlist, self.update_progress, self.cancel_flag
            )
            song_title = downloader.download()
            self.input_url.setText("")
            self.label_done.setText(f"Downloaded: {song_title}")
            self.show_notification(f"Downloaded: {song_title}")
        except Exception as e:
            self.input_url.setText("")
            self.label_done.setText(f"Error: {str(e)}")

    def update_progress(self, progress):
        """Update the progress bar dynamically."""
        self.progress_bar.setValue(progress)

    def show_notification(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Notification")
        msg.exec_()


class Download(object):
    def __init__(self, url, save_path, quality, video_format, playlist, progress_callback, cancel_flag):
        self.url = url
        self.save_path = save_path
        self.qualities = {"Best": "320", "Semi": "192", "Worst": "128"}
        self.video_format = video_format
        self.quality = self.qualities.get(quality, "192")
        self.playlist = playlist
        self.progress_callback = progress_callback
        self.cancel_flag = cancel_flag

    @property
    def video_opts(self):
        return {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "noplaylist": not self.playlist,
            "progress_hooks": [self.hook],
        }

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
            "progress_hooks": [self.hook],
        }

    def hook(self, d):
        """Progress hook for yt-dlp."""
        if self.cancel_flag:
            raise Exception("Download canceled by user.")
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes", None) or d.get("total_bytes_estimate", None)
            if total:
                percentage = downloaded / total * 100
                self.progress_callback(int(percentage))
        elif d["status"] == "finished":
            self.progress_callback(100)

    def download(self):
        options = self.video_opts if self.video_format else self.song_opts
        with YoutubeDL(options) as download_object:
            info = download_object.extract_info(self.url, download=False)
            song_name = info.get("title", "Unknown Title")
            download_object.download([self.url])
            return song_name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setWindowIcon(QtGui.QIcon("logo.ico"))
    sys.exit(app.exec_())
