# NSYNCH: Calibration Phase
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

####------------TASK PARAMETERS------------ ####

#TITRATION PARAMETERS
titr_image_num = 100 # number of trials in a level of the tiration phase
trial_per_block = 50
titr_level_up = 0.80 # % needed to progress to 2 back
titr_level_down = 0.80 # % needed to fall back down to 1 back
nback_image_dur = 1.5 # image duration in seconds 1.5
nback_ISI = 0.75 #0.75
nback_trial_dur = nback_image_dur + nback_ISI  #in seconds 
titr_p_targets = 0.16 # percentage of targets you want
targets_per_block = int(trial_per_block*titr_p_targets)
titr_unique_images = int(titr_image_num*2*(1-titr_p_targets))
titr_block_num = 2

####------------ EXPERIMENT SETUP------------ ####

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.0.0b12'
expName = 'calibration_phase'  # from the Builder filename that created this script
expInfo = {'participant': '', 'age':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel'
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

#sets seed to ensure each phases randomizes lists equally to carry over
np.random.seed(int(expInfo['participant']))

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

# Initialize components for Routine "welcome"
welcomeClock = core.Clock()

#### ------ CREATES TRIAL LISTS -------- ####

#creates an array of numbers representing all the images for each category
scene_list = list(range(titr_unique_images))
animal_list = list(range(titr_unique_images))

#shuffles lists
shuffle(scene_list)
shuffle(animal_list)

animal_list_1 = animal_list[0:trial_per_block-targets_per_block]
animal_list_2 = animal_list[trial_per_block-targets_per_block:titr_image_num-targets_per_block*2]

scene_list_1 = scene_list[0:trial_per_block-targets_per_block]
scene_list_2 = scene_list[trial_per_block-targets_per_block:titr_image_num-targets_per_block*2]


# intializes block and trial counter for titr
titr_block_count = 0
titr_trial_count = 0
num_corr = 0

#function that creates 1back trials
def shuffle_1back(images, repeats):
    shuffle(images)#shuffle list, first len(repeats) are the ones to repeat
    repeated_images = images[0:repeats]
    shuffle(images) 

    for i in range(len(images)+repeats):
      if(images[i] in repeated_images):
        images.insert(i+1,images[i])
        repeated_images.remove(images[i])

#function that creates 2back trials
def shuffle_2back(images, repeats):
    shuffle(images)#shuffle list, first len(repeats) are the ones to repeat
    repeated_images = images[0:repeats]
    shuffle(images) 

    if(images[len(images)-1] in repeated_images and images[len(images)-2] not in repeated_images):  #its a problem if last element is repeated, unless last 2 are   
      images[len(images)-2], images[len(images)-1] = images[len(images)-1], images[len(images)-2]     #if last element is repeated, swap with second last

    for i in range(len(images)+repeats):
      if(images[i] in repeated_images):
        images.insert(i+2,images[i])
        repeated_images.remove(images[i])

#stores animals into blocks

#Shuffles scene list and animal list for 1 back

shuffle_1back(animal_list_1,int(titr_p_targets*trial_per_block))
shuffle_1back(scene_list_1,int(titr_p_targets*trial_per_block))

shuffle_1back(animal_list_2,int(titr_p_targets*trial_per_block))
shuffle_1back(scene_list_2,int(titr_p_targets*trial_per_block))


#variables for 1 back
block_cat = 'animal'
inst_cat_path = 'images/animal_1back/'
current_icon = 'images/animal_icon.png'
curr_animal_list = animal_list_1
curr_scene_list = scene_list_1
level = 1 # always lvl 1 for first time through
response_corr_tally = 0 # keeps track of correct responses
target_corr_tally = 0
#instruction time
for block in range(titr_block_num):
    if block == 1:
        block_cat = 'scene'
        inst_cat_path = 'images/scene_1back/'
        current_icon = 'images/place_icon.png'
        curr_animal_list = animal_list_2
        curr_scene_list = scene_list_2
        

    # Initialize components for Routine "trial"
    trialClock = core.Clock()
    inst_image = visual.ImageStim(
        win=win, name='inst_image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)


    # Initialize components for Routine "trial2"
    trial2Clock = core.Clock()
    animate_1 = visual.ImageStim(
        win=win, name='animate_1',
        image=inst_cat_path + '5.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)
    animate_2 = visual.ImageStim(
        win=win, name='animate_2',
        image=inst_cat_path + '6.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    animate_3 = visual.ImageStim(
        win=win, name='animate_3',
        image=inst_cat_path + '7.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    animate_4 = visual.ImageStim(
        win=win, name='animate_4',
        image=inst_cat_path + '8.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-3.0)

    # Initialize components for Routine "trial"
    trialClock = core.Clock()
    inst_image = visual.ImageStim(
        win=win, name='inst_image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)


    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

    # set up handler to look after randomisation of conditions etc
    prac_inst_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('testtrialorderinst.xlsx', selection='0:4'),
        seed=None, name='prac_inst_trials')
    #thisExp.addLoop(prac_inst_trials)  # add the loop to the experiment
    thisPrac_inst_trial = prac_inst_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial.rgb)
    if thisPrac_inst_trial != None:
        for paramName in thisPrac_inst_trial:
            exec('{} = thisPrac_inst_trial[paramName]'.format(paramName))

    for thisPrac_inst_trial in prac_inst_trials:
        currentLoop = prac_inst_trials
        # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial.rgb)
        if thisPrac_inst_trial != None:
            for paramName in thisPrac_inst_trial:
                exec('{} = thisPrac_inst_trial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        inst_image.setImage(inst_cat_path + inst_image_path)
        key_resp_2 = event.BuilderKeyResponse()
        if block_cat == 'animal':
           inst_cat_path = 'images/animal_1back/'
        else:
           inst_cat_path = 'images/scene_1back/'
        # keep track of which components have finished
        trialComponents = [inst_image, key_resp_2]
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "trial"-------
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *inst_image* updates
            if t >= 0.0 and inst_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                inst_image.tStart = t
                inst_image.frameNStart = frameN  # exact frame index
                inst_image.setAutoDraw(True)
            
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
                theseKeys = event.getKeys(keyList=['space', 'r'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str('')) or (key_resp_2.keys == ''):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str('').lower() == 'none':
               key_resp_2.corr = 1;  # correct non-response
            else:
               key_resp_2.corr = 0;  # failed to respond (incorrectly)
        # store data for prac_inst_trials (TrialHandler)

        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'prac_inst_trials'

    prac_redo = True
    while prac_redo: 
        # ------Prepare to start Routine "trial2"-------
        t = 0
        trial2Clock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(4.000000)
        # update component parameters for each repeat
        # keep track of which components have finished
        trial2Components = [animate_1, animate_2, animate_3, animate_4]
        for thisComponent in trial2Components:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "trial2"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trial2Clock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *animate_1* updates
            if t >= 0.0 and animate_1.status == NOT_STARTED:
                # keep track of start time/frame for later
                animate_1.tStart = t
                animate_1.frameNStart = frameN  # exact frame index
                animate_1.setAutoDraw(True)
            frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
            if animate_1.status == STARTED and t >= frameRemains:
                animate_1.setAutoDraw(False)
            
            # *animate_2* updates
            if t >= 1 and animate_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                animate_2.tStart = t
                animate_2.frameNStart = frameN  # exact frame index
                animate_2.setAutoDraw(True)
            frameRemains = 1 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
            if animate_2.status == STARTED and t >= frameRemains:
                animate_2.setAutoDraw(False)
            
            # *animate_3* updates
            if t >= 2 and animate_3.status == NOT_STARTED:
                # keep track of start time/frame for later
                animate_3.tStart = t
                animate_3.frameNStart = frameN  # exact frame index
                animate_3.setAutoDraw(True)
            frameRemains = 2 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
            if animate_3.status == STARTED and t >= frameRemains:
                animate_3.setAutoDraw(False)
            
            # *animate_4* updates
            if t >= 3 and animate_4.status == NOT_STARTED:
                # keep track of start time/frame for later
                animate_4.tStart = t
                animate_4.frameNStart = frameN  # exact frame index
                animate_4.setAutoDraw(True)
            frameRemains = 3 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
            if animate_4.status == STARTED and t >= frameRemains:
                animate_4.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trial2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "trial2"-------
        for thisComponent in trial2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        # set up handler to look after randomisation of conditions etc
        prac_inst_trials_2 = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions('testtrialorderinst.xlsx', selection='7:13'),
            seed=None, name='prac_inst_trials_2')
        #thisExp.addLoop(prac_inst_trials_2)  # add the loop to the experiment
        thisPrac_inst_trial_2 = prac_inst_trials_2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial_2.rgb)
        if thisPrac_inst_trial_2 != None:
            for paramName in thisPrac_inst_trial_2:
                exec('{} = thisPrac_inst_trial_2[paramName]'.format(paramName))

        for thisPrac_inst_trial_2 in prac_inst_trials_2:
            currentLoop = prac_inst_trials_2
            # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial_2.rgb)
            if thisPrac_inst_trial_2 != None:
                for paramName in thisPrac_inst_trial_2:
                    exec('{} = thisPrac_inst_trial_2[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            inst_image.setImage(inst_cat_path + inst_image_path)
            key_resp_2 = event.BuilderKeyResponse()
            if block_cat == 'animal':
               inst_cat_path = 'images/animal_1back/'
            else:
               inst_cat_path = 'images/scene_1back/'
            # keep track of which components have finished
            trialComponents = [inst_image, key_resp_2]
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "trial"-------
            while continueRoutine:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *inst_image* updates
                if t >= 0.0 and inst_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    inst_image.tStart = t
                    inst_image.frameNStart = frameN  # exact frame index
                    inst_image.setAutoDraw(True)
                
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
                    theseKeys = event.getKeys(keyList=['space', 'r'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_2.rt = key_resp_2.clock.getTime()
                        # was this 'correct'?
                        if (key_resp_2.keys == str('')) or (key_resp_2.keys == ''):
                            key_resp_2.corr = 1
                        else:
                            key_resp_2.corr = 0
                        # a response ends the routine
                        continueRoutine = False
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_2.keys in ['', [], None]:  # No response was made
                key_resp_2.keys=None
                # was no response the correct answer?!
                if str('').lower() == 'none':
                   key_resp_2.corr = 1;  # correct non-response
                else:
                   key_resp_2.corr = 0;  # failed to respond (incorrectly)
            # store data for prac_inst_trials_2 (TrialHandler)

            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
            
    # completed 1 repeats of 'prac_inst_trials_2'


        #practice trials
        if block == 0:
            prac_trial_order_a = [1,2,3,3,4] #hardcoded (third element repeats)
            prac_trial_order_s = [1,1,2,3,4] #hardcoded (first element repeats)
        else:
            prac_trial_order_s = [1,2,3,3,4] #hardcoded (third element repeats)
            prac_trial_order_a = [1,1,2,3,4] #hardcoded (first element repeats)

        #### START PRAC 1-BACK

            
        ##############################################
        #### ------INITIALIZE VARIABLES -----------###
        ##############################################

        # Initialize components for Routine "nback_block_break"
        # Initialize components for Routine "nback_trial"
        nback_trialClock = core.Clock()

        icon = visual.ImageStim(
            win=win, name='icon',
            image= current_icon, mask=None,
            ori=0, pos=(0,325), size=(850,160),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
            
        text = visual.TextStim(win=win, name='text',
            text='+',
            font='Arial',
            pos=(0, 0), height=20, wrapWidth=None, ori=0, 
            color='white', colorSpace='rgb', opacity=1, 
            languageStyle='LTR',
            depth=5.0)

        polygon = visual.Rect(
            win=win, name='polygon',
            width=(500, 500)[0], height=(0, 0)[1],
            ori=0, pos=(0, 0),
            lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
            fillColor=[1,1,1], fillColorSpace='rgb',
            opacity=1, depth=0.0, interpolate=True)
          
        animal_image = visual.ImageStim(
            win=win, name='animal_image',
            image='sin', mask=None,
            ori=0, pos=(0, 0), size=(500,500),
            color=[1,1,1], colorSpace='rgb', opacity=0.50,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-2)
        scene_image = visual.ImageStim(
            win=win, name='scene_image',
            image='sin', mask=None,
            ori=0, pos=(0, 0), size=(500,500),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-0.5)
            
          
    #------ PRACTICE LOOP---------#
        for thisNback_loop in range(len(prac_trial_order_a)): 

            show_animal = prac_trial_order_a[thisNback_loop] # what animal image to show
            show_scene = prac_trial_order_s[thisNback_loop] #what scene image to sho
            # ------Prepare to start Routine "nback_trial"-------
            t = 0
            nback_trialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            scene_image.setImage('practice_scenes/' + str(show_scene) + '.jpg')
            animal_image.setImage('practice_animals/' + str(show_animal) + '.png')
            key_resp_nback = event.BuilderKeyResponse()
            
            # keep track of which components have finished
            nback_trialComponents = [icon, polygon, animal_image, scene_image, key_resp_nback,text]
            for thisComponent in nback_trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "nback_trial"-------
            while continueRoutine:
                # get current time
                t = nback_trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *icon* updates
                if t >= 0.0 and icon.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    icon.tStart = t
                    icon.frameNStart = frameN  # exact frame index
                    icon.setAutoDraw(True)
                frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if icon.status == STARTED and t >= frameRemains:
                    icon.setAutoDraw(False)
                
                # *polygon* updates
                if t >= 0.0 and polygon.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    polygon.tStart = t
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if polygon.status == STARTED and t >= frameRemains:
                    polygon.setAutoDraw(False)

                # *text* updates
                if t >= 0.0 and text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text.tStart = t
                    text.frameNStart = frameN  # exact frame index
                    text.setAutoDraw(True)
                frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text.status == STARTED and t >= frameRemains:
                    text.setAutoDraw(False)
                
                # *scene_image* updates
                if t >= 0.0 and scene_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    scene_image.tStart = t
                    scene_image.frameNStart = frameN  # exact frame index
                    scene_image.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                if scene_image.status == STARTED and t >= frameRemains:
                    scene_image.setAutoDraw(False)
                
                # *animal_image* updates
                if t >= 0.0 and animal_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animal_image.tStart = t
                    animal_image.frameNStart = frameN  # exact frame index
                    animal_image.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                if animal_image.status == STARTED and t >= frameRemains:
                    animal_image.setAutoDraw(False)
                
                # *key_resp_nback* updates
                if t >= 0.0 and key_resp_nback.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_nback.tStart = t
                    key_resp_nback.frameNStart = frameN  # exact frame index
                    key_resp_nback.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_nback.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                frameRemains = 0.0 + 1.35- win.monitorFramePeriod * 0.75  # most of one frame period left
                if key_resp_nback.status == STARTED and t >= frameRemains:
                    key_resp_nback.status = STOPPED
                if key_resp_nback.status == STARTED:
                    theseKeys = event.getKeys()
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if key_resp_nback.keys == []:  # then this was the first keypress
                            key_resp_nback.keys = theseKeys[0]  # just the first key pressed
                            key_resp_nback.rt = key_resp_nback.clock.getTime()
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in nback_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "nback_trial"-------
            for thisComponent in nback_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)


            
            # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
    # completed 1 repeats of 'practice trials'

        all_done = visual.ImageStim(
            win=win, name='all_done',
            image='images/hangofit.jpg', mask=None,
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
                theseKeys = event.getKeys(keyList=['space','r'])
                
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

        if key_resp_5.keys != 'r':
            prac_redo = False
    
    
    #rsets trial count
    titr_trial_count = 0

    # set up handler to look after randomisation of conditions etc
    nback_loop = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=list(range(len(curr_animal_list))), # number of trials per block 
        seed=None, name='nback_loop')
    thisExp.addLoop(nback_loop)  # add the loop to the experiment
    thisNback_loop = nback_loop.trialList[0]  # so we can initialise stimuli with some values

    #------ NBACK MAIN TRIAL LOOP ---------#
    for thisNback_loop in nback_loop: #CHANGE TO NBACK_LOOP  IN NBACK_LOOP NO CAPS
        currentLoop = nback_loop
        
        show_animal = curr_animal_list[titr_trial_count] # what animal image to show
        show_scene = curr_scene_list[titr_trial_count] #what scene image to sho
        # ------Prepare to start Routine "nback_trial"-------
        t = 0
        nback_trialClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        scene_image.setImage('scene_images/' + str(show_scene) + '.jpg')
        animal_image.setImage('animal_images/' + str(show_animal) + '.png')
        key_resp_nback = event.BuilderKeyResponse()
        
        # keep track of which components have finished
        nback_trialComponents = [icon, polygon, animal_image, scene_image, key_resp_nback,text]
        for thisComponent in nback_trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "nback_trial"-------
        while continueRoutine:
            # get current time
            t = nback_trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *icon* updates
            if t >= 0.0 and icon.status == NOT_STARTED:
                # keep track of start time/frame for later
                icon.tStart = t
                icon.frameNStart = frameN  # exact frame index
                icon.setAutoDraw(True)
            frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
            if icon.status == STARTED and t >= frameRemains:
                icon.setAutoDraw(False)
                
            # *text* updates
            if t >= 0.0 and text.status == NOT_STARTED:
                # keep track of start time/frame for later
                text.tStart = t
                text.frameNStart = frameN  # exact frame index
                text.setAutoDraw(True)
            frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
            if text.status == STARTED and t >= frameRemains:
                text.setAutoDraw(False)
            
            # *polygon* updates
            if t >= 0.0 and polygon.status == NOT_STARTED:
                # keep track of start time/frame for later
                polygon.tStart = t
                polygon.frameNStart = frameN  # exact frame index
                polygon.setAutoDraw(True)
            frameRemains = 0.0 + nback_image_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
            if polygon.status == STARTED and t >= frameRemains:
                polygon.setAutoDraw(False)
            
            # *scene_image* updates
            if t >= 0.0 and scene_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                scene_image.tStart = t
                scene_image.frameNStart = frameN  # exact frame index
                scene_image.setAutoDraw(True)
            frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
            if scene_image.status == STARTED and t >= frameRemains:
                scene_image.setAutoDraw(False)
            
            # *animal_image* updates
            if t >= 0.0 and animal_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                animal_image.tStart = t
                animal_image.frameNStart = frameN  # exact frame index
                animal_image.setAutoDraw(True)
            frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
            if animal_image.status == STARTED and t >= frameRemains:
                animal_image.setAutoDraw(False)
            
            # *key_resp_nback* updates
            if t >= 0.0 and key_resp_nback.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_nback.tStart = t
                key_resp_nback.frameNStart = frameN  # exact frame index
                key_resp_nback.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_nback.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
            if key_resp_nback.status == STARTED and t >= frameRemains:
                key_resp_nback.status = STOPPED
            if key_resp_nback.status == STARTED:
                theseKeys = event.getKeys()
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if key_resp_nback.keys == []:  # then this was the first keypress
                        key_resp_nback.keys = theseKeys[0]  # just the first key pressed
                        key_resp_nback.rt = key_resp_nback.clock.getTime()
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in nback_trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "nback_trial"-------
        for thisComponent in nback_trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_nback.keys in ['', [], None]:  # No response was made
            key_resp_nback.keys=None
        nback_loop.addData('key_resp_nback.keys',key_resp_nback.keys)
        if key_resp_nback.keys != None:  # we had a response
            nback_loop.addData('key_resp_nback.rt', key_resp_nback.rt)
                
            #calculates trial type
        if titr_trial_count == 0:
          target_repeat  = 0
        
        if (block_cat == 'animal') & (curr_animal_list[titr_trial_count] == curr_animal_list[titr_trial_count-level]):
          target_repeat = 1
        elif (block_cat == 'scene') & (curr_scene_list[titr_trial_count] == curr_scene_list[titr_trial_count-level]):
          target_repeat = 1
        else:
          target_repeat = 0
        
        if titr_trial_count == 0:
          lure_repeat = 0
        if (block_cat == 'scene') & (curr_animal_list[titr_trial_count] == curr_animal_list[titr_trial_count-level]):
          lure_repeat = 1
        elif (block_cat == 'animal') & (curr_scene_list[titr_trial_count] == curr_scene_list[titr_trial_count-level]):
          lure_repeat = 1
        else:
          lure_repeat = 0
        
        #calculates if response was correct
        if target_repeat == 1:
            if key_resp_nback.keys != None:
                response_corr = 1
            else:
                response_corr = 0
        elif target_repeat == 0:
            if key_resp_nback.keys != None:
                response_corr = 0
            else:
                response_corr = 1
        
        #tallys score to calculate % correct later for targets
        if (target_repeat == 1) & (response_corr == 1):
           target_corr_tally = target_corr_tally + 1
           
        if (response_corr == 1):
           response_corr_tally = response_corr_tally + 1
                
        #adds other variables to dataframe
        nback_loop.addData('nback_level', level)
        nback_loop.addData('target_cat', block_cat)
        nback_loop.addData('animal_img', show_animal)
        nback_loop.addData('scene_img', show_scene)
        nback_loop.addData('trial_resp_corr', response_corr)
        nback_loop.addData('trial_num', titr_trial_count)
        nback_loop.addData('target_repeat', target_repeat)
        nback_loop.addData('lure_repeat', lure_repeat)
        nback_loop.addData('block_num', block+1)
        nback_loop.addData('total_resp_corr', response_corr_tally)
        nback_loop.addData('total_target_corr', target_corr_tally)
        
        #updates trial counts
        titr_trial_count = titr_trial_count + 1 
        
        
        # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
    
# completed 1 repeats of 'nback_loop'
print(response_corr_tally)
print(target_corr_tally)

#calculates percent correct
p_correct_1back = target_corr_tally/(titr_image_num*titr_p_targets)
print(p_correct_1back)

#determines if did good enough job to go to 2back
if p_correct_1back > titr_level_up:
        go_to_2back = True
else:
        go_to_2back = False
        set_level = 1
        

#if they passed 2 back goes to 2 back instructions
if go_to_2back:
    
    #figures out what images to use for 2 back
    animal_list_2back = animal_list[titr_image_num-targets_per_block*2: titr_image_num*2-targets_per_block*4]

    animal_list_3 = animal_list_2back[0:42]
    animal_list_4 = animal_list_2back[42:]
    
    scene_list_2back = scene_list[titr_image_num-targets_per_block*2: titr_image_num*2-targets_per_block*4]

    scene_list_3 = scene_list_2back[0:42]
    scene_list_4 = scene_list_2back[42:]


    # creates 2 back trial order with repeats
    shuffle_2back(animal_list_3,int(titr_p_targets*trial_per_block))
    shuffle_2back(scene_list_3,int(titr_p_targets*trial_per_block))

    shuffle_2back(animal_list_4,int(titr_p_targets*trial_per_block))
    shuffle_2back(scene_list_4,int(titr_p_targets*trial_per_block))

        
    #variables for 2 back
    block_cat = 'animal'
    inst_cat_path = 'images/animal_2back/'
    current_icon = 'images/animal_icon.png'
    curr_animal_list = animal_list_3
    curr_scene_list = scene_list_3
    level = 2 #2back 
    response_corr_tally = 0 # keeps track of correct responses
    target_corr_tally = 0
    block = 0


    #instruction time
    for block in range(titr_block_num):
        if block == 1:
            block_cat = 'scene'
            inst_cat_path = 'images/scene_2back/'
            current_icon = 'images/place_icon.png'
            curr_animal_list = animal_list_4
            curr_scene_list = scene_list_4
            

        # Initialize components for Routine "trial"
        trialClock = core.Clock()
        inst_image = visual.ImageStim(
            win=win, name='inst_image',
            image='sin', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)


        # Initialize components for Routine "trial2"
        trial2Clock = core.Clock()
        animate_1 = visual.ImageStim(
            win=win, name='animate_1',
            image=inst_cat_path + '5.jpg', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)
        animate_2 = visual.ImageStim(
            win=win, name='animate_2',
            image=inst_cat_path + '6.jpg', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-1.0)
        animate_3 = visual.ImageStim(
            win=win, name='animate_3',
            image=inst_cat_path + '7.jpg', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-2.0)
        animate_4 = visual.ImageStim(
            win=win, name='animate_4',
            image=inst_cat_path + '8.jpg', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=-3.0)

        # Initialize components for Routine "trial"
        trialClock = core.Clock()
        inst_image = visual.ImageStim(
            win=win, name='inst_image',
            image='sin', mask=None,
            ori=0, pos=(0, 0), size=(1200,675),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128, interpolate=True, depth=0.0)


        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

        # set up handler to look after randomisation of conditions etc
        prac_inst_trials = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions('testtrialorderinst.xlsx', selection='0:4'),
            seed=None, name='prac_inst_trials')
        #thisExp.addLoop(prac_inst_trials)  # add the loop to the experiment
        thisPrac_inst_trial = prac_inst_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial.rgb)
        if thisPrac_inst_trial != None:
            for paramName in thisPrac_inst_trial:
                exec('{} = thisPrac_inst_trial[paramName]'.format(paramName))

        for thisPrac_inst_trial in prac_inst_trials:
            currentLoop = prac_inst_trials
            # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial.rgb)
            if thisPrac_inst_trial != None:
                for paramName in thisPrac_inst_trial:
                    exec('{} = thisPrac_inst_trial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            inst_image.setImage(inst_cat_path + inst_image_path)
            key_resp_2 = event.BuilderKeyResponse()
            if block_cat == 'animal':
               inst_cat_path = 'images/animal_2back/'
            else:
               inst_cat_path = 'images/scene_2back/'
            # keep track of which components have finished
            trialComponents = [inst_image, key_resp_2]
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "trial"-------
            while continueRoutine:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *inst_image* updates
                if t >= 0.0 and inst_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    inst_image.tStart = t
                    inst_image.frameNStart = frameN  # exact frame index
                    inst_image.setAutoDraw(True)
                
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
                    theseKeys = event.getKeys(keyList=['space', 'r'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_2.rt = key_resp_2.clock.getTime()
                        # was this 'correct'?
                        if (key_resp_2.keys == str('')) or (key_resp_2.keys == ''):
                            key_resp_2.corr = 1
                        else:
                            key_resp_2.corr = 0
                        # a response ends the routine
                        continueRoutine = False
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_2.keys in ['', [], None]:  # No response was made
                key_resp_2.keys=None
                # was no response the correct answer?!
                if str('').lower() == 'none':
                   key_resp_2.corr = 1;  # correct non-response
                else:
                   key_resp_2.corr = 0;  # failed to respond (incorrectly)
            # store data for prac_inst_trials (TrialHandler)

            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 1 repeats of 'prac_inst_trials'

        prac_redo = True
        while prac_redo: 
            # ------Prepare to start Routine "trial2"-------
            t = 0
            trial2Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(4.000000)
            # update component parameters for each repeat
            # keep track of which components have finished
            trial2Components = [animate_1, animate_2, animate_3, animate_4]
            for thisComponent in trial2Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "trial2"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = trial2Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *animate_1* updates
                if t >= 0.0 and animate_1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animate_1.tStart = t
                    animate_1.frameNStart = frameN  # exact frame index
                    animate_1.setAutoDraw(True)
                frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
                if animate_1.status == STARTED and t >= frameRemains:
                    animate_1.setAutoDraw(False)
                
                # *animate_2* updates
                if t >= 1 and animate_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animate_2.tStart = t
                    animate_2.frameNStart = frameN  # exact frame index
                    animate_2.setAutoDraw(True)
                frameRemains = 1 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
                if animate_2.status == STARTED and t >= frameRemains:
                    animate_2.setAutoDraw(False)
                
                # *animate_3* updates
                if t >= 2 and animate_3.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animate_3.tStart = t
                    animate_3.frameNStart = frameN  # exact frame index
                    animate_3.setAutoDraw(True)
                frameRemains = 2 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
                if animate_3.status == STARTED and t >= frameRemains:
                    animate_3.setAutoDraw(False)
                
                # *animate_4* updates
                if t >= 3 and animate_4.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animate_4.tStart = t
                    animate_4.frameNStart = frameN  # exact frame index
                    animate_4.setAutoDraw(True)
                frameRemains = 3 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
                if animate_4.status == STARTED and t >= frameRemains:
                    animate_4.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trial2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "trial2"-------
            for thisComponent in trial2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)

            # set up handler to look after randomisation of conditions etc
            prac_inst_trials_2 = data.TrialHandler(nReps=1, method='sequential', 
                extraInfo=expInfo, originPath=-1,
                trialList=data.importConditions('testtrialorderinst.xlsx', selection='7:13'),
                seed=None, name='prac_inst_trials_2')
            #thisExp.addLoop(prac_inst_trials_2)  # add the loop to the experiment
            thisPrac_inst_trial_2 = prac_inst_trials_2.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial_2.rgb)
            if thisPrac_inst_trial_2 != None:
                for paramName in thisPrac_inst_trial_2:
                    exec('{} = thisPrac_inst_trial_2[paramName]'.format(paramName))

            for thisPrac_inst_trial_2 in prac_inst_trials_2:
                currentLoop = prac_inst_trials_2
                # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial_2.rgb)
                if thisPrac_inst_trial_2 != None:
                    for paramName in thisPrac_inst_trial_2:
                        exec('{} = thisPrac_inst_trial_2[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "trial"-------
                t = 0
                trialClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                # update component parameters for each repeat
                inst_image.setImage(inst_cat_path + inst_image_path)
                key_resp_2 = event.BuilderKeyResponse()
                if block_cat == 'animal':
                   inst_cat_path = 'images/animal_2back/'
                else:
                   inst_cat_path = 'images/scene_2back/'
                # keep track of which components have finished
                trialComponents = [inst_image, key_resp_2]
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "trial"-------
                while continueRoutine:
                    # get current time
                    t = trialClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *inst_image* updates
                    if t >= 0.0 and inst_image.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        inst_image.tStart = t
                        inst_image.frameNStart = frameN  # exact frame index
                        inst_image.setAutoDraw(True)
                    
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
                        theseKeys = event.getKeys(keyList=['space', 'r'])
                        
                        # check for quit:
                        if "escape" in theseKeys:
                            endExpNow = True
                        if len(theseKeys) > 0:  # at least one key was pressed
                            key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                            key_resp_2.rt = key_resp_2.clock.getTime()
                            # was this 'correct'?
                            if (key_resp_2.keys == str('')) or (key_resp_2.keys == ''):
                                key_resp_2.corr = 1
                            else:
                                key_resp_2.corr = 0
                            # a response ends the routine
                            continueRoutine = False
                    
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in trialComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "trial"-------
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                # check responses
                if key_resp_2.keys in ['', [], None]:  # No response was made
                    key_resp_2.keys=None
                    # was no response the correct answer?!
                    if str('').lower() == 'none':
                       key_resp_2.corr = 1;  # correct non-response
                    else:
                       key_resp_2.corr = 0;  # failed to respond (incorrectly)
                # store data for prac_inst_trials_2 (TrialHandler)

                # the Routine "trial" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
                
        # completed 1 repeats of 'prac_inst_trials_2'


            #practice trials
            if block == 0:
                prac_trial_order_a = [1,2,3,2,4] #hardcoded practice trials
                prac_trial_order_s = [1,2,1,3,4] #hardcoded 
            else:
                prac_trial_order_s = [1,2,3,2,4] #hardcoded 
                prac_trial_order_a = [1,2,1,3,4] #hardcoded

            #### START PRAC 1-BACK

                
            ##############################################
            #### ------INITIALIZE VARIABLES -----------###
            ##############################################

            # Initialize components for Routine "nback_block_break"
            # Initialize components for Routine "nback_trial"
            nback_trialClock = core.Clock()

            icon = visual.ImageStim(
                win=win, name='icon',
                image= current_icon, mask=None,
                ori=0, pos=(0,325), size=(850,160),
                color=[1,1,1], colorSpace='rgb', opacity=1,
                flipHoriz=False, flipVert=False,
                texRes=128, interpolate=True, depth=0.0)
                
            text = visual.TextStim(win=win, name='text',
                text='+',
                font='Arial',
                pos=(0, 0), height=20, wrapWidth=None, ori=0, 
                color='white', colorSpace='rgb', opacity=1, 
                languageStyle='LTR',
                depth=5.0)

            polygon = visual.Rect(
                win=win, name='polygon',
                width=(500, 500)[0], height=(0, 0)[1],
                ori=0, pos=(0, 0),
                lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                fillColor=[1,1,1], fillColorSpace='rgb',
                opacity=1, depth=0.0, interpolate=True)
              
            animal_image = visual.ImageStim(
                win=win, name='animal_image',
                image='sin', mask=None,
                ori=0, pos=(0, 0), size=(500,500),
                color=[1,1,1], colorSpace='rgb', opacity=0.5,
                flipHoriz=False, flipVert=False,
                texRes=128, interpolate=True, depth=-2)
            scene_image = visual.ImageStim(
                win=win, name='scene_image',
                image='sin', mask=None,
                ori=0, pos=(0, 0), size=(500,500),
                color=[1,1,1], colorSpace='rgb', opacity=1,
                flipHoriz=False, flipVert=False,
                texRes=128, interpolate=True, depth=-0.5)
                
              
        #------ PRACTICE LOOP---------#
            for thisNback_loop in range(len(prac_trial_order_a)): 

                show_animal = prac_trial_order_a[thisNback_loop] # what animal image to show
                show_scene = prac_trial_order_s[thisNback_loop] #what scene image to sho
                # ------Prepare to start Routine "nback_trial"-------
                t = 0
                nback_trialClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                # update component parameters for each repeat
                scene_image.setImage('practice_scenes/' + str(show_scene) + '.jpg')
                animal_image.setImage('practice_animals/' + str(show_animal) + '.png')
                key_resp_nback = event.BuilderKeyResponse()
                
                # keep track of which components have finished
                nback_trialComponents = [icon, polygon, animal_image, scene_image, key_resp_nback,text]
                for thisComponent in nback_trialComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "nback_trial"-------
                while continueRoutine:
                    # get current time
                    t = nback_trialClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *icon* updates
                    if t >= 0.0 and icon.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        icon.tStart = t
                        icon.frameNStart = frameN  # exact frame index
                        icon.setAutoDraw(True)
                    frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if icon.status == STARTED and t >= frameRemains:
                        icon.setAutoDraw(False)
                    
                    # *polygon* updates
                    if t >= 0.0 and polygon.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        polygon.tStart = t
                        polygon.frameNStart = frameN  # exact frame index
                        polygon.setAutoDraw(True)
                    frameRemains = 0.0 + nback_image_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if polygon.status == STARTED and t >= frameRemains:
                        polygon.setAutoDraw(False)

                    # *text* updates
                    if t >= 0.0 and text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        text.tStart = t
                        text.frameNStart = frameN  # exact frame index
                        text.setAutoDraw(True)
                    frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if text.status == STARTED and t >= frameRemains:
                        text.setAutoDraw(False)
                    
                    # *scene_image* updates
                    if t >= 0.0 and scene_image.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        scene_image.tStart = t
                        scene_image.frameNStart = frameN  # exact frame index
                        scene_image.setAutoDraw(True)
                    frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                    if scene_image.status == STARTED and t >= frameRemains:
                        scene_image.setAutoDraw(False)
                    
                    # *animal_image* updates
                    if t >= 0.0 and animal_image.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        animal_image.tStart = t
                        animal_image.frameNStart = frameN  # exact frame index
                        animal_image.setAutoDraw(True)
                    frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                    if animal_image.status == STARTED and t >= frameRemains:
                        animal_image.setAutoDraw(False)
                    
                    # *key_resp_nback* updates
                    if t >= 0.0 and key_resp_nback.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        key_resp_nback.tStart = t
                        key_resp_nback.frameNStart = frameN  # exact frame index
                        key_resp_nback.status = STARTED
                        # keyboard checking is just starting
                        win.callOnFlip(key_resp_nback.clock.reset)  # t=0 on next screen flip
                        event.clearEvents(eventType='keyboard')
                    frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if key_resp_nback.status == STARTED and t >= frameRemains:
                        key_resp_nback.status = STOPPED
                    if key_resp_nback.status == STARTED:
                        theseKeys = event.getKeys()
                        
                        # check for quit:
                        if "escape" in theseKeys:
                            endExpNow = True
                        if len(theseKeys) > 0:  # at least one key was pressed
                            if key_resp_nback.keys == []:  # then this was the first keypress
                                key_resp_nback.keys = theseKeys[0]  # just the first key pressed
                                key_resp_nback.rt = key_resp_nback.clock.getTime()
                    
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in nback_trialComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "nback_trial"-------
                for thisComponent in nback_trialComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)


                
                # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
        # completed 1 repeats of 'practice trials'

            all_done = visual.ImageStim(
                win=win, name='all_done',
                image='images/hangofit.jpg', mask=None,
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
                    theseKeys = event.getKeys(keyList=['space','r'])
                    
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

            if key_resp_5.keys != 'r':
                prac_redo = False
        
        


        #resets trial count
        titr_trial_count = 0

        level = 2 # always lvl 2
        
        # set up handler to look after randomisation of conditions etc
        nback_loop = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=list(range(len(curr_animal_list))), # number of trials per block #len(block_1_animal)
            seed=None, name='nback_loop')
        thisExp.addLoop(nback_loop)  # add the loop to the experiment
        thisNback_loop = nback_loop.trialList[0]  # so we can initialise stimuli with some values


              
        #------ NBACK MAIN TRIAL LOOP ---------#
        for thisNback_loop in nback_loop: #CHANGE TO NBACK_LOOP  IN NBACK_LOOP NO CAPS
            currentLoop = nback_loop
            
            show_animal = curr_animal_list[titr_trial_count] # what animal image to show
            show_scene = curr_scene_list[titr_trial_count] #what scene image to sho
            # ------Prepare to start Routine "nback_trial"-------
            t = 0
            nback_trialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            scene_image.setImage('scene_images/' + str(show_scene) + '.jpg')
            animal_image.setImage('animal_images/' + str(show_animal) + '.png')
            key_resp_nback = event.BuilderKeyResponse()
            
            # keep track of which components have finished
            nback_trialComponents = [icon, text, polygon, animal_image, scene_image, key_resp_nback]
            for thisComponent in nback_trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "nback_trial"-------
            while continueRoutine:
                # get current time
                t = nback_trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *icon* updates
                if t >= 0.0 and icon.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    icon.tStart = t
                    icon.frameNStart = frameN  # exact frame index
                    icon.setAutoDraw(True)
                frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if icon.status == STARTED and t >= frameRemains:
                    icon.setAutoDraw(False)
                
                # *text* updates
                if t >= 0.0 and text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text.tStart = t
                    text.frameNStart = frameN  # exact frame index
                    text.setAutoDraw(True)
                frameRemains = 0.0 + nback_trial_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text.status == STARTED and t >= frameRemains:
                    text.setAutoDraw(False)
                 
                # *polygon* updates
                if t >= 0.0 and polygon.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    polygon.tStart = t
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur- win.monitorFramePeriod * 0.75  # most of one frame period left
                if polygon.status == STARTED and t >= frameRemains:
                    polygon.setAutoDraw(False)
                
                # *scene_image* updates
                if t >= 0.0 and scene_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    scene_image.tStart = t
                    scene_image.frameNStart = frameN  # exact frame index
                    scene_image.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                if scene_image.status == STARTED and t >= frameRemains:
                    scene_image.setAutoDraw(False)
                
                # *animal_image* updates
                if t >= 0.0 and animal_image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    animal_image.tStart = t
                    animal_image.frameNStart = frameN  # exact frame index
                    animal_image.setAutoDraw(True)
                frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
                if animal_image.status == STARTED and t >= frameRemains:
                    animal_image.setAutoDraw(False)
                
                # *key_resp_nback* updates
                if t >= 0.0 and key_resp_nback.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_nback.tStart = t
                    key_resp_nback.frameNStart = frameN  # exact frame index
                    key_resp_nback.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_nback.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                frameRemains = 0.0 + 1.35- win.monitorFramePeriod * 0.75  # most of one frame period left
                if key_resp_nback.status == STARTED and t >= frameRemains:
                    key_resp_nback.status = STOPPED
                if key_resp_nback.status == STARTED:
                    theseKeys = event.getKeys()
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if key_resp_nback.keys == []:  # then this was the first keypress
                            key_resp_nback.keys = theseKeys[0]  # just the first key pressed
                            key_resp_nback.rt = key_resp_nback.clock.getTime()
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in nback_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "nback_trial"-------
            for thisComponent in nback_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_nback.keys in ['', [], None]:  # No response was made
                key_resp_nback.keys=None
            nback_loop.addData('key_resp_nback.keys',key_resp_nback.keys)
            if key_resp_nback.keys != None:  # we had a response
                nback_loop.addData('key_resp_nback.rt', key_resp_nback.rt)
                    
                #calculates trial type
            if titr_trial_count == 0:
              target_repeat  = 0
              
            if titr_trial_count == 1:
              target_repeat  = 0
            
            if (block_cat == 'animal') & (curr_animal_list[titr_trial_count] == curr_animal_list[titr_trial_count-level]):
              target_repeat = 1
            elif (block_cat == 'scene') & (curr_scene_list[titr_trial_count] == curr_scene_list[titr_trial_count-level]):
              target_repeat = 1
            else:
              target_repeat = 0
            
            if titr_trial_count == 0:
              lure_repeat = 0
            if (block_cat == 'scene') & (curr_animal_list[titr_trial_count] == curr_animal_list[titr_trial_count-level]):
              lure_repeat = 1
            elif (block_cat == 'animal') & (curr_scene_list[titr_trial_count] == curr_scene_list[titr_trial_count-level]):
              lure_repeat = 1
            else:
              lure_repeat = 0
            
            #calculates if response was correct
            if target_repeat == 1:
                if key_resp_nback.keys != None:
                    response_corr = 1
                else:
                    response_corr = 0
            elif target_repeat == 0:
                if key_resp_nback.keys != None:
                    response_corr = 0
                else:
                    response_corr = 1

            #tallys score to calculate % correct later
            if (target_repeat == 1) & (response_corr == 1):
               target_corr_tally = target_corr_tally + 1
               
            if (response_corr == 1):
               response_corr_tally = response_corr_tally + 1
                
            #adds other variables to dataframe
            nback_loop.addData('nback_level', level)
            nback_loop.addData('target_cat', block_cat)
            nback_loop.addData('animal_img', show_animal)
            nback_loop.addData('scene_img', show_scene)
            nback_loop.addData('trial_resp_corr', response_corr)
            nback_loop.addData('trial_num', titr_trial_count)
            nback_loop.addData('target_repeat', target_repeat)
            nback_loop.addData('lure_repeat', lure_repeat)
            nback_loop.addData('block_num', block+1)
            nback_loop.addData('total_resp_corr', response_corr_tally)
            nback_loop.addData('total_target_corr', target_corr_tally)
            #updates trial counts
            titr_trial_count = titr_trial_count + 1 
            
            
            # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 1 repeats of 'nback_loop'
        
    print(response_corr_tally)
    print(target_corr_tally)

    #calculates percent correct
    p_correct_2back = target_corr_tally/(titr_image_num*titr_p_targets)

    #determines if did good enough job to stay at 2 back or fall down
    if p_correct_2back > titr_level_down:
            set_level = 2
    else:
            set_level = 1
            
            

#logs info to transfer to nback phase

os.chdir(os.getcwd() + '/data/logs') #set wd to data

level_log = [expInfo['participant'],expInfo['age'], set_level]

make_file = open(expInfo['participant'] + '.csv','w')

for i in level_log:
    make_file.write(str(i) + "\n")
make_file.close()

os.chdir(_thisDir)

#show done page

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
        theseKeys = event.getKeys()
        
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
