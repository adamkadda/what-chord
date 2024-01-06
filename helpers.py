def note_to_int(inversion):
    
    int_notation = {
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

    pitches = tuple(int_notation[note] for note in inversion)

    return pitches


def get_intervals(pitches):

    intervals = []

    for i, note in enumerate(pitches):
        if i == 0:
            # assign root note
            intervals.append(0)
        
        else:
            # if current note is 'lower' than prev
            if note < pitches[i - 1]:

                # interval = (12 + note) - prev
                ival = sum(intervals) + (12 + note) - pitches[i - 1]
                intervals.append(ival)

            # else, note must be 'higher'
            else:
                ival = sum(intervals) + (note - pitches[i - 1])
                intervals.append(ival)

    return tuple(intervals)



def get_name(intervals, notes):

    ivals = {
        'min-2': 1,
        'maj-2': 2,
        'min-3': 3,
        'maj-3': 4,
        'perf-4': 5,
        'aug-4': 6, 'dimd-5': 6,
        'perf-5': 7,
        'min-6': 8, 'aug-5': 8,
        'maj-6': 9,
        'min-7': 10,
        'maj-7': 11

    }
    
    name = []
    name.append(notes[0])

    return None