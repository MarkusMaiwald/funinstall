import re
import os
import urllib.request
import subprocess
import shutil
import tarfile
import curses
import argparse
import glob
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

# Check distro


# Arch check
class Arch():
    def __init__(self):
        pass

    def check_funtoo(self):
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

    def check_gentoo(self):
        try:
            self.arches = input("What's your arch? (x86 or amd64): ")
            # checking if the user choosed x86...
            if not "x86" == self.arches:
                if not "amd64" == self.arches:
                    raise WrongArch
            return(self.arches)
        
        except WrongArch:
            print("You chose the wrong arch")

class Net():
    def __init__(self):
        pass

    def activate(self):
        print("I'll run dhcpcd on the network interface that you want\n")
        subprocess.call(["ifconfig", "-s"])
        net_device = input("\nPlease enter the network interface (enter no to cancel): ")
        if not net_device == "no":
            try:
                subprocess.check_call("dhcpcd {0}".format(net_device), shell=True)
                print(bcolors.HEADER + "dhcpcd successfully started on {0}".format(net_device) + bcolors.ENDC)
            except:
                print("You chose an", bcolors.WARNING + "incorrect internet device" + bcolors.ENDC, "or maybe", bcolors.WARNING + "dhcpcd is already running" + bcolors.ENDC, "on the interface that you specified")


class Partition():
    def __init__(self):
        pass

    def create(self):
        while True:
            subprocess.call(["fdisk -l"])
            c = input("\nOn what device you would like to create partitions? (enter no if you want to cancel - in the form /dev/xxx): ")
            if c == "no":
                break
            try:
                subprocess.check_call(["cfdisk", c])

                p = input("\n Do you want to create partitions on other hard drive? (yes or no)")
                if p == "no":
                    break

            except:
                print("Cfdisk failed to work on {0}".format(c))
                
            
                      
        
            
                            
        
                        

    def swap(self):
        subprocess.call(["fdisk", "-l"])
        swap_partition = input("\nPleaser enter the partition that you would like to format to swap (enter no if you want to cancel): ")
        while True:
            if "no" == swap_partition:
                break
            
            try:
                subprocess.check_call(["mkswap", swap_partition])
                break
            except:
                print("Mkswap failed on {0}".format(swap_partition))

    def format(self):
        while True:
            subprocess.call(["fdisk", "-l"])
            partition = input("Please enter the partition that you to format (in the form '/dev/xxx': ")
            filesystem = input("Please enter the filesystem that you want to use on the previous partition (enter no to cancel - ext2, ext3 or ext4): ")
            if "no" == filesystem:
                break
            print("I'll format {0} with the {1} filesystem\n".format(partition, filesystem))
            if "yes" == input(bcolors.WARNING + "Are you sure you want to do this? (yes or no): " + bcolors.ENDC):
                try:
                    subprocess.check_call("mkfs.{0} {1}".format(filesystem, partition), shell=True)
                except:
                    print("The formatting of {0} with the {1} filesystem failed.".format(partition,filesystem))
                
            if "no" == input("Do you want to format another partition? (yes or no): "):
                break
        

    def check(self):
        if not os.access("/mnt/gentoo", os.F_OK):
            os.mkdir("/mnt/gentoo")

    def mount(self):
        subprocess.call(["fdisk", "-l"])
        c = input("\nEnter here the partition that you want to mount at /mnt/gentoo  (typically your root partition, in the form /dev/xxx): ")
        try:
            subprocess.call(["mount", c, "/mnt/gentoo"])
            while True:
                c = input("Enter here any other partition that you would like to mount (in the form /dev/xxx -- enter no if you don't have others partition too mount): ")
                if c == "no":
                    break
                d = input("Enter the mount point of this partition (inside /mnt/gentoo. Ex: /mnt/gentoo/home): ")
                subprocess.check_call(["mount", c, d])
        except:
            print("Incorrect mount point or partition specified")
        

