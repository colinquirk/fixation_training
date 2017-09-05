"""Code used to train subjects to focus their eyes in the center of the screen.

If participants move their eyes, they should notice a flash.

To use, simply open and run the code in psychopy.
Alternativly, import and run yourself.

The main function is run_FixationTraining, which takes a bool as
show_distractor and an int as nTrials.

Pressing 'q' while the program is expecting a key press will quit.

This code was originally written by Albert Chen under the supervision of Colin
Quirk. Small changes in usage and formatting have been made by Colin Quirk.
"""

from __future__ import division

import random
import sys

import psychopy.visual
import psychopy.event
import psychopy.core

win = psychopy.visual.Window(
    units='pix', color=(-1, -1, -1), colorSpace='rgb', fullscr=True)


def wait():
    keys = psychopy.event.waitKeys(
        maxWait='inf', keyList=['space', 'q'], modifiers=False,
        timeStamped=False)

    if 'q' in keys:
        sys.exit(0)

intro_text = psychopy.visual.TextStim(
    win, text="Welcome to eye-fixation training. Press the spacebar to begin.")

instruction_text_1 = psychopy.visual.TextStim(
    win, text="A circular gray field will soon appear. Keep your eyes on " +
    "the black dot in the center and try to minimize eye movements. " +
    "If you see a random dot pattern pop out from the gray field, this " +
    "means that you have made an eye movement. " +
    "Press the spacebar to continue.")

instruction_text_2 = psychopy.visual.TextStim(
    win, text="There will be multiple intervals, each of which lasts for 3 " +
    "to 5 seconds.")

instruction_text_3 = psychopy.visual.TextStim(
    win, text="There may be an arrow pointing towards one side of the " +
    "screen. If so, a white line will appear on that side. Try to pay " +
    "attention to the direction the line points WITHOUT moving your eyes. " +
    "Press space to start.")

instruction_text = [instruction_text_1, instruction_text_2, instruction_text_3]

interval_text = psychopy.visual.TextStim(
    win, text="Press the spacebar to start interval.")

fixation = psychopy.visual.Circle(
    win, radius=25, lineColor=(-1, -1, -1), fillColor=(-1, -1, -1))
left_arrow = psychopy.visual.TextStim(win, text='<', height=40)
right_arrow = psychopy.visual.TextStim(win, text='>', height=40)

field_1 = psychopy.visual.ImageStim(win, mask='circle', image='Static_1.png')
field_2 = psychopy.visual.ImageStim(win, mask='circle', image='Static_2.png')
field_1.size = 800
field_2.size = 800
white_dot_buffer = psychopy.visual.BufferImageStim(win, stim=[field_1])
black_dot_buffer = psychopy.visual.BufferImageStim(win, stim=[field_2])

distractor_1 = ['/']*15
distractor_2 = ['\\']*15
distractors = distractor_1 + distractor_2
random.shuffle(distractors)

left = [-1]*15
right = [1]*15
position_side = left + right
random.shuffle(position_side)

intro_text.draw()
win.flip()
wait()

for text in instruction_text:
    text.draw()
    win.flip()
    wait()

psychopy.core.wait(1.5)


def run_FixationTraining(show_distractor=False, nTrials=5):
    for x in range(nTrials):
        distractor_stim = psychopy.visual.TextStim(
            win, text=distractors[x], pos=(300*position_side[x], 0),
            bold=False, height=50)

        white_first = True
        interval_text.draw()
        win.flip()
        wait()

        if show_distractor:
            for frameN in range(50):
                if position_side[x] == -1:
                    left_arrow.draw()
                    win.flip()
                else:
                    right_arrow.draw()
                    win.flip()

        timer = psychopy.core.Clock()
        display_time = random.uniform(1.5, 2.5)

        while timer.getTime() < display_time:
            if white_first:
                white_dot_buffer.draw()
                fixation.draw()
                win.flip()
                white_first = False
            else:
                black_dot_buffer.draw()
                fixation.draw()
                win.flip()
                white_first = True

        if show_distractor:
            for frameN in range(4):
                if white_first:
                    white_dot_buffer.draw()
                    white_first = False
                else:
                    black_dot_buffer.draw()
                    white_first = True
                distractor_stim.draw()
                fixation.draw()
                win.flip()

        timer.reset()
        while timer.getTime() < display_time:
            if white_first:
                white_dot_buffer.draw()
                fixation.draw()
                win.flip()
                white_first = False
            else:
                black_dot_buffer.draw()
                fixation.draw()
                win.flip()
                white_first = True

        win.flip(clearBuffer=True)
        timer.reset()

if __name__ == '__main__':
    run_FixationTraining()
    run_FixationTraining(True, 25)

win.close()
