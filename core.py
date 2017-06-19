import os
import sys


DISTRIBUTIONS = ["stretch", "jessie", "jessie-backports", "sid", "wheezy",
                 "wheeze-backports", "oldstable", "stable", "testing",
                 "unstable"]

AREAS = ["main", "contrib", "non-free"]


class SourcesCreator(object):
    def __init__(self):
        self.httpredir = "deb http://httpredir.debian.org/debian"
        self.httpredir_src = "deb-src http://httpredir.debian.org/debian"

    def add_repos(self, dists, areas, overwrite=False):
        lines = []
        blank = ""
        title = "# Lines added by Debian Post Installation Script"
        if overwrite:
            symbol = 'w'
        else:
            symbol = 'a'
            lines.append(blank)
        for dist in dists:
            line1 = self.httpredir + " " + dist
            line2 = self.httpredir_src + " " + dist
            for area in areas:
                line1 += " " + area
                line2 += " " + area
            lines.append(title)
            lines.append(line1)
            lines.append(line2)
            lines.append(blank)
        with open("/etc/apt/sources.list", symbol) as sources:
            sources.write('\n'.join(lines))


class PackagesInstaller(object):
    def __init__(self):
        self.install_packages = {}

    def read(self, packages_filename):
        distribution = ""
        title = ""
        titles = []
        packages = {}
        try:
            os.path.isdir(packages_filename)
        except:
            return None, None
        with open(os.path.join(".", packages_filename)) as pkgfile:
            for line in pkgfile:
                if "#" not in line:
                    if "!" in line:
                        if distribution == "":
                            distribution = line.replace("!", "").strip()
                            if distribution not in DISTRIBUTIONS:
                                raise ValueError("Distribution " + 
                                                 distribution +
                                                 "is not a valid one.")
                                sys.exit()
                        else:
                            raise Warning("Line " + line + " ignored.")
                    if "[" in line:
                        title = line.replace("[", "").replace("]", "")
                        title = title.strip()
                        titles.append(title)
                        packages[title] = []
                    elif line.strip() != "\n":
                        elements = line.split()
                        if title != "":
                            for item in elements:
                                packages[title].append(item)
        return distribution, titles, packages

    def choose_packages(self, packages_filename):
        distribution, titles, packages = self.read(packages_filename)
        install = []
        for title in titles:
            answer = question(" "*2 + "* Install " + title + "?")
            if answer:
                for package in packages[title]:
                    install.append(package)
        if not self.install_packages.has_key(distribution):
            self.install_packages[distribution] = []
        for package in install:
            self.install_packages[distribution].append(package)

    def install(self, yes=False):
        apt_line = "apt-get install -t "
        install_lines = []
        for distribution in self.install_packages.keys():
            install_line = apt_line + distribution
            if yes:
                install_line += " -y"
            for package in self.install_packages[distribution]:
                install_line += " " + package
            install_lines.append(install_line.strip())
        for install_line in install_lines:
            os.system(install_line)


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


def choose(options, zero_option=None, multichoice=False, return_number=False):
    """
    Parameters:
    options: list
        Options to list as available choices
    zero_option: string (optional)
        Last option, set to 0 choice. Defaults None.
    multichoice: bool (optional)
        If several options want to be chosen it must be True.
        Defaults False.
    return_number: bool (optional)
        If True the function returns the index number of the chosen option.
        If False, it simply returns the chosen option as string (or strings
        list if multichoice is True). Defaults False.

    Returns:
    results:
        Returns the chosen options. If return_numeber is True they will be
        integers corresponding to chosen options.
        If return_number is False, they will be the options as strings.
        If multichoice is True then it will be a list, otherwise will be a
        string or integer.
    """
    def _test_choice(choice, max_number, zero=False):
        if zero is False and choice == 0:
            print "0 is not a valid choice"
            return False
    
        if choice > max_number:
            print "Choice is out of range"
            return False
    
        if choice < 0:
            print "Choices must be greater to zero"
            return False
    
        return True
    
    for i in range(1, len(options)+1):
        print " "*2 + str(i) + ") " + options[i-1]

    if zero_option is not None:
        print " "*2 + "0) " + zero_option

    if not multichoice:
        while True:
            choice = raw_input("Choice: ")
            try:
                choice = int(choice)
            except:
                print "Choice must be an integer"
            else:
                status = _test_choice(choice, len(options),
                                      zero=(zero_option is not None))
                if status:
                    break

        if return_number:
            result = choice
        else:
            if choice == 0:
                result = zero_option
            else:
                result = options[choice - 1]

    else:
        while True:
            choice = raw_input("Choice/s (eg 1 4): ")
            choice = choice.replace(",", "")
            choice = choice.split()
            try:
                choice = [int(item) for item in choice]
            except:
                print "Choices must be integers"
            else:
                status = True
                if len(choice) == 0:
                    status = False
                
                for item in choice:
                    status = _test_choice(item, len(options),
                                          zero=(zero_option is not None))
                    if not status:
                        break

                if zero_option is not None:
                    if 0 in choice and len(choice) > 1:
                        status = False
                        print "Zero option cannot be chosen along with others"

                if status:
                    break
    
        if 0 in choice:
            if return_number:
                result = [0]
            else:
                result = [zero_option]
        else:
            if return_number:
                result = [item for item in choice]
            else:
                result = [options[item-1] for item in choice]
    
    return result
