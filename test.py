from helpers import note_to_int, get_intervals, get_name
from itertools import permutations

input = ('C', 'E', 'F#', 'Ab', 'B', 'Db')

inversions = list(permutations(input))

versions = []
intervals = []
chords = {}

# generate integer notation-'ified' inversions
for inversion in inversions:
    versions.append(note_to_int(inversion))

# calculate intervals for each inversion
for version in versions:
    intervals.append(get_intervals(version))

# generate names for each inversion
    # while retaining access to the inversion's alphabetic notation
for i, interval in enumerate(intervals):
    name = get_name(interval, inversions[i])
    
    if not name:
        continue
    
    # at this point, add entry into 
    chords[inversions[i]] = name

# # filter out empty inversions and sort remainder by probability
# cleaned = clean_chords(chords)

for chord, name in chords.items():
    print(f"{chord} : {name}")