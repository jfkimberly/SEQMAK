import random
import os

def seqgen(criton):
    """ returns a segment of random DNA bases starting at 'start' and
    ending in 'end' which is 'criton' length long"""
    
    BASES = ['A','T','G','C']
    segment = ''
    
    for x in range(criton):
        segment += random.choice(BASES)
 
    return segment


def help():
    """ 'help' command. prints out all possible commands. """

    print "Possible commands are:"
    print "1. newarms (na)"
    print "2. show (s)"
    print "3. link3 (l3)"
    print "4. link5 (l5)"
    print "5. crunch (cr)"
    print "6. strands (ss)"
    print "7. exit"

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

def crunch(arms):
    """

    """

    print "Please enter the following"
    print "arm #, starting base, end base"

    crunch_dat = map(int,raw_input().split(','))
    arm,start,end = crunch_dat
    criton = end-start+1
#        if criton == end-start+1: break
#        else: 
#            print "Criton size does not match segment length!"
#            print "Please enter again!"

    while True:
        segment = seqgen(criton)
        print segment
        print "(a)ccept or (r)eject or (s)et"
        decision = raw_input()

        if decision == 'a':
            arms['arm'+str(arm)][0] =\
                arms['arm'+str(arm)][0][:start-1] + segment +\
                arms['arm'+str(arm)][0][end:]

            comp_segment = ''
            for base in segment:
                if base == 'T': comp_segment += 'A'
                elif base == 'A': comp_segment += 'T'
                elif base == 'G': comp_segment += 'C'
                elif base == 'C': comp_segment += 'G'

            arms['arm'+str(arm)][1] =\
                arms['arm'+str(arm)][1][:start-1] + comp_segment +\
                arms['arm'+str(arm)][1][end:]
            break

        elif decision == 's':
            print "Enter desired segment:"
            segment = raw_input()
            arms['arm'+str(arm)][0] =\
                arms['arm'+str(arm)][0][:start-1] + segment +\
                arms['arm'+str(arm)][0][end:]
            
            comp_segment = ''
            for base in segment:
                if base == 'T': comp_segment += 'A'
                elif base == 'A': comp_segment += 'T'
                elif base == 'G': comp_segment += 'C'
                elif base == 'C': comp_segment += 'G'

            arms['arm'+str(arm)][1] =\
                arms['arm'+str(arm)][1][:start-1] + comp_segment +\
                arms['arm'+str(arm)][1][end:]
            break
    
    return arms


def save(strands):
    """ 'save' command; saves the produced DNA strands 'strands' to file
    'filename'.

    """
    
    DIR = os.getcwd()

    while True:
        decision = raw_input("Save to file (y/n)?\n")
        if decision == 'y':
            strand_count = 1
            for key in sorted(strands.iterkeys()):
                strandfile.write(("strand %d\n") % (strand_count))
                strandfile.write(("%s\n\n") % (strands[key]))
                strand_count += 1
            break
        if decision == 'n': return None
        else: print "please enter 'y' or 'n'"

    # remove existing file 'strands.txt' if it exists
    # if os.path.exists(DIR + r'/' + 'strands.txt'): os.remove('strands.txt')
    outputfile = raw_input("Type the name of the output file:\n")
    strandfile = open(DIR+"//"+outputfile,"w")

