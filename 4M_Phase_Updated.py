from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import csv # to read in csv files/logs  
from datetime import datetime # to get current date for file choosing  with 3Nback
import random

####------------TASK PARAMETERS------------ ####


#------------ MEMORY TEST PARAMETERS ------------ #
nback_trial_num_all = 250 # number of nback trials overall
nback_p_targets = 0.16 # percentage of targets you want
total_targets = int(nback_trial_num_all*nback_p_targets) # num targets, 40

old_image_num = nback_trial_num_all - total_targets # of old images
new_image_num = 84 #number of lures
mem_trial_num = old_image_num + new_image_num #number of memory trials total
mem_ISI = 0.5 # in seconds
mem_trial_dur = 30 # in seconds
mem_block_num = 3 # number of blocks (294 trials can be divided into 2, 3, 6, or 7(?) blocks)


####------------ EXPERIMENT SETUP------------ ####

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
# Store info about the experiment session
psychopyVersion = '3.2.4'
expName = 'builder_test'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], 'memory_data', expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/marlietandoc/Desktop/NSYNCH/builder_test.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess


#reads in the shuffled memory trial order created in nback_phase
os.chdir(os.getcwd() + '/data/logs') #set wd to data

with open(expInfo['participant'] + '_mem_trial_order.csv', 'r') as f:
  reader = csv.reader(f)
  mem_trial_order = list(reader)

#opens log for info of age
with open(expInfo['participant'] + '.csv', 'r') as f:
  reader = csv.reader(f)
  level_log = list(reader)

os.chdir(_thisDir) #resets dir back to normal

#adds age to data
expInfo['age'] = int(level_log[1][0])



#############################################
### -------------START MEM TEST ------ -#####
#############################################

#MEMORY TEST STUFF


# Initialize components for Routine "mem_inst_1_routine"
mem_inst_1_routineClock = core.Clock()

