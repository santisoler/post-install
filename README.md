# Manjaro Post Installation Script

These script allows to automatize Manjaro post installation tasks as system update and
package installation.

## Installing

Download this repository manually, or use git if it's already installed:

```
git clone https://www.github.com/santisoler/post-install
```

Uncompress (if you downloaded manually) and change working directory to
`post_install`.
Then make the script excecutable and finally we can ran it as root.

```
$ cd post-install/
$ chmod +x post-install
$ sudo ./post-install --help
```

## Setting up

Before running the script we must write our own packages file, as the one
present in this repo.
In this file we will put the packages that the script will ask which we want
to install.
We group them using titles written between `[` and `]`.

For example:
```
[ latex ]
texlive-full

[ vim and git]
vim
git
```

The [`packages`](https://github.com/santisoler/post-install/blob/master/packages)
file has a collection of packages that are generally used by me, see if it meets your
requirements and feel free to edit it as you please.

## How to use it
Once the packages file is created, we can run the script (as root) as follows:

```
$ sudo ./post-install packages
```

If we want to assume yes all the questions from the apt statements, we can add
a `-y` option:

```
$ sudo ./post-install -y packages
```

In case we have more than one packages file, for example `packages1` and `packages2`,
we can run them together:

```
$ sudo ./post-install packages1 packages2
```

## Old script

Previous versions of the script can be found in this repository under the
[old-script](https://github.com/santisoler/post-install/tree/old-script) or the
[debian](https://github.com/santisoler/post-install/tree/debian) branches.


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
along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
