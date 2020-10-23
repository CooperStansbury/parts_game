"""
A simple tool to generate a list of chords under the contraint
that every chords must contain at least one note from the input list. 

Up to five-note chords
"""

import argparse
import ast
import numpy as np
import ast

# GLOBALS
global INTERVAL_2_NOTE
INTERVAL_2_NOTE = {1:'Ab', 2:'A', 3:'Bb', 4:'B', 
         5:'C', 6:'Db', 7:'D', 8:'Eb', 
         9:'E', 10:'F', 11:'Gb', 12:'G'}

global NOTE_2_INTERVAL
NOTE_2_INTERVAL = {y:x for x,y in INTERVAL_2_NOTE.items()}

global CHORD_DICT
CHORD_DICT = {
    'Power':[0, 7, np.nan, np.nan, np.nan],
    'Major':[0, 4, 7, np.nan, np.nan],
    'Major6':[0, 4, 7, 9, np.nan],
    'Major7' : [0, 4, 7, 11, np.nan],
    'Major69': [0, 4, 7, 9, 2], 
    'Major9':[0, 4, 7, 11, 2],
    'Minor':[0, 3, 7, np.nan, np.nan],
    'Minor6':[0, 3, 7, 9, np.nan],
    'Minor7' : [0, 3, 7, 10, np.nan],
    'Minor9' : [0, 3, 7, 10, 2],
    'Diminished':[0, 3, 6, np.nan, np.nan],
    'HalfDiminished':[0, 3, 6, 10, np.nan],
    'Diminished7':[0, 3, 6, 9, np.nan],
    'DiminishedMaj7':[0, 3, 6, 11, np.nan],
    'Aug':[0, 4, 8, np.nan, np.nan],

}


def coerce_input(_input):
    """A function to normalize input or throw a descriptive error

    Args:
        -input (list of str): the input chord notes
    Returns:
        - normed_input: capitalization corrected input
    Raises: 
        - ValueError: in the case that the notes are not valid note names
    """
    try:
        parsed_input = [x.strip().upper() for x in _input.split(",")]
        normed_input = [f"{x[0]}{x[1].lower()}" if len(x) == 2 else x for x in parsed_input]
        assert(len(np.setdiff1d(normed_input, list(NOTE_2_INTERVAL.keys()))) == 0)
    except:
        raise ValueError("Some input not recognized. Valid examples: `c, g, Ab`, `G, F, bb`")
    return normed_input


def print_detected_input(roots):
    """A function to print the input chord name 
    if detectable
    
    Args:
        - roots (list of str): chord notes
    Returns:
        - None: printing only
    """
    for chord_name, chord_ints in CHORD_DICT.items():
        if set(input_intervals) == set(chord_ints):
            rootname = f"{roots[0]} {chord_name}"
            print(f"\nInput Detected: {rootname}")


def print_all_chords(root_note):
    """A function to print chord dict given a root note
    
    Args:
        - root_note (string): the root of the chords
    Returns:
        - None: printing func only
    """

    root_ind = NOTE_2_INTERVAL[root_note]

    for i in range(5):
        print(f"{root_note} is note {(i+1)} in chord:")
        for chord_name, chord_ints in CHORD_DICT.items():
        
            # shift chord intervals by root note
            if root_ind > chord_ints[i]:
                shift = root_ind - chord_ints[i]
                raw_interval_trans = [x + shift for x in chord_ints]
                interval_trans = [(x - len(INTERVAL_2_NOTE)) if x > len(INTERVAL_2_NOTE) else x for x in raw_interval_trans]
            else:
                shift = chord_ints[i] - root_ind
                raw_interval_trans = [x - shift for x in chord_ints]
                interval_trans = [(x + len(INTERVAL_2_NOTE)) if x <= 0 else x for x in raw_interval_trans]

            stripNA = [x for x in interval_trans if not np.isnan(x)]
            chord_trans = [INTERVAL_2_NOTE[x] for x in stripNA]

            if len(chord_trans) > 0:
                new_root = INTERVAL_2_NOTE[stripNA[0]]
                print(f"\t{new_root} {chord_name} ({', '.join(chord_trans)})")



            # if not np.isnan(base):
            #     interval_trans = [(x % len(INTERVAL_2_NOTE))+1 if x > len(INTERVAL_2_NOTE) else x for x in interval_trans]
            #     chord_trans = [INTERVAL_2_NOTE[x] for x in interval_trans]

            #     print(f"\t{root_note} {chord_trans}")
                

if __name__ == "__main__":
    desc = """A Python3 commandline tool to generate chords based on seed notes. """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-root", default='C, E, G',
                        help="seed list of notes. first note is assume to be the root. flats are `b`.")

    args = parser.parse_args()
    roots = coerce_input(args.root)

    # get the inveral values based on the first note
    # of the input 
    root_ind = NOTE_2_INTERVAL[roots[0]]
    input_intervals = [(NOTE_2_INTERVAL[note] - root_ind) for note in roots]

    print_detected_input(roots)

    for idx, note in enumerate(roots):
        print(f"\n--------- Chords with {note} ({input_intervals[idx]} of root):")
        print_all_chords(note)
    