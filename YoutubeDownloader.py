from __future__ import unicode_literals
import os
import sys
import threading
from yt_dlp import YoutubeDL
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


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

    def set_button(self):
        file_name = QFileDialog.getExistingDirectory()
        if file_name:
            self.input_path.setText(file_name)

    def download_button(self):
        url = self.input_url.text()
        save_path = self.input_path.text()
        quality = self.combo_quality.currentText()
        download = threading.Thread(
            target=self.download_thread, args=(url, save_path, quality), daemon=True
        )
        download.start()

    def download_thread(self, url, save_path, quality):
        playlist = not self.radio_single.isChecked()
        video_format = self.check_video.isChecked()

        try:
            downloader = Download(url, save_path, quality, video_format, playlist)
            downloader.download()
            self.input_url.setText("")
            self.label_done.setText("Download Done!")
        except Exception as E:
            self.input_url.setText("")
            self.label_done.setText(str(E))


class Download(object):
    def __init__(self, url, save_path, quality, video_format, playlist=False):
        self.url = url
        self.save_path = save_path
        self.qualities = {"Best": "320", "Semi": "192", "Worst": "128"}
        self.video_format = video_format
        self.quality = self.qualities.get(quality, "192")
        self.playlist = playlist

    @property
    def video_opts(self):
        return {
            "verbose": False,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "noplaylist": not self.playlist,
        }

    @property
    def song_opts(self):
        return {
            "verbose": False,
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
        }

    def download(self):
        options = self.video_opts if self.video_format else self.song_opts
        with YoutubeDL(options) as download_object:
            info = download_object.extract_info(self.url, download=False)
            song_name = info.get("title", None)
            window.label_done.setText(song_name)
            download_object.download([self.url])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setWindowIcon(QtGui.QIcon("logo.ico"))
    sys.exit(app.exec_())
