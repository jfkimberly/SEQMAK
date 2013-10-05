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

import os
import re
import random
from itertools import count, izip, product
from functions import *

strands = {}

def help():
    """ 'help' command. prints out all possible commands. """

    print "Possible commands are:"
    print "1. newarms (na)"
    print "2. show (s)"
    print "3. link (l)"
    print "4. crunch (c)"
    print "5. strandgen (sg)"
    print "6. repeatcheck (rp)"
    print "7. save (sv)"
    print "8. load (ld)"
    print "9. exit"

    print "Use '--help' for more information. e.g. 'na --help'"

    return None


def newarms():
    """ 'newarms' command; returns a dictionary 'arms' of the newly created
    arms. The keys are arm1, arm2, etc. and their values are a 2-element
    list. The elements are "empty" strings of the arms of length 'arm_length'
    e.g. ['xxxx','xxxx']. The two strings are meant to become complementary
    segments when using the "crunch" function.

    """

    arm_num = 1
    arms = {}
    while True:

        # user input for the number and length of the arms
        # e.g. if 4 arms of length 4 and 4 arms of length 8 are needed then the
        # user input for the first iteration through the outer while loop should
        # be 'arm_numbers' = 4 and 'arm_length' = 4 and for the second iteration
        # the input should be 'arm_numbers' = 4 and 'arm_length' = 8.
        while True:
            try:
                arm_numbers  = int(raw_input("How many arms do you want?\n"))
            except ValueError:
                print "Come again?"
            else: break

        while True:
            try:
                arm_length = int(raw_input("What is the length of the subarms of these arms?\n"))
            except ValueError:
                print "Come again?"
            else: break

        # creates a dictionary 'arms' where the keys are the arms, i.e. arm1,
        # arm2, arm3, etc. and their corresponding values are 2-element lists of
        # strings of length 'arm_length' (the first element is the DNA segment
        # and the second element is its complementary segment. The specific
        # bases for both are generated when using the "crunch" function).
        # e.g. arm1:['xxxx','xxxx'], arm2:['xxxxxx','xxxxxx'], etc.
        for arm_count in range(arm_num,arm_num+arm_numbers):
            arms['arm'+str(arm_count)] = ['x'*arm_length,'x'*arm_length]

        print "Number of arms: %d, Arm length: %d" % (arm_numbers,arm_length)

        # asks user if more arms are needed
        while True:
            decision = raw_input("Any more arms? (y/n)\n")
            if decision == 'n': break
            elif decision == 'y': break
            else: print "please enter 'y' or 'n'\n"

        if decision == 'n': return arms

        arm_num = arm_count+1

    return arms


def show(arms):
    """ show (s) command; prints out 'arms' which is a dictionary of all the
    created arms and their base sequences

    """

    for key in sorted(arms.iterkeys()):
        print ""
        print key
        print re.sub("(.{5})", "\\1 ", arms[key][0])
        print re.sub("(.{5})", "\\1 ", arms[key][1])

    return None


def linker():
    """ 'linker' function used in 'strandgen' function.

    """

    # create links (the arms)
    link3 = linker3()
    link5 = linker5()

    # join the 3'-linked and 5'-linked arms into 'linker_list' to create strands
    try:
        for l5 in link5:
            print "l5", l5
            # Sequentially looks for a match between the first (last) element of
            # all the elements of the 5'-linked arm list (link5), e.g. the '1'
            # ('2') and '3' ('4') in [['1','2'],['3','4']], and the last (first)
            # element of any element in the 3'-linked arm list (link3), e.g. the
            # '1' ('2') and '3' ('4') in [['5','1'],['2','3'],['4','6']] and if
            # found changes the value of 'index_fore' (index_post) to 1. Also
            # checks if the matching elements are from different strands
            # (l3_ind1 != l3_ind2) and appends the joined arms into 'link3' and
            # copies to 'linker_list' list for output.
            index_fore = None
            index_post = None
            for l3_index, l3 in izip(count(), link3):

                if l3[-1] == l5[0]:
                    forearms = l3[:]
                    link3 = [x for x in link3 if x != l3]
                    index_fore = 1
                    l3_ind1 = l3_index

                if l3[0] == l5[1]:
                    postarms = l3[:]
                    link3 = [x for x in link3 if x != l3]
                    index_post = 1
                    l3_ind2 = l3_index

            if (index_fore and index_post) and (l3_ind1 != l3_ind2):
                link3.append(forearms+postarms)
                
            print "link3",link3

        linker_list = link3[:]

    except (IndexError, UnboundLocalError):
        print "Hmm, something seems off, try the 'link' command again."

    print "linker_list", linker_list

    return linker_list





