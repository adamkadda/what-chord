from itertools import permutations

ntoi = {
        'C': 0, 'B#': 0,
        'C#': 1, 'Db': 1,
        'D': 2,
        'D#': 3, 'Eb': 3,
        'E': 4, 'Fb': 4,
        'F': 5, 'E#': 5,
        'F#': 6, 'Gb': 6,
        'G': 7,
        'G#': 8, 'Ab': 8,
        'A': 9,
        'A#': 10, 'Bb': 10,
        'B': 11, 'Cb': 11
    }

itoa = {
        1: 'b2',
        2: '2',
        5: '4',
        6: '#4',
        8: 'b6',
        9: '6',
        # 10
        13: 'b9',
        14: '9',
        15: '#9',
        16: 'b11',
        17: '11',
        18: '#11',
        # 19
        20: 'b13',
        21: '13'
    }

atoi = {
        'min-2': 1,
        'maj-2': 2,
        'min-3': 3,
        'maj-3': 4,
        'perf-4': 5,
        'aug-4': 6, 'dim-5': 6,
        'perf-5': 7,
        'min-6': 8, 'aug-5': 8,
        'maj-6': 9,
        'min-7': 10,
        'maj-7': 11,
        # Skip 'octave': 12
        'min-9': 13,
        'maj-9': 14,
        'min-10': 15,
        'maj-10': 16,
        'perf-11': 17,
        'aug-11': 18, 'dim-12': 18,
        # Skip 'perf-12': 19
        'min-13': 20,
        'maj-13': 21,
        'min-14': 22,
        'maj-14': 23
        # Skip 'double-octave': 24
    }


def clean_notes(notes):

    tally = {}

    cleaned = notes

    for i, note in enumerate(notes):

        # check for invalid notes
        if note not in ntoi:
            print(f"Invalid note: {note}")
            return None

        # check for duplicates        
        if note not in tally:
            tally[note] = 1
        else:
            cleaned.pop(i)

    return cleaned


def note_to_int(chord):
    intval = tuple(ntoi[note] for note in chord)
    return intval


def get_intervals(integer_notes):

    intervals = []

    for i, note in enumerate(integer_notes):

        # assign root note
        if i == 0:
            intervals.append(0)
        
        else:

            prev = integer_notes[i - 1]

            # if current note is 'lower' than prev
            if note < prev:

                # interval = prev_interval + (12 + note) - prev_note
                val = intervals[i - 1] + (12 + note) - prev
                intervals.append(val)

            # else, note must be 'higher'
            else:
                # prev_interval + (note - prev_note)
                val = intervals[i - 1] + (note - prev)
                intervals.append(val)

    return intervals


def check_inversion(inversion):
    
    for interval in inversion:
        if interval > 21:
            return False

    third_or_sus = [1, 2, 3, 4, 5, 6]
    
    # check whether a third or sus exists in this inversion
    for interval in inversion:
        if interval in third_or_sus:
            return True

    return False