# memory game icon (top middle)
icon = visual.ImageStim(
    win=win, name='icon',
    image='images/mem_icon.png', mask=None,
    ori=0, pos=(0,325), size=(850,160),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# intro slide 1
mem_inst_1 = visual.ImageStim(
    win=win, name='mem_inst_1',
    image='images/mem_inst/1.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_inst_2_routine"
mem_inst_2_routineClock = core.Clock()
# intro slide 2
meminst2 = visual.ImageStim(
    win=win, name='meminst2',
    image='images/mem_inst/2.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_inst_3_routine"
mem_inst_3_routineClock = core.Clock()
# intro slide 3
meminst3 = visual.ImageStim(
    win=win, name='meminst3',
    image='images/mem_inst/3.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_inst_4_routine"
mem_inst_4_routineClock = core.Clock()
# intro slide 4
meminst4 = visual.ImageStim(
    win=win, name='meminst4',
    image='images/mem_inst/4.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_inst_5_routine"
mem_inst_5_routineClock = core.Clock()
# intro slide 5
meminst5 = visual.ImageStim(
    win=win, name='meminst5',
    image='images/mem_inst/5.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_inst_5_routine_2"
mem_inst_5_routine_2Clock = core.Clock()
# intro slide 6
mem6thing = visual.ImageStim(
    win=win, name='mem6thing',
    image='images/mem_inst/6.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "mem_inst_1_routine"-------
t = 0
mem_inst_1_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_1_routineComponents = [mem_inst_1, key_resp_2]
for thisComponent in mem_inst_1_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_1_routine"-------
# slide 1
while continueRoutine:
    # get current time
    t = mem_inst_1_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *mem_inst_1* updates
    if t >= 0.0 and mem_inst_1.status == NOT_STARTED:
        # keep track of start time/frame for later
        mem_inst_1.tStart = t
        mem_inst_1.frameNStart = frameN  # exact frame index
        mem_inst_1.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_2.keys = theseKeys[-1]  # just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_1_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_1_routine"-------
for thisComponent in mem_inst_1_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_2.keys in ['', [], None]:  # No response was made
    key_resp_2.keys=None
thisExp.nextEntry()
# the Routine "mem_inst_1_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "mem_inst_2_routine"-------
t = 0
mem_inst_2_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_3 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_2_routineComponents = [meminst2, key_resp_3]
for thisComponent in mem_inst_2_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_2_routine"-------
# slide 2
while continueRoutine:
    # get current time
    t = mem_inst_2_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *meminst2* updates
    if t >= 0.0 and meminst2.status == NOT_STARTED:
        # keep track of start time/frame for later
        meminst2.tStart = t
        meminst2.frameNStart = frameN  # exact frame index
        meminst2.setAutoDraw(True)
    
    # *key_resp_3* updates
    if t >= 0.0 and key_resp_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_3.tStart = t
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_3.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_3.keys = theseKeys[-1]  # just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_2_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_2_routine"-------
for thisComponent in mem_inst_2_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys=None

thisExp.nextEntry()
# the Routine "mem_inst_2_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "mem_inst_3_routine"-------
t = 0
mem_inst_3_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_4 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_3_routineComponents = [meminst3, key_resp_4]
for thisComponent in mem_inst_3_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_3_routine"-------
# slide 3
while continueRoutine:
    # get current time
    t = mem_inst_3_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *meminst3* updates
    if t >= 0.0 and meminst3.status == NOT_STARTED:
        # keep track of start time/frame for later
        meminst3.tStart = t
        meminst3.frameNStart = frameN  # exact frame index
        meminst3.setAutoDraw(True)
    
    # *key_resp_4* updates
    if t >= 0.0 and key_resp_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_4.tStart = t
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_4.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_4.keys = theseKeys[-1]  # just the last key pressed
            key_resp_4.rt = key_resp_4.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_3_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_3_routine"-------
for thisComponent in mem_inst_3_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_4.keys in ['', [], None]:  # No response was made
    key_resp_4.keys=None

thisExp.nextEntry()
# the Routine "mem_inst_3_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "mem_inst_4_routine"-------
t = 0
mem_inst_4_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_5 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_4_routineComponents = [meminst4, key_resp_5]
for thisComponent in mem_inst_4_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_4_routine"-------
# slide 4
while continueRoutine:
    # get current time
    t = mem_inst_4_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *meminst4* updates
    if t >= 0.0 and meminst4.status == NOT_STARTED:
        # keep track of start time/frame for later
        meminst4.tStart = t
        meminst4.frameNStart = frameN  # exact frame index
        meminst4.setAutoDraw(True)
    
    # *key_resp_5* updates
    if t >= 0.0 and key_resp_5.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_5.tStart = t
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_5.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_5.keys = theseKeys[-1]  # just the last key pressed
            key_resp_5.rt = key_resp_5.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_4_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_4_routine"-------
for thisComponent in mem_inst_4_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_5.keys in ['', [], None]:  # No response was made
    key_resp_5.keys=None

thisExp.nextEntry()
# the Routine "mem_inst_4_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "mem_inst_5_routine"-------
t = 0
mem_inst_5_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_6 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_5_routineComponents = [meminst5, key_resp_6]
for thisComponent in mem_inst_5_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_5_routine"-------
# slide 5
while continueRoutine:
    # get current time
    t = mem_inst_5_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *meminst5* updates
    if t >= 0.0 and meminst5.status == NOT_STARTED:
        # keep track of start time/frame for later
        meminst5.tStart = t
        meminst5.frameNStart = frameN  # exact frame index
        meminst5.setAutoDraw(True)
    
    # *key_resp_6* updates
    if t >= 0.0 and key_resp_6.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_6.tStart = t
        key_resp_6.frameNStart = frameN  # exact frame index
        key_resp_6.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_6.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_6.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_6.keys = theseKeys[-1]  # just the last key pressed
            key_resp_6.rt = key_resp_6.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_5_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_5_routine"-------
for thisComponent in mem_inst_5_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_6.keys in ['', [], None]:  # No response was made
    key_resp_6.keys=None

thisExp.nextEntry()
# the Routine "mem_inst_5_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "mem_inst_5_routine_2"-------
t = 0
mem_inst_5_routine_2Clock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_7 = event.BuilderKeyResponse()
# keep track of which components have finished
mem_inst_5_routine_2Components = [mem6thing, key_resp_7]
for thisComponent in mem_inst_5_routine_2Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "mem_inst_5_routine_2"-------
# slide 6
while continueRoutine:
    # get current time
    t = mem_inst_5_routine_2Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *mem6thing* updates
    if t >= 0.0 and mem6thing.status == NOT_STARTED:
        # keep track of start time/frame for later
        mem6thing.tStart = t
        mem6thing.frameNStart = frameN  # exact frame index
        mem6thing.setAutoDraw(True)
    
    # *key_resp_7* updates
    if t >= 0.0 and key_resp_7.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_7.tStart = t
        key_resp_7.frameNStart = frameN  # exact frame index
        key_resp_7.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_7.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_7.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_7.keys = theseKeys[-1]  # just the last key pressed
            key_resp_7.rt = key_resp_7.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mem_inst_5_routine_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mem_inst_5_routine_2"-------
for thisComponent in mem_inst_5_routine_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_7.keys in ['', [], None]:  # No response was made
    key_resp_7.keys=None

thisExp.nextEntry()
# the Routine "mem_inst_5_routine_2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


# Initialize components for Routine "mem_trial"
# start trial
mem_trialClock = core.Clock()
# stimulus image
mem_trial_image = visual.ImageStim(
    win=win, name='mem_trial_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
# button for if it is a new image
new_button = visual.ImageStim(
    win=win, name='new_button',
    image='images/new_button.png', mask=None,
    ori=0, pos=(-200, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
# button for if it is an old image
old_button = visual.ImageStim(
    win=win, name='old_button',
    image='images/old_button.png', mask=None,
    ori=0, pos=(200, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
# Initialize components for Routine "mem_trial_rate"
mem_trial_rateClock = core.Clock()
# secondary image shown to determine how certain you are it was an old/new image
mem_trial_image_con = visual.ImageStim(
    win=win, name='mem_trial_image_con',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
# image scale shown to determine how certain you are that it was an old/new image
mem_con_scale = visual.ImageStim(
    win=win, name='mem_con_scale',
    image= 'images/mem_rating_scale.png', mask=None,
    ori=0, pos=(0, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
# white box surrounding image
polygon = visual.Rect(
    win=win, name='polygon',
    width=(500, 500)[0], height=(500, 500)[1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0, interpolate=True)
# image for the break between image sets
mem_break = visual.ImageStim(
    win=win, name='mem_break',
    image='images/mem_inst/break.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# -------------------------------------------------------------------------------------------
# programming of order images are presented

#set up handler to look after randomisation of conditions etc
# has trial occur in sequential order repeating mem_trial_num times
memory_trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=list(range(mem_trial_num)), #HARDCODE
    seed=None, name='memory_trials')
thisExp.addLoop(memory_trials)  # add the loop to the experiment
thisMemory_trial = memory_trials.trialList[0]  # so we can initialise stimuli with some values
#abbreviate parameter names if possible (e.g. rgb = thisMemory_trial.rgb)
#if thisMemory_trial != None:
#    for paramName in thisMemory_trial:
#        exec('{} = thisMemory_trial[paramName]'.format(paramName))

mem_trial_count = 0
icon.setImage('images/mem_icon.png')

# Initialize components for Routine "mem_inst_1_routine"
mem_trialClock = core.Clock()

# getting required images to be shown 
#33_nback_data_2019_Dec_20_1312.csv file types llook like this
# get current date in specific format
curr_date = datetime.today().strftime('%Y_%b_%d')
Nback_filepath = expInfo['participant'] + '_nback_data_' + curr_date
Nback_filename = ''
# getting the matching file for the memory phase
for filenm in os.listdir('./data'):
    root, ext = os.path.splitext(filenm)
    if root.startswith(Nback_filepath) and ext == '.csv':
        Nback_filename =  filenm

trial_data = []
with open('./data/' + Nback_filename, 'r') as f:
    # reading the csv file line by line
    trials_list = csv.reader(f, delimiter=',',)
    for trial in trials_list:
        # only take data we need
        if trial[7] != '':
            try:
                trial[8] = int(trial[8])
                trial[9] = int(trial[9])
            except:
                print('header')
            trial_data.append(trial[7:10])
# remove header from data list
del trial_data[0]

# randomize order of the data for display
random.shuffle(trial_data)

used_images = set()
used_object_images = set()
used_face_images = set()
all_unique_object_images = set()
all_unique_face_images = set()
control_list = []

face_image_attended = {}
obj_image_attended = {}

# getting list of non-repeated images
for item in trial_data:
    curr_face_len = len(all_unique_face_images)
    curr_obj_len = len(all_unique_object_images)
    # items can have same number if face or object so you must differentiate
    all_unique_face_images.add(item[1])
    all_unique_object_images.add(item[2])
    
    # keeping track of attended for the corresponding images
    if item[0] == 'face' and len(all_unique_face_images) > curr_face_len:
            face_image_attended[item[1]] = 1
    elif item[0] == 'object' and len(all_unique_face_images) > curr_face_len:
            face_image_attended[item[1]] = 0
    
    if item[0] == 'face' and len(all_unique_object_images) > curr_obj_len:
            obj_image_attended[item[2]] = 0
    elif item[0] == 'object' and len(all_unique_object_images) > curr_obj_len:
            obj_image_attended[item[2]] = 1
# break data into two

count = 0

# creating the control list
for i in range(len(trial_data)):
    # length should be half of the unique face images as it stores half of unique face images and half of unique object images
    if (len(control_list)) == (len(all_unique_face_images)/2):
        break
    # ensure no repeats
    if (trial_data[i][1] not in used_face_images) and (trial_data[i][2] not in used_object_images):
        control_list.append(trial_data[i])
        # adding face and object image to used images
        used_face_images.add(trial_data[i][1])
        used_object_images.add(trial_data[i][2])

# getting list of non control images (difference between set of unique images and set of already used images for control)
rand_face_images = list(all_unique_face_images.difference(used_face_images))
rand_object_images = list(all_unique_object_images.difference(used_object_images))

# used to differentiate face and object images - could be done in one loop but this is safer
for i in range(len(rand_face_images)):
    rand_face_images[i] = ['f', rand_face_images[i], 'old', 'randomly']

for i in range(len(rand_object_images)):
    rand_object_images[i] = ['o', rand_object_images[i], 'old', 'randomly']

# combine for all images
all_image_list = rand_face_images + rand_object_images

new_images = []
# adding new images to list of images
with open('./data/logs/' + expInfo['participant'] + '_mem_trial_order.csv', 'r') as f:
    # reading the csv file line by line
    images_list = csv.reader(f, delimiter=',',)
    for image in images_list:
        # only take data we need
        if image[2] == 'new':
            # keeps track of cat, id, old/new, presented w/o order or randomly, attended
            all_image_list.append([image[1], int(image[0]), 'new', 'randomly', image[3]])
            new_images.append([image[1], int(image[0]), 'new', 'randomly', image[3]])

# adding items in control list to list of images
for item in control_list:
    all_image_list.append(item)

# randomize the order of image presentation
random.shuffle(all_image_list)

count = 0
# updating image list to show control images in the correct order
for item in all_image_list:
    # if isinstance(item, list):
    if (item[0] == 'face') or (item[0] == 'object'):
        control_index = all_image_list.index(item)
        temp = item
        # if the target cat is face, show face first, if it is object, show object first
        if (item[0] == 'face'):
            # append with abbreviation to know correct dir for image
            first,second = ['f', item[1], 'old', 'ordered'], ['o', item[2], 'old', 'ordered']
        elif (item[0] == 'object'):
            first,second = ['o', item[2], 'old', 'ordered'], ['f', item[1], 'old', 'ordered']
        else:
            print('Error, non face or object element found')
            break
        all_image_list[control_index] = second
        all_image_list.insert(control_index, first)

# appending the attended variable
for i in range(len(all_image_list)):
    if (all_image_list[i][2] == 'old'):
        if all_image_list[i][0] == 'o':
            attended = obj_image_attended[all_image_list[i][1]]
            all_image_list[i].append(attended)
        elif all_image_list[i][0] == 'f':
            attended = face_image_attended[all_image_list[i][1]]
            all_image_list[i].append(attended)

mem_trial_count = 0
mem_trial_num = len(all_image_list)
#print(mem_trial_num)
# ------ MAIN MEMORY LOOP -------------#
for thisMemory_trial in range(mem_trial_num): #number of trials
    # trials occur in 4 blocks of size 440/4
    # code for the breaks between image sets
    if (thisMemory_trial != 0) & (thisMemory_trial%(mem_trial_num/mem_block_num) == 0): #if time for block break
        # ------Prepare to start Routine "mem_block_break"-------
        mem_block_breakClock = core.Clock()
        t = 0
        mem_block_breakClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_5 = event.BuilderKeyResponse()
        # keep track of which components have finished
        mem_block_breakComponents = [mem_break, key_resp_5]
        for thisComponent in mem_block_breakComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "mem_block_break"-------
        while continueRoutine:
            # get current time
            t = mem_block_breakClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *mem_break* updates
            if t >= 0.0 and mem_break.status == NOT_STARTED:
                # keep track of start time/frame for later
                mem_break.tStart = t
                mem_break.frameNStart = frameN  # exact frame index
                mem_break.setAutoDraw(True)
            
            # *key_resp_5* updates
            if t >= 0.0 and key_resp_5.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_5.tStart = t
                key_resp_5.frameNStart = frameN  # exact frame index
                key_resp_5.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_5.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_5.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_5.rt = key_resp_5.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in mem_block_breakComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "mem_block_break"-------
        for thisComponent in mem_block_breakComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_5.keys in ['', [], None]:  # No response was made
            key_resp_5.keys=None

        # the Routine "mem_block_break" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

    # ------------------------------------------------------------
    currentLoop = memory_trials

    # current_mem_image = mem_trial_order[mem_trial_count][0] #figures out this loops image ID
    # current_image_cat = mem_trial_order[mem_trial_count][1] #figures out this loops category (face or object)
    # current_image_type = mem_trial_order[mem_trial_count][2] #figures out this loops trial type (old or new)
        # attended = mem_trial_order[mem_trial_count][3]


    current_image_cat = all_image_list[mem_trial_count][0] # get image category (face or object)
    current_mem_image = all_image_list[mem_trial_count][1] # get image id
    current_image_type = all_image_list[mem_trial_count][2] # get if image is old or new
    current_presentation_type = all_image_list[mem_trial_count][3] # get if image was presented randomly or ordered
    attended = all_image_list[mem_trial_count][4] # attended
  

    mem_trial_count = mem_trial_count + 1 # updates my trial counter

    # choose the image based on the category
    if current_image_type != 'new':
        if current_image_cat == 'f':
            mem_img_path = 'face_images/'
        else:
            mem_img_path = 'object_images/'
    # TO REMOVE IF PATH NOT DIFFERENTIATED BASED ON NEW OR OLD
    else:
        if current_image_cat == 'f':
            mem_img_path = 'face_images/'
        else:
            mem_img_path = 'object_images/'



    # mem_img_path = 'object_images/'

    #set opacity
    # mem_trial_image.setOpacity(0.5)
    # mem_trial_image_con.setOpacity(0.5)

    # ------Prepare to start Routine "mem_trial"-------
    t = 0
    mem_trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(20)
    # update component parameters for each repeat
    key_resp_mem_old_new = event.BuilderKeyResponse()
    # choosed image based on the current trial order
    # IMPORTANT
    mem_trial_image.setImage(mem_img_path + str(current_mem_image) + '.jpg')

    # keep track of which components have finished
    mem_trialComponents = [icon,polygon,mem_trial_image, key_resp_mem_old_new, new_button, old_button]
    for thisComponent in mem_trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "mem_trial"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = mem_trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
                # *icon* updates
        if t >= 0.0 and icon.status == NOT_STARTED:
            # keep track of start time/frame for later
            icon.tStart = t
            icon.frameNStart = frameN  # exact frame index
            icon.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if icon.status == STARTED and t >= frameRemains:
            icon.setAutoDraw(False)
        
        # *polygon* updates
        if t >= 0.0 and polygon.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon.tStart = t
            polygon.frameNStart = frameN  # exact frame index
            polygon.setAutoDraw(True)
        frameRemains = 0.0 + 1000 - win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon.status == STARTED and t >= frameRemains:
            polygon.setAutoDraw(False)
        
        # *mem_trial_image* updates
        if t >= 0.0 and mem_trial_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            mem_trial_image.tStart = t
            mem_trial_image.frameNStart = frameN  # exact frame index
            mem_trial_image.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if mem_trial_image.status == STARTED and t >= frameRemains:
            mem_trial_image.setAutoDraw(False)
        
        # *key_resp_mem_old_new* updates
        if t >= 0.0 and key_resp_mem_old_new.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_mem_old_new.tStart = t
            key_resp_mem_old_new.frameNStart = frameN  # exact frame index
            key_resp_mem_old_new.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_mem_old_new.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if key_resp_mem_old_new.status == STARTED and t >= frameRemains:
            key_resp_mem_old_new.status = STOPPED
        if key_resp_mem_old_new.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_mem_old_new.keys = theseKeys[-1]  # just the last key pressed
                key_resp_mem_old_new.rt = key_resp_mem_old_new.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # *new_button* updates
        if t >= 0.0 and new_button.status == NOT_STARTED:
            # keep track of start time/frame for later
            new_button.tStart = t
            new_button.frameNStart = frameN  # exact frame index
            new_button.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if new_button.status == STARTED and t >= frameRemains:
            new_button.setAutoDraw(False)
        
        # *old_button* updates
        if t >= 0.0 and old_button.status == NOT_STARTED:
            # keep track of start time/frame for later
            old_button.tStart = t
            old_button.frameNStart = frameN  # exact frame index
            old_button.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if old_button.status == STARTED and t >= frameRemains:
            old_button.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mem_trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "mem_trial"-------
    for thisComponent in mem_trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_mem_old_new.keys in ['', [], None]:  # No response was made
        key_resp_mem_old_new.keys=None
    memory_trials.addData('key_resp_mem_old_new.keys',key_resp_mem_old_new.keys)
    if key_resp_mem_old_new.keys != None:  # we had a response
        memory_trials.addData('key_resp_mem_old_new.rt', key_resp_mem_old_new.rt)
    
    #calculates if resp (old new judgment is correct)
    if key_resp_mem_old_new.keys == 'f':
        if current_image_type == 'old':
           response_corr = 1
        else:
           response_corr = 0
    elif key_resp_mem_old_new.keys == 'j':
        if current_image_type == 'new':
           response_corr = 1
        else:
           response_corr = 0
           
    #adds other wanted variables to dataframe
    memory_trials.addData('trial_num',mem_trial_count)
    memory_trials.addData('mem_image',current_mem_image)
    memory_trials.addData('category',current_image_cat)
    memory_trials.addData('trial_type',current_image_type)
    memory_trials.addData('correct',response_corr)
    memory_trials.addData('attended',attended)
    memory_trials.addData('ordered', current_presentation_type)
    # ------Prepare to start Routine "mem_trial_rate"-------
    t = 0
    mem_trial_rateClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(20.000000)
    
    if key_resp_mem_old_new: # if the list contains at least one entry,
       continueRoutine = True
    else:
       continueRoutine = False # don't show this feedback routine
    
    # update component parameters for each repeat
    key_resp_mem_confidence = event.BuilderKeyResponse()
    mem_trial_image_con.setImage(mem_img_path + str(current_mem_image) + '.jpg')
    # keep track of which components have finished
    mem_trial_rateComponents = [icon,polygon,mem_trial_image_con, key_resp_mem_confidence, mem_con_scale]
    for thisComponent in mem_trial_rateComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "mem_trial_rate"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = mem_trial_rateClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
                        # *icon* updates
        if t >= 0.0 and icon.status == NOT_STARTED:
            # keep track of start time/frame for later
            icon.tStart = t
            icon.frameNStart = frameN  # exact frame index
            icon.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if icon.status == STARTED and t >= frameRemains:
            icon.setAutoDraw(False)
        
                # *polygon* updates
        if t >= 0.0 and polygon.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon.tStart = t
            polygon.frameNStart = frameN  # exact frame index
            polygon.setAutoDraw(True)
        frameRemains = 0.0 + 1000 - win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon.status == STARTED and t >= frameRemains:
            polygon.setAutoDraw(False)
        
        # *mem_trial_image_con* updates
        if t >= 0.0 and mem_trial_image_con.status == NOT_STARTED:
            # keep track of start time/frame for later
            mem_trial_image_con.tStart = t
            mem_trial_image_con.frameNStart = frameN  # exact frame index
            mem_trial_image_con.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if mem_trial_image_con.status == STARTED and t >= frameRemains:
            mem_trial_image_con.setAutoDraw(False)
        
        # *key_resp_mem_confidence* updates
        if t >= 0.0 and key_resp_mem_confidence.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_mem_confidence.tStart = t
            key_resp_mem_confidence.frameNStart = frameN  # exact frame index
            key_resp_mem_confidence.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_mem_confidence.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if key_resp_mem_confidence.status == STARTED and t >= frameRemains:
            key_resp_mem_confidence.status = STOPPED
        if key_resp_mem_confidence.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_mem_confidence.keys = theseKeys[-1]  # just the last key pressed
                key_resp_mem_confidence.rt = key_resp_mem_confidence.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # *mem_con_scale* updates
        if t >= 0.0 and mem_con_scale.status == NOT_STARTED:
            # keep track of start time/frame for later
            mem_con_scale.tStart = t
            mem_con_scale.frameNStart = frameN  # exact frame index
            mem_con_scale.setAutoDraw(True)
        frameRemains = 0.0 + 1000- win.monitorFramePeriod * 0.75  # most of one frame period left
        if mem_con_scale.status == STARTED and t >= frameRemains:
            mem_con_scale.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mem_trial_rateComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "mem_trial_rate"-------
    for thisComponent in mem_trial_rateComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_mem_confidence.keys in ['', [], None]:  # No response was made
        key_resp_mem_confidence.keys=None
    memory_trials.addData('key_resp_mem_confidence.keys',key_resp_mem_confidence.keys)
    if key_resp_mem_confidence.keys != None:  # we had a response
        memory_trials.addData('key_resp_mem_confidence.rt', key_resp_mem_confidence.rt)
    thisExp.nextEntry()

#completed 1 repeats of 'memory_trials'

all_done = visual.ImageStim(
    win=win, name='all_done',
    image='images/done.jpg', mask=None,
    ori=0, pos=(0, 0), size=(1200,675),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)


# ------Prepare to start Routine "done_routine"-------
done_routineClock = core.Clock()
t = 0
done_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_5 = event.BuilderKeyResponse()
# keep track of which components have finished
done_routineComponents = [all_done, key_resp_5]
for thisComponent in done_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "done_routine"-------
while continueRoutine:
    # get current time
    t = done_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *all_done* updates
    if t >= 0.0 and all_done.status == NOT_STARTED:
        # keep track of start time/frame for later
        all_done.tStart = t
        all_done.frameNStart = frameN  # exact frame index
        all_done.setAutoDraw(True)
    
    # *key_resp_5* updates
    if t >= 0.0 and key_resp_5.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_5.tStart = t
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_5.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_5.keys = theseKeys[-1]  # just the last key pressed
            key_resp_5.rt = key_resp_5.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in done_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "done_routine"-------
for thisComponent in done_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_5.keys in ['', [], None]:  # No response was made
    key_resp_5.keys=None

# the Routine "done_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()




# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()