def crunch(arms,strands,linker_list,segment_list):
    """ randomly generates or the user defines a sequence of bases for the each
    of the arms and returns dictionary 'arms' which consists of the arms as
    keys, e.g. arm1, arm2, etc., and each arms' sequence and its complementary
    sequence as a 2-element list as its value.

    The user input is the arm number 'arm', the starting base index number of
    the arm segment to be randomly generated 'start', and the end base index
    number of the arm segment to be randomly generated 'end'. 'criton' refers to
    the length of the segment to be generated.

    """

    print "Please enter the following"
    print "arm #, starting base, end base, CRITON size, # of repeats (default: None)"
    while True:
        try:
            crunch_dat = map(int,raw_input().split(','))
        except ValueError:
            print "Your input doesn't make any sense!"
            break
        else: break

    # check if repeats should be allowed
    # (default is no input meaning no repeats allowed)
    try:
        if len(crunch_dat) == 4:
            repeat = 0
            arm, start, end, criton = crunch_dat
        else: arm, start, end, criton, repeat = crunch_dat

    except (ValueError, UnboundLocalError) as error:
        print error

    else:
        # segment size to crunch (length of random bases to produce)
        segsize = end - start + 1
        critkey = 'crit' + str(segsize)
        print critkey


        while True:

            # produce a random segment 'segment' of 'segsize' and chooses to
            # (a)ccept, (r)eject, or (s)et in 'decision'.
            segment, decision = seggen(segsize, segment_list)
            
            # check the number of repeats of 'segment' in 'strands' and changes
            # 'decision' accordingly
            decision = repeats(strands, segment, criton, repeat, decision)

            # actions according to 'decision'
            if decision == 'r':
                break

            elif decision == 'a':
                # create complementary segment
                comp_segment = compgen(segment)

                # add segment and complementary segment to 'segment_list'
                segment_list.append(segment)
                segment_list.append(comp_segment)

                # change the specified arm segment
                arms = armgen(arms,segment,crunch_dat)

                # change the corresponding strand segment
                strands = strandgen(arms,linker_list)

                break

            elif decision == 's':
                # create segment & complementary segment
                segment = raw_input("Enter desired segment:\n").upper()
                comp_segment = compgen(segment)

                # add segment and complementary segment to 'segment_list' only if
                # the segment is a nonempty string
                if segment != '':
                    segment_list.append(segment)
                    segment_list.append(comp_segment)

                    # change the specified arm segment
                    arms = armgen(arms,segment,crunch_dat)

                    # change the corresponding strand segment
                    strands = strandgen(arms,linker_list)

                break

    return arms, strands, segment_list


def strandgen(arms,linker_list):
    """ 'strandgen (sg)' command; returns the dictionary DNA strands 'strands'
    created by combining the dictionary input 'arms'.

    """

    for strand_count, arm_num in izip(count(),linker_list):

        try:
            temp_strand = ''
            for arm_count, arm_index in izip(count(),arm_num):
                if arm_count % 2 == 0:
                    temp_strand += arms['arm'+arm_index][0]
                else:
                    temp_strand += arms['arm'+arm_index][1][::-1]
            strands['strand'+str(strand_count+1)] = temp_strand[:]

        except KeyError as error:
            print "Can't generate strands. Try 'link' command again then 'strandgen'."
            break

    strand_count = 1
    for key in sorted(strands.iterkeys()):
        print ""
        print "strand %d (%d bases)" % (strand_count,len(strands[key]))

        # print out strand in 5 base units
        print re.sub("(.{5})", "\\1 ", strands[key])
        strand_count += 1
    print ""

    return strands


