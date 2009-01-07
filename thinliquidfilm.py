#!/usr/bin/python

from qt import *
from main import *
import sys
import os
import commands
import re
import uploadFileInfo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.argv.pop(0)
    print sys.argv
    processed_files = []
    if len(sys.argv) > 0:
        for i in sys.argv:
            if i[0] == '~':
                os.path.expanduser(i)
            if i[0] != '/':
                i = os.getcwd() + '/' + i
            processed_files.append(i)
    f = main()
    codec_errors = 0
    cmd = ('ffmpeg -formats')
    output = commands.getoutput(cmd)
    match = re.findall('xvid', output)
    if len(match) > 0:
        print 'ffmpeg supports xvid'
        f.comboCodec.insertItem('xvid',0)
    else:
        print 'ffmpeg does not support xvid.  thin liquid film will not be able to read or encode xvid video files.'
        codec_errors += 1
    match = re.findall('h264', output)
    if len(match) > 0:
        print 'ffmpeg supports h264'
        f.comboCodec.insertItem('h264',-1)
    else:
        print 'ffmpeg does not support h264.  thin liquid film will not be able to read or encode h264 video files.'
        codec_errors += 1
    if codec_errors == 2:
        print "ffmpeg does not support either xvid or h264.  thin liquid film will not work without one of those codecs being supported by ffmpeg.  thin liquid film will exit."
        os.system('kdialog --title "FFMPEG dependency failure" --error "ffmpeg does not support either xvid or h264.  thin liquid film will not work without one of those codecs being supported by ffmpeg.  thin liquid film will exit."')
        sys.exit()
    f.home_directory = os.popen("echo $HOME").readline()[0:-1]
    f.config_directory = f.home_directory + '/.thinliquidfilm'
    try:
        os.mkdir(f.config_directory)
    except(OSError):
        pass
    f.file_paths = []
    f.encodeSettings = []
    f.transferSettings = []
    f.frames = []
    f.version = 1.00
    f.listView2.setSorting(-1)
    f.listView3.setSorting(-1)
    f.currentList = f.listView3
    f.tabWidget2.setTabEnabled(f.tabWidget2.page(1),False)
    f.Upload.setDisabled(True)
    f.groupBox1.setDisabled(True)
    f.groupBox3.setDisabled(True)
    f.ipodInfo.setDisabled(True)
    f.Upload.setDisabled(True)
    f.lineDestination.setText(f.home_directory)
    if os.path.exists(f.config_directory + '/defaults'):
        from ConfigParser import RawConfigParser
        config = RawConfigParser()
        config.read(f.config_directory + '/defaults')
        if config.get('Main','passes') == '1':
            f.radioOnePass.setChecked(True)
        else:
            f.radioTwoPass.setChecked(True)
        if config.get('Main','quality') == '0':
            f.radioiPod.setChecked(True)
        else:
            f.radioTV.setChecked(True)
        f.comboCodec.setCurrentText(config.get('Main','codec'))
        if config.get('Main','audio') == '128':
            f.radioAudioLow.setChecked(True)
        else:
            f.radioAudioHigh.setChecked(True)
        f.lineDestination.setText(config.get('Main','destination'))
    if os.path.exists(f.config_directory + '/mountpoint'):
        from ConfigParser import RawConfigParser
        config = RawConfigParser()
        config.read(f.config_directory + '/mountpoint')
        f.lineMountpoint.setText(config.get('Main','mountpoint'))
    f.tabWidget3.setCurrentPage(0)
    if len(sys.argv) > 0:
        f.fileAdded(processed_files)
    f.checkVersion()
    f.show()
    app.setMainWidget(f)
    app.exec_loop()