def get_name(intervals, notes):
    
    # initialize chord attributes
    third = None
    fifth = False
    seventh = False
    ninth = False
    eleventh = False

    # initialize chord name segments
    triad = None
    lead = ""
    sus = []
    add = []

    # gigantic match case haha
    # hopefully this isn't too ugly...
    for interval in intervals:

        match interval:

            # unison
            case 0:
                continue

            # third/sus
            case x if x >= 1 and x <= 5:
                
                # min-3 (2nd prio)
                if x == 3:
                    third = 'minor'

                    if sus:
                        add.append(sus.pop(0))

                # maj-3 (1st prio)
                elif x == 4:

                    # replace minor 3
                    if third == 'minor':
                        add.append('#2')

                    third = 'major'

                    if sus:
                        add.append(sus.pop(0))

                # else (sus/add)
                else:

                    # if no min-3 or maj-3 ...
                    if not third:
                        sus.append(itoa[x])

                    else:
                        add.append(itoa[x])


            # sus/add #4 || diminished 5 -> dim triad
            case 6:

                # sus
                if not third:
                    sus.append(itoa[6])

                # dim 5
                elif third == 'minor':
                    triad = 'dim'

                # else (maj-3 -> add #4)
                else:
                    add.append(itoa[6])


            # min/major triad completion
            case 7:

                fifth = True

                # major triad
                if third == 'major':
                    triad = ''

                # minor triad
                elif third == 'minor':

                    # if a diminished triad already formed ...
                    if triad == 'dim':
                        add.append(itoa[6])
                        
                    triad = 'm'

                # else (sus triad)
                else:
                    triad = ''


            # aug triad || add b6
            case 8:

                # aug triad
                if third == 'major':

                    # if a triad already formed ...
                    if triad:
                        add.append(itoa[8])

                    else:
                        triad = 'aug'
                        fifth = True

                # else (min-3 or sus -> add b6)
                else:
                    add.append(itoa[8])
                    

                    
            # X6 || dim 7 || add 6
            case 9:

                # dim 7
                if third == 'minor':

                    if triad == 'dim':
                        lead = '7'

                    else:
                        add.append(itoa[9])

                # else (maj-3 or sus -> lead 6)
                else:
                    lead = '6'


            # 7th chord completion
            case x if x == 10 or x == 11:

                # applies to sus as well
                lead = '7'
                seventh = True

                # min-7
                if x == 10:

                    # X7
                    if third == 'major':
                        triad = ''

                    # Xm7
                    elif third == 'minor':
                        
                        # Xm7(b5)
                        if triad == 'dim':
                            triad = 'm'
                            add.append('b5')
                        
                        # Xm7 is default
                            
                # maj-7
                elif x == 11:

                    # XmM7
                    if third == 'minor':

                        if triad == 'dim':
                            add.append(itoa[6])

                        triad = 'mM'

                    # Xmaj7 and Xaug7 
                    else:

                        # turns aug-5 into an add
                        if triad == 'aug':
                            add.append(itoa[8])

                        triad = 'maj'

                
            # case 12:


            # min-9    
            case 13:

                # else (add b9)
                add.append(itoa[13])


            # maj-9
            case 14:

                # Xmaj9 and Xaug9 || Xm9 Xdim9 || X9
                if (third or sus) and fifth and seventh:
                    lead = '9'
                    ninth = True

                # else (add 9)
                else:
                    add.append(itoa[14])


            # min-10
            case 15:

                # add #9
                add.append(itoa[15])


            # maj-10
            case 16:

                # add b11
                add.append(itoa[16])


            # perf-11
            case 17:

                # Xmaj11 | Xm11 || X11
                if ninth:
                    lead = '11'
                    eleventh = True

                # else (add 11)
                else:
                    add.append(itoa[17])


            # aug 11 || dim 12
            case 18:

                # add #11
                add.append(itoa[18])


            # case 19:


            # min-13
            case 20:

                # else (add b13)
                add.append(itoa[20])


            # maj-13
            case 21:

                # Xmaj13 || Xm13 || X13
                if eleventh:
                    lead = '13'

                # else (add 13)
                add.append(itoa[21])

    root = notes[0]
    jsus = 'sus' + (' '.join(sus))
    jadd = '(' + (' '.join(add)) + ')'

    # was unsure if format strings have `if else` functionality
    name = '{}{}{}{}{}'.format(root, triad if triad else "", lead if lead else "", jsus if sus else '', jadd if add else "")

    chord = {}

    chord['name'] = name
    chord['root'] = root
    chord['conciseness'] = 1 + len(lead) + len(sus) + len(add)

    return chord


def what_chord(notes):

    notes = clean_notes(notes)

    if not notes:
        return None

    # use itertools.permutations to generate permutations
    perms = list(permutations(notes))

    inversions = []
    for perm in perms:

        # convert perms into integer notation
        iperm = note_to_int(perm)

        # then generate intervals (called inversions here)
        inversions.append(get_intervals(iperm))

    # {}'notes': ['C', 'Eb', 'G'], 'name': 'Cm', 'root': 'C', 'conciseness': 1}
    chords = []
    names = []

    for i, inversion in enumerate(inversions):

        # detect and skip invalid inversions with clean_inversions()
        if not check_inversion(inversion):
            continue

        # store important information for db tables
        perm = perms[i]
        chord = get_name(inversion, perm)
        chord['inversion'] = perm

        if chord['name'] in names:
            continue            

        names.append(chord['name'])

        chords.append(chord)

    return chords

