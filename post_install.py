#!/usr/bin/env python
import os


def question(sentence, default=True):
    answer = False
    yes = ['yes', 'y']
    no = ['no', 'n']
    if default:
        yes.append('')
        key_indicator = " [Y/n] "
    else:
        no.append('')
        key_indicator = " [y/N] "
    while not answer:
        choice = raw_input(str(sentence) + key_indicator).lower()
        if choice in yes:
            answer = True
            return True
        elif choice in no:
            answer = True
            return False


def ask_pkg(sentence, main, main_list, default=True):
    response = question(sentence, default=default)
    if response:
        if type(main) == list:
            for item in main:
                main_list.append(item)
        elif type(main) == str:
            main_list.append(main)
    return response


def sources_creator(contrib=True, nonfree=True, jessie_backports=True):
    jessie = "deb http://httpredir.debian.org/debian jessie main"
    security = "deb http://security.debian.org/ jessie/updates main"
    if contrib:
        jessie += " contrib"
        security += " contrib"
    if nonfree:
        jessie += " non-free"
        security += " non-free"
    jessie_src = jessie[:3] + "-src" + jessie[3:]
    security_src = security[:3] + "-src" + security[3:]
    os.system('echo "' + jessie + '" | sudo tee /etc/apt/sources.list ' +
              '> /dev/null')
    os.system('echo "' + jessie_src + '" | sudo tee --append ' +
              '/etc/apt/sources.list > /dev/null')
    os.system('echo "\n' + security + '" | sudo tee --append ' +
              '/etc/apt/sources.list > /dev/null')
    os.system('echo "' + security_src + '" | sudo tee --append ' +
              '/etc/apt/sources.list > /dev/null')
    if jessie_backports:
        line = "deb http://httpredir.debian.org/debian jessie-backports main"
        line_src = line[:3] + "-src" + line[3:]
        os.system('echo "\n' + line + '" | sudo tee --append ' +
                  '/etc/apt/sources.list > /dev/null')
        os.system('echo "' + line_src + '" | sudo tee --append ' +
                  '/etc/apt/sources.list > /dev/null')


xfce_basics_pkg = ["gtk2-engines-murrine", "light-locker",
                   "gnome-system-tools", "xfce4-whiskermenu-plugin",
                   "gdebi", "gksu", "catfish", "gnome-system-monitor",
                   "qt4-qtconfig", "gigolo",
                   "gparted", "gnome-disk-utility", "wipe"]

utilities = ["unrar-free", "grsync", "firefox-esr-l10n-es-ar",
             "icedtea-plugin", "locate", "libreoffice-l10n-es", "samba",
             "gvfs-backends", "curl", "cryptsetup", "git", "htop"]

python_pkg = ["ipython", "ipython-notebook", "pyflakes", "python-rope",
              "python-numpy", "python-scipy", "python-matplotlib",
              "python-pip", "python-gi", "python-gi-cairo",
              "python-mpltoolkits.basemap", "python-pyproj", "pep8"]

latex_pkg = ["texlive", "texlive-latex-extra", "texlive-lang-spanish",
             "texlive-lang-english"]

main = []
backports = []
extra_commands = []

# packages
os.system("clear")
print "Packages Management"
sources = question("Create /etc/apt/sources.list?")
if sources:
    contrib = question("\tadd contrib?")
    nonfree = question("\tadd non-free?")
    jessie_backports = question("\tadd jessie-backports?")
    sources_creator(contrib=contrib, nonfree=nonfree,
                    jessie_backports=jessie_backports)

update = question("Update packages' list?")
upgrade = question("Upgrade packages?")
if upgrade:
    distupgrade = question(" L---> Dist-Upgrade packages?")
if upgrade and not update:
    print "WARNING: Package list must be updated before upgrading system."
    upgrade = question("Upgrade anyway?", default=False)


# xfce
os.system("clear")
print "XFCE"
response = ask_pkg("Install basics main for a better XFCE experience?",
                   xfce_basics_pkg, main)
if response:
    extra_commands.append("sudo apt-get install --no-install-recommends " +
                          "file-roller && sudo apt-get purge xarchiver")
    extra_commands.append("sudo apt-get purge xscreensaver")


