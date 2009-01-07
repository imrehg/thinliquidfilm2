import os
import statvfs
import stat

# Returns bytes free space on filesystem at (dir)
def diskFree(dir):
    fs_stat = os.statvfs(dir)
    return fs_stat[statvfs.F_BSIZE] * fs_stat[statvfs.F_BFREE]

# Returns total disk space on filesystem at (dir)
def diskSpace(dir):
    fs_stat = os.statvfs(dir)
    return fs_stat[statvfs.F_BSIZE] * fs_stat[statvfs.F_BLOCKS]

# Get size of file on diskst
def fileSize(size_files):
    total = 0
    error_flag = 0
    for file in size_files:
        try:
            file_stat = os.stat(file)
            print 'file:'
            print file_stat
        except:
            error_flag += 1
        total += file_stat[stat.ST_SIZE] # add filesize to total
        print 'running total:'
        print total
    return total,error_flag

# Open ipod database

def checkSize(check_files,mountpoint):
    loc_filesize = fileSize(check_files)
    print "total size:"
    print loc_filesize[0]
    errors = loc_filesize[1]
    print "freespace:"
    print diskFree(mountpoint)
    if int(loc_filesize[0]) > int(diskFree(mountpoint)):
        size_ok = 0
    else:
        size_ok = 1
    return size_ok,errors
