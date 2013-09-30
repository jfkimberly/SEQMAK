#######################################################################
# Copyright (C) 2012 Junghoon Kim
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

import random
from itertools import permutations as perm

def seqgen(criton):
    """ returns a segment of random DNA bases starting at 'start' and
    ending in 'end' which is 'criton' length long"""
    
    BASES = ['A','T','G','C']
    segment = ''
    
    for x in range(criton):
        segment += random.choice(BASES)
 
    return segment


def compgen(segment):
    """ returns a complementary sequence string 'comp_segment' to the input
    sequence string 'segment'. 

    """

    comp_segment = ''
    for base in segment:
        if base == 'T': comp_segment += 'A'
        elif base == 'A': comp_segment += 'T'
        elif base == 'G': comp_segment += 'C'
        elif base == 'C': comp_segment += 'G'
    
    return comp_segment


def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    
    for i in range(0, len(l), n): yield l[i:i+n]


def linker3():
    """ linker3 (l3) command; takes user input of the ordered pairs of arm
    segments in the 5' -> 3' direction and returns them as a list. Used in the 
    'linker' function.

    """

    print "Enter the arm and it's 3'-linked arm:"
    return list(chunks(raw_input().split(','),2))


def linker5():
    """ linker5 (l5) command; takes user input of the ordered pairs of arm
    segments in the 3' -> 5' direction and returns them as a list. Used in the 
    'linker' function.

    """

    print "Enter the arm and it's 5'-linked arm (press `Enter' if there are\
 none):"
    link5 = raw_input()
    if link5 :
        return list(chunks(link5.split(','),2))
    else :
        return []


def user_decision():
    """ 'user_decision' function used in the 'crunch' function. Keeps looping
    until an appropriate 'y' (yes), 'n' (no), or 'N' (abort) answer is given and
    returns a decision.

    """

    while True:
        use = raw_input()
        if use == 'y': 
            decision = 'a'
            break
        elif use == 'n': 
            decision = 'r'
            break
        elif use == 'N':
            decision = 'N'
        else: print "Please answer 'y', 'n', or 'N'"

    return decision


def seggen(segsize,segment_list):
    """ 'seggen' function. """

    # produce new random 'segment' of 'segsize' which is not in 'segment_list'
    while True:
        segment = seqgen(segsize)

        if segment in segment_list: 
            print "{SEGMENT} has been used {TIMES} times\n".format(SEGMENT=segment, TIMES=segment_list.count(segment))
            print "Use anyway? (y/n)"
            decision = user_decision()

            if decision == 'a': break


        else:
            print segment
            print "(a)ccept or (r)eject or (s)et"

            while True:
                decision = raw_input()
                if decision == 'r' or decision == 'a' or decision == 's': break
                else: print "Type `a', `r', or `s'."

            if decision == 'a' or decision == 's': break

    return segment, decision


def repeats(strands, segment, criton, repeat, decision):
    """ 'repeats' command; checks all strands for number of repeating segments.

    """

    # check for repeating segments in 'strands' for all generated sequences
    repeatseg = 0
    for strand in strands.values():
        for base in range(len(strand) - criton + 1):
            if 'x' not in strand[base:base + criton]: 
                testseg = strand[base:base + criton]
                if testseg == segment: repeatseg += 1

    if repeat == 0 and repeatseg > 0: 
        print "There are repeated segments with the given CRITON size"
        print "Please increase CRITON size"
        decision = 'r'
    elif repeat >= repeatseg: pass
    else: 
        print "There are %d repeats of this segment" % (repeatseg)
        print "Use anyways (y/n)?"
        decision = user_decision()

    return decision

def armgen(arms, segment, crunch_dat):
    """ 'armgen' function; Used in the 'crunch' function. Receives dictionary
    'arms' and returns the dictionary 'arms' replaced with the randomly
    generated arm segment

    """
    
    arm = crunch_dat[0]
    start = crunch_dat[1]
    end = crunch_dat[2]

    # retrieve latest segment and complementary segment from 'segment_list'
    comp_segment = compgen(segment)

    # change arms e.g. arm1 => 'xxxx' -> 'AGCT'
    arms['arm'+str(arm)][0] =\
        arms['arm'+str(arm)][0][:start-1] + segment +\
        arms['arm'+str(arm)][0][end:]

    arms['arm'+str(arm)][1] =\
        arms['arm'+str(arm)][1][:start-1] + comp_segment +\
        arms['arm'+str(arm)][1][end:]

    return arms

