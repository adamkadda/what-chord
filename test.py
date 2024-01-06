from helpers import note_to_int, get_intervals
from itertools import permutations

c_minor = ("C", "Eb", "G")

inversions = list(permutations(c_minor))

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
    name = get_chord(interval, inversion[i])
    chords[inversion[i]] = name

# filter out empty inversions and sort remainder by probability
cleaned = clean_chords(chords)
