from lamda.client import Device
d = Device("192.168.9.6")

r=  d.start_activity(**{"component": "org.telegram.messenger.web/org.telegram.messenger.DefaultIcon"})

print(r)