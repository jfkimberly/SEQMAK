import random
import os
# remove existing strand text files if they exist
DIR = os.getcwd()
if os.path.exists(DIR + r'/' + 'strands.txt'):
    os.remove('strands.txt')

strandfile=open("strands.txt","a",0)

def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    
    for i in range(0, len(l), n): yield l[i:i+n]

def crunch(criton):
    """ returns a segment of random DNA bases starting at 'start' and
    ending in 'end' which is 'criton' length long"""
    
    BASES = ['A','T','G','C']
    segment = ''
    
    for x in range(criton):
        segment += random.choice(BASES)
 
    return segment



def printscreen():
    """ Main function to determine what command to enter"""

    arm_num = 0
    arms = {}
    strands = {}
    l3_list = []
    l5_list = []


    while True:
        
        command = raw_input("Enter a command (type 'help' for help)\n")

        if command == 'exit': break
        
        elif command == 'help':
            print "Possible commands are:"
            print "1. newarms (na)"
            print "2. show (s)"
            print "3. link3 (l3)"
            print "4. link5 (l5)"
            print "5. crunch (cr)"
            print "6. strands (ss)"
            print "7. exit"
            
        elif command == 'newarms' or command ==  'na':
            arm_num = int(raw_input("How many arms do you want?\n"))
            arm_length = int(raw_input("Enter arm length:\n"))
            
            for arm_count in range(1,arm_num+1):
                arms['arm'+str(arm_count)] = ['x'*arm_length,'x'*arm_length]
# if arms is used as a list and not dict 
#            arms.append['x'*arm_length,'x'*arm_length]
            print "Number of arms: %d, Arm length: %d" %  (arm_num,arm_length)

        elif command == 'show' or command == 's':

            for key in sorted(arms.iterkeys()):
                print ""
                print key
                print arms[key][0]
                print arms[key][1]

            print ""


        elif command == 'link3' or command == 'l3':
            print "Enter the arm and it's 3'-linked arm:"
            l3_list = list(chunks(raw_input().split(','),2))

#            x.isdigit() for x in raw_input().split(','):
#                l3_list = list(chunks(raw_input().split(','),2))
#            else: print "Please enter only digits"
            
        elif command == 'link5' or command == 'l5':
            print "Enter the arm and it's 5'-linked arm:"
            l5_list = list(chunks(raw_input().split(','),2))
            
        elif command == 'crunch' or command == 'c':

            print "Please enter the following"
            print "arm #, starting base, end base"
            while True:
                crunch_dat = map(int,raw_input().split(','))
                arm,start,end = crunch_dat
                criton = end-start+1
                if criton == end-start+1: break
                else: 
                    print "Criton size does not match segment length!"
                    print "Please enter again!"


            while True:
                segment = crunch(criton)
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
                        arms['arm'+str(arm)][0][:start-1] + comp_segment +\
                        arms['arm'+str(arm)][0][end:]
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
                        arms['arm'+str(arm)][0][:start-1] + comp_segment +\
                        arms['arm'+str(arm)][0][end:]
                    break


        elif command == 'strands' or command == 'ss':

#            strands = ['' for x in range(arm_num/2)]
#            for strand_num in range(arm_num/2):
            strands['s1'] = arms['arm1'][0] + arms['arm2'][1] +\
                arms['arm3'][0] + arms['arm4'][1]

            strands['s2'] = arms['arm5'][0] + arms['arm1'][1][::-1]

            strands['s3'] = arms['arm3'][1][::-1] + arms['arm2'][0][::-1] +\
                arms['arm6'][1] + arms['arm7'][0]

            strands['s4'] = arms['arm4'][0][::-1] + arms['arm8'][1]
            
            strands['s5'] = arms['arm8'][0] + arms['arm7'][1] +\
                arms['arm6'][0] + arms['arm5'][1]

            strand_count = 1
            for key in sorted(strands.iterkeys()):
                print ""
                print "strand %d" % (strand_count)
                print strands[key]

                strand_count += 1
            print ""
            

            save = raw_input("Save to file (y/n)?\n")
            if save == 'y':
                strand_count = 1
                for key in sorted(strands.iterkeys()):
                    strandfile.write(("strand %d\n") % (strand_count))
                    strandfile.write(("%s\n\n") % (strands[key]))
                    strand_count += 1

        else: print "What? Retype command!"


    return 0


printscreen()
