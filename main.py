import re
import os
import urllib.request
import subprocess
import tarfile
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
            self.arches = input("What's your arch? (x86-64bit or x86-32bit): ")
            # checking if choice the user wrote x86..
            if not "x86-32bit" ==  self.arches:
                # checking if the user wrote x86_64..
                if not "x86-64bit" == self.arches:
                    raise WrongArch

            return(self.arches)

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


class Stage():
            
    def get(self):
        self.arches = Arch().check()
        if self.arches == "x86-32bit":
            arches_list = ["amd64-k8_32", "athlon-xp", "atom_32", "core2_32", "generic_32", "i686", "pentium4"]
        if self.arches == "x86-64bit":
            arches_list = ["amd64-k8", "amd64-k10", "atom_64", "core2_64", "corei7", "generic_64"]
        number = 0
        for stage3 in arches_list:
            print(number,"-", stage3)
            number = number + 1

        self.optimi_number = input("Enter your choice (just input the number): ")
        self.arches_list = arches_list
        print(self.arches, self.arches_list[int(self.optimi_number)])
        try:
            print("Downloaded of the stage3 archive started...")
            urllib.request.urlretrieve("http://ftp.osuosl.org/pub/funtoo/funtoo-current/{0}/{1}/stage3-latest.tar.xz".format(self.arches, self.arches_list[int(self.optimi_number)]), filename="/mnt/gentoo/stage3-latest.tar.xz")
        except PermissionError:
            print("Are you root?")


    def extract(self, path="/mnt/gentoo/stage3-latest.tar.bz2"):
        stage3 = tarfile.open(name=path, mode='r|*')
        stage3.extractall(path="/mnt/gentoo")

class Tree():
    def get(self):
        subprocess.call("emerge --sync", shell=True)

class pre_chroot():
    def proc():
        subprocess.call("mount --bind /proc /mnt/gentoo/proc", shell=True)

    def dev():
        subprocess.call("mount --bind /dev /mnt/gentoo/dev", shell=True)


# Funtoo
class Configure():
    def fstab():
        subprocess.call("nano /etc/fstab", shell=True)

    def localtime():
        subprocess.call("nano /etc/localtime", shell=True)

    def portage():
        subprocess.call("nano /etc/make.conf", shell=True)

    def keymaps():
        subprocess.call("nano /etc/conf.d/keymaps", shell=True)

    def clock():
        subprocess.call("nano /etc/conf.d/hwclock", shell=True)

    def root_passwd():
        print("Configuring root password")
        subprocess.call("passwd root", shell=True)

    def bootloader():
        asw = input("Do you want to emerge boot-update? (yes or no): ")
        if "yes" == asw:
            subprocess.call("emerge boot-update", shell=True)

    def kernel():
        print("I'll build the debian-sources kernel with the binary useflag for you")
        print("Doing this requires 12GB of space in /var/tmp")
        subprocess.call("df -h /var/tmp", shell=True)
        input("Do you have enough place? If you have, just press enter. If you don't, exit the script with CTRL-C and deal with the kernel yourself!")
        packageuse = open("/etc/portage/package.use", "a")
        packageuse.write("# The following line was added by funinstall")
        packageuse.write("sys-kernel/debian-sources binary")
        
            
Partition().check()            
Partition().mount()
Stage().get()
Stage().extract()
pre_chroot().proc()
pre_chroot().dev()
os.chroot("/mnt/gentoo")
Configure().fstab()
Configure().portage()
