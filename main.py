# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os, getpass, shutil, subprocess

# pip instal easygui
import easygui
# pip install qdarkgraystyle
# import qdarkgraystyle

# pip install pytube
from pytube import YouTube

# pip install youtube-dl
import youtube_dl

import imageio

title = 'J-Media Player'
version = 'v0.1'
username = getpass.getuser()
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle(title + ' ' + version) 
        self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)
        
        # Create new action 
        downloadAction = QAction('&Download Youtube Video', self)     
        downloadAction.setStatusTip('Download youtube video')
        downloadAction.triggered.connect(self.youtubeDownloadPopup)
        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(downloadAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        
        # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
        # Force the style to be the same on all OSs:
        app.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")
        if fileName.endswith('.mp4'):
            reader = imageio.get_reader(fileName)
            fps = reader.get_meta_data()['fps']
            fileName = fileName.replace('.mp4', '.avi')
            writer = imageio.get_writer(fileName, fps=fps)
            for im in reader:
                writer.append_data(im[:, :, :])
            writer.close()
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        self.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
    
    def youtubeDownloadPopup(self):
        # self.close()
        self.youtube_download_popup = youtube_download('Download Youtube Video')
        self.youtube_download_popup.setFixedSize(300, 310)
        self.youtube_download_popup.setWindowTitle('Download Youtube Video')
        # self.youtube_download_popup.setWindowIcon(QtGui.QIcon('add.png'))
        self.youtube_download_popup.show()

class youtube_download(QDialog):
    def __init__(self, name):
        super().__init__()
        self.title = name
        # TEXT BOX START
        self.txtURL = QLineEdit(self)
        self.txtURL.move(10,10)
        self.txtURL.resize(250,30)
        # TEXT BOX END
        # LABEL START
        self.lblTitle = QLabel(self)
        self.lblTitle.move(10,100)
        self.lblTitle.resize(250,30)
        self.lblTitle.setText("Title: ")
        # LABEL END
        # BUTTON START
        self.btnDownload = QPushButton(self)
        self.btnDownload.setText('Download')
        self.btnDownload.move(10,60)
        self.btnDownload.clicked.connect(self.downloadYoutube)
        # BUTTON END
    def downloadYoutube(self):
        try:
            directory = 'C:/Users/{}/Videos/J-Media Player Downloads'.format(username)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            url = self.txtURL.text()
            if 'https://www.youtube.com/watch?' not in url:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
                return
            ydl_opts = {}
            info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download = False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            self.lblTitle.setText("Title: " + str(video_title))
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            shutil.move(video_title + '-' + video_id + '.mp4', directory + '/' + video_title + '.mp4')
            buttonReply = QMessageBox.information(self, 'Success! :)', "Succesfully downloaded!\nDo you want to open the file directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.explore(directory)
        except Exception as e:
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(800, 400)
    player.show()
    sys.exit(app.exec_())
