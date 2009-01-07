import commands
import re

def getInfo(file):
    try:
        cmd = ('ffmpeg -i "%s" -vframes 10 -vcodec mpeg4 -r 29.970030 -b 768k -ar 24000 -ab 128k -s 320x180 -f avi - > /dev/null' %(file))
        output = commands.getoutput(cmd)

        regexp = r'''(?isx).*?Duration:\s(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}.\d)'''
        match = re.search(regexp, output)
        hours = int(match.group('hours'))
        minutes = int(match.group('minutes'))
        seconds = float(match.group('seconds'))

        regexp = r'''(?isx).*?bitrate:\s(?P<bitrate>.*?)\s|$'''
        match = re.search(regexp, output)
        bitrate = match.group('bitrate')

        regexp = r'''(?isx).*?Video:\s(?P<type>.*?),\s'''
        match = re.search(regexp, output)
        type = match.group('type')

        regexp = r'''(?isx).*?,\s(?P<width>\d*?)x(?P<height>\d*?)\s'''
        match = re.search(regexp, output)
        aspect = str(float(match.group('width'))/float(match.group('height')))[:6]
        size = match.group('width') + 'x' + match.group('height')

        regexp = r'''(?isx).*?\s(?P<fps>\d{1,2}\.\d{1,2})\stb'''
        match = re.search(regexp, output)
        fps = float(match.group('fps'))
        length = int((hours*3600 + minutes*60 + seconds)*1000)
        frames = int((hours*3600 + minutes*60 + seconds)*fps)
        values = [type,frames,aspect,bitrate,length,size]
        return values
    except:
        return 'parsing error'
