from lamda.client import *


def kuaishouspider():
    d = Device("192.168.9.6")
    d.application("com.kuaishou.nebula")
    print(d)




kuaishouspider()