class Stage():
            
    def get_funtoo(self, url="http://ftp.osuosl.org/pub/funtoo/funtoo-current/{0}/{1}/stage3-latest.tar.xz"):
        # get the base name of the archive
        basename = os.path.basename(url)
        
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
            print("Downloading of the stage3 archive started...")
            urllib.request.urlretrieve("http://ftp.osuosl.org/pub/funtoo/funtoo-current/{0}/{1}/stage3-latest.tar.xz".format(self.arches, self.arches_list[int(self.optimi_number)]), filename="/mnt/gentoo/{0}".format(self.basename))
        except PermissionError:
            print("Are you root?")

    def get_gentoo(self):
        self.arch = Arch().check_gentoo()
        if "x86" == self.arch:
            self.arch2 = "i686"

        else:
            self.arch2 = "amd64"

        base_url = "http://distfiles.gentoo.org/releases/{0}/autobuilds/".format(self.arch)
        stage3_file = urllib.request.urlopen("http://distfiles.gentoo.org/releases/{0}/autobuilds/latest-stage3-{1}.txt".format(self.arch, self.arch2))
        stage3_file = stage3_file.readlines()[2]
        stage3_file = str(stage3_file)
        stage3_file = stage3_file.replace("\\n", "")
        stage3_file = stage3_file.replace("'", "")
        stage3_file = stage3_file[1:]
        full_stage3_url = "{0}{1}".format(base_url, stage3_file)
        # catch the name of the archive
        self.basename = os.path.basename("full_stage3_url")
        try:
            print("Downloading of the stage3 archive started...")
            urllib.request.urlretrieve(full_stage3_url, filename="/mnt/gentoo/{0}".format(self.basename))
        except:
            print ("Unexpected Error")
        


    def catch_stage3_name(self):
        return(glob.glob("/mnt/gentoo/stage3*")[0])
    

            
    def extract(self, path=Stage().catch_stage3_name()):
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
        # print("Doing this requires 12GB of space ind /var/tmp")
        packageuse = open("/etc/portage/package.use", "a")
        ## Right now Mon Jan 14 2013 genkernel fail with debian-sources +binary
        ## So i'll use gentoo-sources instead :)
        # packageuse.write("# The following line was added by funinstall")
        # packageuse.write("\nsys-kernel/debian-sources binary")
        packageuse.write("# The following line was added by funinstall")
        packageuse.write("\nsys-kernel/gentoo-sources symlink")
        subprocess.call(["emerge", "gentoo-sources"])
        print(bcolors.WARNING + "Only the sources of the kernel is installed. You have to go where the sources are (typically /usr/src/linux) and configure the kernel to your needs (typically with make menuconfig).\nThen, you have to copy the kernel images to your boot parition and edit your bootloader so it will find it." + bcolors.ENDC)        
    
parser = argparse.ArgumentParser(description='Installing a Gentoo/Funtoo system')
parser.add_argument("--config", action="store_true", help="Configure the needed file for your installation")
parser.add_argument("--partition", action="store_true", help="Configure partitions and mounts points")
parser.add_argument("--net", action="store_true", help="Activate the network if on a wired connection")
parser.add_argument("--getgentoo", action="store_true", help="Fetch the stage3 archive for Gentoo and save it in /mnt/gentoo")
parser.add_argument("--getfuntoo", action="store_true", help="Fetch the stage3 archive for Funtoo and save it in /mnt/gentoo")
parser.add_argument("--create-tree", action="store_true", help="Create an initial portage tree for your installation")
parser.add_argument("--full", action="store_true", help="Walk trough each step automatically")
args = parser.parse_args()


if args.config:
    pre_chroot().proc()
    pre_chroot().dev()
    os.chroot("/mnt/gentoo")
    Configure().mtab()
    COnfigure().fstab()
    Configure().localtime()
    Configure().portage()
    Configure().keymaps()
    Configure().clock()
    Tree().get()

if args.partition:
    Partition().check()
    Partition().format()
    Partition().format()

if args.getfuntoo:
    Stage().get_funtoo()
    Stage().extract()
    
if args.getgentoo:
    Stage().get_gentoo
    Stage().extract()
                    
if args.net:
    Net().activate()

if args.full:
    Net().activate()

    Partition().create()
    Partition().check()
    Partition().swap()
    Partition().format()
    Partition().mount()
    
    c = input("\nAre you installing funtoo or gentoo?")
    if c == "gentoo":
        Stage().get_gentoo()

    elif c == "funtoo":
        Stage().get_funtoo()

    else:
        print("Sorry, can't understand your answer")

    Stage().extract()

    pre_chroot().proc()
    pre_chroot().dev()

    Configure().keep_internet()

    os.chroot("/mnt/gentoo")
    Configure().mtab()
    Configure().fstab()
    Configure().localtime()
    Configure().portage()
    Configure().keymaps()
    Configure().clock()
    Configure().root_passwd()
    Tree().get()

#Stage().get_gentoo()
#Partition().check()            
#Partition().format()
#Stage().extract()
#pre_chroot().proc()
#pre_chroot().dev()
#Configure().keep_internet()
#os.chroot("/mnt/gentoo")
#Configure().fstab()
#Configure().portage()
#Configure().bootloader()
#Configure().kernel()
