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
    print "8. exit"
    
    print "Use '--help' for more information. e.g. 'na --help'"
    return 0


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
        arm_numbers  = int(raw_input("How many arms do you want?\n"))
        arm_length = int(raw_input("What is the length of these arms\n"))

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
        print arms[key][0]
        print arms[key][1]

    return None


def linker():
    """ 'linker' function used in 'strandgen' function. 

    """
    
    # create links (the arms)
    link3 = linker3()
    link5 = linker5()

    # join the arms to create strands
    for l5 in link5:
        for l3_index, l3 in izip(count(), link3):

            if l3[-1] == l5[0]:
                forearms = l3[:]
                index = l3_index
                link3 = [x for x in link3 if x != l3]

            if l3[0] == l5[1]:
                postarms = l3[:]
#                index = l3_index
                link3 = [x for x in link3 if x != l3]

        link3.insert(index, forearms+postarms)

    print "link3", link3
    print "link5", link5
    
    return link3, link5
    

def crunch(arms,strands,link3,segment_list):
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
    crunch_dat = map(int,raw_input().split(','))

    # check if repeats should be allowed 
    # (default is no input meaning no repeats allowed)
    if len(crunch_dat) == 4:
        repeat = 0
        arm, start, end, criton = crunch_dat
    else: arm, start, end, criton, repeat = crunch_dat

    # segment size to crunch (length of random bases to produce)
    segsize = end - start + 1

    while True:

        # produce a random segment 'segment' of 'segsize and chooses to
        # (a)ccept, (r)eject, or (s)et in 'decision'.
        segment, decision = seggen(segment_list, segsize)
                    
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
            arms = armgen(arms,segment_list,crunch_dat)
            
            # change the corresponding strand segment            
            strands = strandgen(arms,link3)

            break

        elif decision == 's':
            # create segment & complementary segment
            segment = raw_input("Enter desired segment:\n")
            comp_segment = compgen(segment)

            # add segment and complementary segment to 'segment_list' only if
            # the segment is a nonempty string
            if segment != '':
                segment_list.append(segment)
                segment_list.append(comp_segment)

            # change the specified arm segment
                arms = armgen(arms,segment_list,crunch_dat)
            
            # change the corresponding strand segment            
                strands = strandgen(arms,link3)

            break

    return arms, strands, segment_list


def strandgen(arms,link3,link5=None):
    """ 'strandgen (sg)' command; returns the dictionary DNA strands 'strands'
    created by combining the dictionary input 'arms'.

    """

    if link5 is None: link5 = []

    for strand_count, arm_num in izip(count(),link3):
        
        temp_strand = ''
        for arm_count, arm_index in izip(count(),arm_num):
            if arm_count % 2 == 0: 
                temp_strand += arms['arm'+arm_index][0]
            else: 
                temp_strand += arms['arm'+arm_index][1][::-1]
        strands['strand'+str(strand_count+1)] = temp_strand[:]

    strand_count = 1
    for key in sorted(strands.iterkeys()):
        print ""
        print "strand %d" % (strand_count)

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
        repeat_dat = map(int, raw_input().split(','))
        if len(repeat_dat) == 4: break
        else: print "Please enter 4 numbers"

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
                        print 

    

    


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
                strandfile.write(("arm%d\n") % (arm_count))
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

    return 0



if __name__ == '__main__':

    list3 = [['1','2'],['3','4'],['5','6'],['7','1'],['9','3'],['2','8'],['11','5'],['4','10'],['6','12'],['12','11'],['10','9'],['8','7']]
    list5 = [['2','3'],['4','5'],['3','2'],['5','4'],['11','10'],['9','8']]
    arm =[]
    
    strands(arm,list3,list5)