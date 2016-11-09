from bluetooth import *
from uuid import getnode as get_mac
import time


def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = ''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))


# loop forever, try to find, retry in 1 second
while 1 == 1:
    hostname = "192.168.1.3"  # maybe?
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        print "performing bt inquiry... for(" + sys.argv[1] + ")"
        nearby_devices = discover_devices(lookup_names=True)
        for addr, name in nearby_devices:
            if name == sys.argv[1]:
                wake_on_lan(get_mac())  # wont work, need to get host address
                print "Sending WOL Magic Packet to: %s - %s" % (addr, name)
    time.sleep(1000)
