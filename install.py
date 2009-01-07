#!/usr/bin/python
import os
import sys
import shutil
import time
import commands
import re
current_directory = os.getcwd()
destination_directory = '/usr/local/thinliquidfilm'
print '*************************************'
print '      installing thinliquidfilm'
print '*************************************'
print ''
print ''
print '-------------------------'
print 'Checking dependencies ...'
print '-------------------------'
print ''
try:
    import qt
    print 'pyqt is present'
except:
    print 'Couldn\'t find pyqt.  thin liquid film will not work without pyqt.  Aborting installation.'
    sys.exit()
print ''
if os.popen('which ffmpeg').read() == '':
    print 'Couldn\'t find ffmpeg.  thin liquid film will not work without ffmpeg.  Aborting installation.'
    sys.exit()
else:
    print 'ffmpeg is present'
    print ''
codec_errors = 0
cmd = ('ffmpeg -formats')
output = commands.getoutput(cmd)
match = re.findall('xvid', output)
if len(match) > 0:
    print 'ffmpeg supports xvid'
else:
    print 'ffmpeg does not support xvid.  thin liquid film will not be able to read or encode xvid video files.'
    codec_errors += 1
print ''
match = re.findall('h264', output)
if len(match) > 0:
    print 'ffmpeg supports h264'
else:
    print 'ffmpeg does not support h264.  thin liquid film will not be able to read or encode h264 video files.'
    codec_errors += 1
if codec_errors == 2:
    print 'ffmpeg does not support either xvid or h264.  thin liquid film will not work without one of those codecs being supported by ffmpeg.  Aborting installation.'
    sys.exit()
print ''
cmd = 'ls -l /bin/sh'
output = commands.getoutput(cmd)
match = re.findall('dash', output)
if len(match) == 0:
    print 'using bash as shell'
    print ''
else:
    print 'You are not using "bash" as your default shell.  This is most likely because you are using Ubuntu which links the default shell to the "dash" shell.  See http://liquidweather.net/howto/index.php?id=59 on how to fix this.  thinliquidfilm won\'t work properly unless you fix this.'
    sys.exit()
try:
    import gpod
    print 'libgpod python bindings are present'
except:
    print 'Couldn\'t find libgpod python bindings.  You will need to install libgpod, and its python bindings to be able to upload videos to your ipod from thin liquid film'
print ''
if os.popen('which mplayer').read() == '':
    print 'Couldn\'t find mplayer.  Without mplayer, you will not be able to preview encoded videos.'
else:
    print 'mplayer is present'
print ''
try:
    child = os.popen('which konqueror')
    data = child.read()
    data = data.replace('\n','')
    data = data.split('/')
    ind = data.index('bin')
    kdedir = data[:ind]
    kdedir = '/'.join(kdedir)
    print 'konqueror is present'
    havekonq = 1
except:
    print 'Couldn\'t find konqueror.  Servicemenus will not be installed.'
    havekonq = 0
print ''
print '--------------------------------------------'
print 'Checking permissions for install process ...'
print '--------------------------------------------'
print ''
# check we are root
child = os.popen('touch /usr/local/test_thinliquidfilm &> /dev/null')
err = child.close()
if err:
    print 'You need to login as root to run this installation script.  You can do this by typing \'su\' at the command line, and then entering your root password.  If you are using *ubuntu, you should run this script with the command: \'sudo ./install.py\''
    sys.exit()
else:
    print 'Permissions OK'
print ''
time.sleep(1.0)
print '------------------------------'
print 'Clearing old installations ...'
print '------------------------------'
#clear old installs
if os.path.isfile(kdedir + '/share/apps/konqueror/servicemenu/thinliquidfilm.desktop'):
    print 'Removing ' + kdedir + '/share/apps/konqueror/servicemenu/thinliquidfilm.desktop sevicemenu'
    os.remove(kdedir + '/share/apps/konqueror/servicemenu/thinliquidfilm.desktop')
if os.path.isfile('/usr/local/bin/thinliquidfilm'):
    print 'Removing symlink to main application'
    os.remove('/usr/local/bin/thinliquidfilm')
if os.path.exists('/usr/local/thinliquidfilm'):
    print 'Removing /usr/local/thinliquidfilm directory'
    shutil.rmtree('/usr/local/thinliquidfilm')
print ''
print 'Old installations cleared'
print ''
time.sleep(1.0)
print '---------------------------------------------------'
print 'Copying ' + current_directory + ' to /usr/local ...'
shutil.copytree(current_directory,destination_directory)
print '---------------------------------------------------'
print ''
print 'Directory copied'
print ''
time.sleep(1.0)
print '---------------------------------------------'
print 'Creating symlink to main application file ...'
print '---------------------------------------------'
os.symlink('/usr/local/thinliquidfilm/thinliquidfilm.py','/usr/local/bin/thinliquidfilm')
print ''
print 'Symlink created'
print ''
time.sleep(1.0)
if havekonq == 1:
    print '---------------------------------------'
    print 'Creating thinliquidfilm servicemenu ...'
    print '---------------------------------------'
    if os.path.isdir(kdedir + '/share/apps/konqueror/servicemenus/'):
        shutil.copyfile('/usr/local/thinliquidfilm/thinliquidfilm.desktop',kdedir + '/share/apps/konqueror/servicemenus/thinliquidfilm.desktop')
        print ''
        print 'Servicemenu created'
    else:
        print ''
        print 'Couldn\'t find servicemenu directory.  Servicemenu entry not installed.  You can install it manuall by copying the file "thinliquidfilm.desktop" from the install directory to the directory where konqueror\'s service menus are stored.'
    print ''
    print ''
print '*************************************'
print '      thinliquidfilm installed'
print '*************************************'
