# Debian Post Installation Script

This script allows us to automatize post installation tasks as repositories
creation, system upgrade and package installation.

## Install

Download this repository manually, or use git if it's already installed:

```
git clone https://www.github.com/santis19/post_install
```

Uncompress (if you downloaded manually) and change working directory to post_install. Then make the script excecutable and finally we can ran it as root.
First we should make it excecutable:

```
$ cd post_install
$ chmod +x post-install
$ su
# ./post-install --help
```

## Running

Before running the script we must write our own packages file, as the one present in this repo.
In this file we will put the packages that the script will ask which we want to install.
We group them using titles written between \[ and \].

In the package file we must also set the distribution from which the packages will be installed.
We do it in the first line, putting the distribution after a ! symbol. For example: ! stretch

An example of this package file can be:

```
! stretch

[ Git]
git

[ iPython and Numpy ]
ipython python-numpy
```

Once the packages file is created, we can run the script (as root) as follows:

```
# ./post-install packages
```

If we want to assume yes all the questions from the apt statements, we can add a -y option:

```
# ./post-install -y packages
```

In case we have more than one packages file, for example one for jessie and another one for jessie-backports, we can run them together:

```
# ./post-install packages1 packages2
```


## Licence

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
