def fractSec(s):
       years, s = divmod(s, 31556952)
       min, s = divmod(s, 60)
       h, min = divmod(min, 60)
       d, h = divmod(h, 24)
       return years, d, h, min, s 
