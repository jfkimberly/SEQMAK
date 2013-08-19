#######################################################################
# Copyright 2012 Junghoon Kim
# jfkimberly@skku.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

import commands

def main():
    """ Main function to determine what command to enter """

    segment_list = []
    all_seg_list = {}

    while True:
        
        command = raw_input("Enter a command (type 'help' or 'h' for help):\n")

        if command == 'exit': break

        # 'help' command
        # prints a list of possible commands
        elif command == 'help' or command == 'h':
            commands.help()

        # 'newarm (na)' command
        # creates newarms and their corresponding segment sequences in a
        # dictionary 'arms'
        elif command == 'newarms' or command == 'na': 
            arms = commands.newarms()
                
        # 'show (s)' command
        # prints out the created arms
        elif command == 'show' or command == 's':
            commands.show(arms)

        # 'link (l)' command
        elif command == 'link' or command == 'l':
            l3_list, l5_list = commands.linker()

        # 'crunch (c)' command
        # produces random sequences of 
        elif command == 'crunch' or command == 'c':
            try:
                strands
            except UnboundLocalError:
                print "Maybe you should generate your strands first ('strandgen')?"
            else:
                try:
                    arms,strands,segment_list,all_seg_list =\
                        commands.crunch(arms,strands,l3_list,segment_list,all_seg_list)
                    print segment_list
                except TypeError:
                    print "Something's not right. Try 'crunch' again."

        # 'strandgen (sg)' command
        # 
        elif command == 'strandgen' or command == 'sg':
            try:
                strands = commands.strandgen(arms, l3_list, l5_list)
            except UnboundLocalError:
                print "Something's wrong. Maybe you missed a step?"

        # 'repeatcheck (rp) command
        elif command == 'repeatcheck' or command == 'rp':
            try:
                commands.repeatcheck(strands)
            except UnboundLocalError:
                print "Something's wrong. Maybe you missed a step?"

        # 'save (sv)' command
        elif command == 'save' or command == 'sv':
            try:
                commands.save(arms, strands)
            except UnboundLocalError:
                print "Something's wrong. Maybe you missed a step?"

        else: print "What? Retype command!"


    return None


if __name__ == '__main__':

    main()
