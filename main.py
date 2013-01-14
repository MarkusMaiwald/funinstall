import re
import os
import urllib.request
import subprocess
# Exceptions
class WrongArch(Exception):
    pass

# Welcome
print("Welcome to my highly experimental Gentoo/Funtoo installation program.\nI'll ask you a couple of questions now.")

# Arch check
class Arch():
    def __init__(self):
        pass

    def check(self):
        try:
            self.arches = input("What's your arch? (x86_64 or x86): ")
            # checking if choice the user wrote x86..
            if not "x86" ==  self.arches:
                # checking if the user wrote x86_64..
                if not "x86_64" == self.arches:
                    raise WrongArch

        except WrongArch:
            print("You chose the wrong arch")


class Net():
    def __init__(self):
        pass

    def activate(self):
        print("If you are on a wired network, I can run dhcpcd for you on eth0 or any devices")
        net_device = input("Please enter the network interface (enter no if you want to skip this part) : ")
        if not net_device == "no":
            try:
                subprocess.check_call("dhcpcd {0}".format(net_device), shell=True)
                print("Running dhcpcd on {0}".format(net_device))
            except:
                print("You probably choosed a wrong internet device, this is why it just failed!")


class Partition():
    def __init__(self):
        pass

    def check(self):
        if not os.access("/mnt/gentoo", os.F_OK):
            os.mkdir("/mnt/gentoo")
            print("Mount point /mnt/gentoo created")

    def mount(self):
        subprocess.call("fdisk -l", shell=True)
        input("Now open a seperate terminal and go mount your root parition on /mnt/gentoo and any other partition\nPress enter here when you are done. ")
        print("At this point, all your parition should be mounted at the appropriate mountpoint")
        
        
                    
            
            
        
        

Partition().mount()