# utilities
os.system("clear")
print "Utilities"
ask_pkg("Install usefull utilities?", utilities, main)
other_utils = {"Geany (jessie-backports)": [["geany", "geany-plugins"], backports],
			   "unrar (non-free)": ["unrar", main],
               "synapse (jessie-backports)": ["synapse", backports],
               "owncloud (jessie-backports)":
                   [["owncloud-client", "owncloud-client-l10n"], backports],
               "Python related packages?": [python_pkg, main],
               "wine": [["wine", "winetricks"], main],
               "VirtualBox": ["virtualbox", main],
               "Pavucontrol and GStreamer0.10-pulseaudio":
                   [["pavucontrol", "gstreamer0.10-pulseaudio"], main],
               "GnuCash": ["gnucash", main]
               }
for key in other_utils.keys():
    ask_pkg("Install " + key + "?", other_utils[key][0], other_utils[key][1])


# multimedia main
os.system("clear")
print "Multimedia"
multimedia = {"SMPlayer": ["smplayer", main],
              "VLC": ["vlc", main],
              "Chromium": ["chromium", main],
              "Icedove (Debian's Thunderbird)": ["icedove", main],
              "Banshee": ["banshee", main],
              "Inkscape": ["inkscape", main],
              "Darktable": ["darktable", backports],
              "Shotwell": ["shotwell", main],
              "Deluge": ["deluge", backports],
              "MuseScore": ["musescore", backports]
              }

for key in multimedia.keys():
    ask_pkg("Install " + key + "?", multimedia[key][0], multimedia[key][1])


# science and office
os.system("clear")
print "Science and Office"
science = {"LaTeX": [latex_pkg, main],
           "Microsoft Fonts (non-free)": ["ttf-mscorefonts-installer", main],
           "KBibTex": ["kbibtex", main],
           "Jabref": ["jabref", main],
           "GMT 5 (jessie-backports)": ["gmt gmt-doc gmt-gshhg", backports],
           "wxmaxima": ["wxmaxima", main],
           "QtiPlot": ["qtiplot", main]
           }
for key in science.keys():
    ask_pkg("Install " + key + "?", science[key][0], science[key][1])


# networks and security
os.system("clear")
print "Networks and Security"
network = {"gufw firewall": ["gufw", main],
           "nmap": ["nmap", main],
           "netdiscover": ["netdiscover", main],
           "Tor Browser": ["torbrowser-launcher", main],
           "gpg and seahorse": [["gnupg", "gnupg-curl", "seahorse"], main],
           "KeePassX (Password Manager)": ["keepassx", backports],
           "PWGen (Password Generator)": ["pwgen", main]
           }
for key in network.keys():
    ask_pkg("Install " + key + "?", network[key][0], network[key][1])


# INSTALLATION:
# update & upgrade
if update:
    os.system("clear")
    print "Updating packages"
    os.system("sudo apt-get update")
if upgrade:
    os.system("clear")
    if distupgrade:
        print "Dist-upgrading packages"
        os.system("sudo apt-get dist-upgrade")
    else:
        print "Upgrading packages"
        os.system("sudo apt-get upgrade")

# main
if len(main) > 0:
    line = "sudo apt-get install "
    for item in main:
        line += item + " "
    os.system("clear")
    print "Installing packages"
    os.system(line)

# backports
if len(backports) > 0:
    line = "sudo apt-get install -t jessie-backports "
    for item in backports:
        line += item + " "
    os.system("clear")
    print "Installing jessie-backports packages"
    os.system(line)

# extra commands
if len(extra_commands) > 0:
    for line in extra_commands:
        os.system("clear")
        print "Other commands:"
        print line
        os.system(line)

if "torbrowser-launcher" in main:
    os.system("clear")
    print "TorBrowser Launcher"
    os.system("torbrowser-launcher")

# --------------------------------------------------------------------------

# configurations
os.system("clear")
print "Configurations"
bin_dir = question("Create ~/bin directory?")
if bin_dir:
    os.system("mkdir ~/bin")
    path = question("Add ~/bin to PATH?")
    if path:
        home_path = os.getenv("HOME")
        bashrc_path = home_path + "/.bashrc"
        if os.path.isfile(bashrc_path):
            bashrc = open(bashrc_path, 'a')
            bashrc.write("\n" + u"export PATH=$PATH:" + home_path + u"/bin")
            bashrc.close()

response = question("Show users in lightdm?")
if response:
    os.system('cat /usr/share/lightdm/lightdm.conf.d/' +
              '01_debian.conf | sed "s/greeter-hide-users=' +
              '.*/greeter-hide-users=false/g" | ' +
              'sudo tee /usr/share/lightdm/lightdm.conf.d/' +
              '01_debian.conf')
