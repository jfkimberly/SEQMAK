import commands


def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    
    for i in range(0, len(l), n): yield l[i:i+n]


def printscreen():
    """ Main function to determine what command to enter"""


    strands = {}
    l3_list = []
    l5_list = []

    while True:
        
        command = raw_input("Enter a command (type 'help' for help):\n")

        if command == 'exit': break

        # 'help' command
        # prints a list of possible commands
        elif command == 'help':
            commands.help()

        # 'newarm (na)' command
        # creates newarms and their corresponding segment sequences in a
        # dictionary 'arms'
        elif command == 'newarms' or command ==  'na': 
            arms = commands.newarms()
                
        # 'show (s)' command
        # prints out the created arms
        elif command == 'show' or command == 's':
            commands.show(arms)

        # 'link3 (l3)' command
        elif command == 'link3' or command == 'l3':
            print "Enter the arm and it's 3'-linked arm:"
            l3_list = list(chunks(raw_input().split(','),2))

        # 'link5 (l5)' command
        elif command == 'link5' or command == 'l5':
            print "Enter the arm and it's 5'-linked arm:"
            l5_list = list(chunks(raw_input().split(','),2))

        # 'crunch (c)' command
        # produces random sequences of 
        elif command == 'crunch' or command == 'c':
            arms = commands.crunch(arms)

        elif command == 'strands' or command == 'ss':

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
            
        elif command == 'save' or command == 'sv':
            commands.save(strands)

        else: print "What? Retype command!"


    return 0


printscreen()
