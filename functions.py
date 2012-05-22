import random

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

    print "Enter the arm and it's 5'-linked arm:"
    return list(chunks(raw_input().split(','),2))


def user_decision():
    """ 'user_decision' function used in the 'crunch' function. Keeps
    looping until an appropriate 'y' (yes) or 'n' (no) answer is given
    and returns a decision. 

    """

    while True:
        use = raw_input("Use anyways? (y/n)\n")
        if use == 'y': 
            decision = 'a'
            break
        elif use == 'n': 
            decision = 'r'
            break
        else: print "Please answer 'y' or 'n'"

    return decision


def seggen(segment_list, segsize):
    """ 'seggen' function. """

    # produce new random 'segment' of 'segsize' which is not in 
    # 'segment_list' 
    while True:
        segment = seqgen(segsize)
        print segment

        if segment_list.count(segment) == 0: 
            print "(a)ccept or (r)eject or (s)et"
            decision = raw_input()
            if decision == 'a' or decision == 's': break

        else: 
            segcount = segment_list.count(segment)
            print "This segment has been used %d times" % (segcount)
            decision = user_decision()
            if decision == 'a': break

    return segment, decision


def repeats(strands, segment, criton, repeat, decision):
    """ 'repeats' command; checks all strands for number of repeating segments.

    """

    # check for repeating segments
    repeatseg = 0
    for strand in strands.values():
        for base in range(len(strand) - criton + 1):
            if 'x' not in strand[base:base + criton]: 
                testseg = strand[base:base + criton]
                if testseg == segment: repeatseg += 1

    if repeat == None and repeatseg > 0: 
        print "CRITON size is too small!"
        decision = 'r'
    elif repeat >= repeatseg: pass
    else: 
        print "There are %d repeats of this segment" % (repeatseg)
        decision = user_decision()

    return decision

def armgen(arms, segment_list, crunch_dat):
    """ 'armgen' function; Used in the 'crunch' function. Receives dictionary
    'arms' and returns the dictionary 'arms' replaced with the randomly
    generated arm segment

    """
    
    arm = crunch_dat[0]
    start = crunch_dat[1]
    end = crunch_dat[2]

    # retrieve latest segment and complementary segment from 'segment_list'
    segment = segment_list[-2][:]
    comp_segment = segment_list[-1][:]

    # change arms e.g. arm1 => 'xxxx' -> 'AGCT'
    arms['arm'+str(arm)][0] =\
        arms['arm'+str(arm)][0][:start-1] + segment +\
        arms['arm'+str(arm)][0][end:]

    arms['arm'+str(arm)][1] =\
        arms['arm'+str(arm)][1][:start-1] + comp_segment +\
        arms['arm'+str(arm)][1][end:]

    return arms

