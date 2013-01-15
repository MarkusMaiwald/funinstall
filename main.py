import re
import os
import urllib.request
import subprocess
import shutil
import tarfile

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# Exceptions
class WrongArch(Exception):
    pass

# Welcome
print("-")
print("Welcome to my highly experimental Gentoo/Funtoo installation program")
print("-")

# Check distro


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

    def format(self):
        if "yes" == input("Do you want me to format partition for you?"):
            while True:
                subprocess.call(["fdisk", "-l"])
                partition = input("Please enter the partition that you want to format (in the form '/dev/xxx': ")
                filesystem = input("Please enter the filesystem that you want to use on the previous partition (ext2, ext3 or ext4): ")
                print("I'll format {0} with the {1} filesystem".format(partition, filesystem))
                if "yes" == input(bcolors.WARNING + "Are you sure you want to do this? (yes or no): " + bcolors.ENDC):
                    subprocess.call("mkfs.{0} {1}".format(filesystem, partition), shell=True)

                if "no" == input("Do you want to format another partition? (yes or no): "):
                    break
        

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


    def extract(self, path="/mnt/gentoo/stage3-latest.tar.xz"):
        stage3 = tarfile.open(name=path, mode='r|*')
        stage3.extractall(path="/mnt/gentoo")

class Tree():
    def get(self):
        subprocess.call("emerge --sync", shell=True)

class pre_chroot():
    def proc(self):
        subprocess.call("mount --bind /proc /mnt/gentoo/proc", shell=True)

    def dev(self):
        subprocess.call("mount --bind /dev /mnt/gentoo/dev", shell=True)


# Funtoo
class Configure():
    def mtab(self):
        subprocess.call("grep -v rootfs /proc/mounts > /etc/mtab", shell=True)
    def fstab(self):
        subprocess.call("nano /etc/fstab", shell=True)

    def localtime(self):
        subprocess.call("nano /etc/localtime", shell=True)

    def portage(self):
        subprocess.call("nano /etc/make.conf", shell=True)
        subprocess.call("emerge --sync", shell=True)

    def keymaps(self):
        subprocess.call("nano /etc/conf.d/keymaps", shell=True)

    def clock(self):
        subprocess.call("nano /etc/conf.d/hwclock", shell=True)

    def root_passwd(self):
        print("Configuring root password")
        subprocess.call("passwd root", shell=True)
    def keep_internet(self):
        shutil.copy2("/etc/resolv.conf", "/mnt/gentoo/etc/resolv.conf")
        

    def bootloader(self):
        asw = input("Here's a quick description of what boot-update is:\n-\nboot-update provides a unified mechanism for configuring the GRUB 1.9x (sys-boot/grub) and GRUB 0.97 (sys-boot/grub-legacy) boot loaders.\n-\nDo you want to install it? (yes or no): ")
        if "yes" == asw:
            subprocess.call("emerge boot-update", shell=True)

        if "yes" == input("Do you want to install grub? (yes or no): "):
            subprocess.call(["emerge", "grub"])

        

    def kernel(self):
        # print("I'll build the debian-sources kernel with the binary useflag for you")
        # print("Doing this requires 12GB of space in /var/tmp")
        packageuse = open("/etc/portage/package.use", "a")
        ## Right now Mon Jan 14 2013 genkernel fail with debian-sources +binary
        ## So i'll use gentoo-sources instead :)
        # packageuse.write("# The following line was added by funinstall")
        # packageuse.write("\nsys-kernel/debian-sources binary")
        packageuse.write("# The following line was added by funinstall")
        packageuse.write("\nsys-kernel/gentoo-sources symlink")
        subprocess.call(["emerge", "gentoo-sources"])
        print(bcolors.WARNING + "Only the sources of the kernel is installed. You have to go where the sources are (typically /usr/src/linux) and configure the kernel to your needs (typically with make menuconfig).\nThen, you have to copy the kernel images to your boot parition and edit your bootloader so it will find it." + bcolors.ENDC)
    
            
#Partition().check()            
Partition().format()
#Stage().extract()
#pre_chroot().proc()
#pre_chroot().dev()
#Configure().keep_internet()
#os.chroot("/mnt/gentoo")
#Configure().fstab()
#Configure().portage()
Configure().bootloader()
#Configure().kernel()