def repeatcheck(strands):
    """ 'repeatcheck' command; checks the number of repeats and returns the
    positions of the repeating strands.

    """

    print "Enter min. CRITON size, max. CRITON size, min. # of repeats, max. #\
of repeats"

    while True:
        try:
            repeat_dat = map(int, raw_input().split(','))
            if len(repeat_dat) == 4: break
            else: print "Please enter 4 numbers"
        except (ValueError, UnboundLocalError):
            print "Please enter only integers!"

    mincrit, maxcrit, minrep, maxrep = repeat_dat

    # CRITON repeat check
    for criton in range(mincrit,maxcrit+1):
        segment_list = []

        for strand_key in strands:
            for base in range(len(strands[strand_key]) - criton + 1):
                testseg = strands[strand_key][base:base + criton]

                if testseg not in segment_list:
                    segment_list.append(testseg)

                    # check strands
                    reppos_list = []
                    repeatseg = 0
                    for key, value in strands.items():
                        for rep_pos in range(len(value) - criton + 1):
                            if testseg == value[rep_pos:rep_pos + criton]:
                                repeatseg += 1
                                reppos_list.append((key, rep_pos))

                    if minrep <= repeatseg <= maxrep:
                        print "'%s' has %d repeats " % (testseg, repeatseg)
                        print "strand # => base position"
                        for strand_num, pos in reppos_list:
                            print "%s => %d" % (strand_num, pos + 1)
                        print ""


def save(arms, strands):
    """ 'save' command; saves the produced DNA strands 'strands' to file
    'filename'.

    """

    DIR = os.getcwd()
    # remove existing file 'strands.txt' if it exists
    # if os.path.exists(DIR + r'/' + 'strands.txt'): os.remove('strands.txt')
    outputfile = raw_input("Type the name of the output file:\n")
    strandfile = open(DIR+"//"+outputfile,"w")

    while True:
        decision = raw_input("Save to file (y/n)?\n")
        if decision == 'y':
            arm_count = 1
            strand_count = 1
            for key in sorted(arms.iterkeys()):
                strandfile.write(key)
                strandfile.write("\n")
                strandfile.write(("%s\n%s\n\n") % (arms[key][0],arms[key][1]))
                arm_count += 1

            strandfile.write("5' -> 3'\n")
            for key in sorted(strands.iterkeys()):
                strandfile.write(("strand %d\n") % (strand_count))
                strandfile.write(("%s\n\n") % (re.sub("(.{5})", "\\1 ", strands[key])))
                strand_count += 1
            break
        elif decision == 'n': return None
        else: print "please enter 'y' or 'n'"

    return None

def load():
    """loads a file containing sequence information of strands from the user and
    returns a dictionary 'strands'

    """

    try:
        user_input = raw_input("Enter the name of the file (e.g., strands.txt)\
 or 'q' to exit command:\n")
        if user_input == 'q': return 0
        f = open(user_input, 'r')
    except IOError:
        print "file doesn't exist!"
        return 0

    strands = {}
    print ''
    for index,lines in izip(count(),f):

        sequence = lines.upper().replace(" ","").strip()
        if sequence:
            strands['strand'+str(index+1)] = sequence
            print '{}: {}'.format('strand'+str(index+1), strands['strand'+str(index+1)])

    f.close()

    return strands



if __name__ == '__main__':

    list3 = [['1','2'],['3','4'],['5','6'],['7','1'],['9','3'],['2','8'],['11','5'],['4','10'],['6','12'],['12','11'],['10','9'],['8','7']]
    list5 = [['2','3'],['4','5'],['3','2'],['5','4'],['11','10'],['9','8']]
    arm =[]

    strands(arm,list3,list5)
