#!/usr/bin/env python
#
# kloki
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Koen Klinkers k.klinkers@gmail.com


import random, sys


def main():
    results=open(sys.argv[1]).readlines()
    newresults=open(sys.argv[2],"w+")
    for parse in results:
        parse=parse.replace("{","(")
        parse=parse.replace("}",")")
        newresults.write(parse)
    
    
    newresults.close()


#-------------------------------
if __name__ == "__main__":
    main()
