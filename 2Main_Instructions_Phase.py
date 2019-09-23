
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
import csv #to read and write csvs 


#------------ NBACK PARAMETERS ------------ #
nback_ISI = 0.75 #in seconds 0.5
nback_image_dur = 1.5
nback_trial_dur = nback_image_dur + nback_ISI  #in seconds 
nback_trial_num_all = 40 # number of nback trials overall
nback_trial_num = 20 # number of nback trials per block
nback_block_num = 2 # number of blocks for n-back
nback_p_targets = 0.16 # percentage of targets you want
total_targets = int(nback_trial_num_all*nback_p_targets) #80
targets_per_block =  total_targets/nback_block_num #20
nback_unique_images = int(nback_trial_num_all*(1-nback_p_targets))
hardcode_target_num = 3 
block_num = 2


####------------ EXPERIMENT SETUP------------ ####

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
# Store info about the experiment session
psychopyVersion = '3.0.0b12'
expName = 'main_instructions'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], 'practice_data', expInfo['date'])

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
    size=[1440, 900], fullscr=False, screen=0,
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


#gets level from calibration_phase by participant id string and reading the last (3rd) value in the list
os.chdir(os.getcwd() + '/data/logs') #set wd to data

with open(expInfo['participant'] + '.csv', 'r') as f:
  reader = csv.reader(f)
  level_log = list(reader)

level = int(level_log[2][0]) #gets set level! (either 1 or 2)

os.chdir(_thisDir)

#adds age to data
expInfo['age'] = int(level_log[1][0])

#### ------ CREATES TRIAL LISTS -------- ####

#assigns certain images to nback vs lures on the mem test
nback_object_list = list(range(nback_trial_num*2)) #objects assigned to nback

nback_face_list = list(range(nback_trial_num*2)) #objects assigned to nback

#shuffle
shuffle(nback_object_list)
shuffle(nback_face_list)



# intializes block and trial counter for nback
nback_block_count = 0
nback_trial_count = 0


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

#distributes block target nums
#if needed to jitter targets use this 
#target_jitter= [int(np.ceil(targets_per_block)),int(np.ceil(targets_per_block)),int(np.floor(targets_per_block)),int(np.floor(targets_per_block))]
target_jitter = [20,20,20,20] #for now

#stores faces + objects into blocks
block_1_face = nback_face_list[0:nback_trial_num]

block_2_face = nback_face_list[nback_trial_num:]

block_1_object = nback_object_list[0:nback_trial_num]

block_2_object = nback_object_list[nback_trial_num:]

#Shuffles face list and object list based on level
if level == 1: # if 1 back 
    shuffle_1back(block_1_face, hardcode_target_num)
    shuffle_1back(block_2_face,hardcode_target_num)

    
    nback_order_face = block_1_face + block_2_face 

    shuffle_1back(block_1_object,hardcode_target_num)
    shuffle_1back(block_2_object,hardcode_target_num)

    nback_order_ob = block_1_object + block_2_object 
    

else:# IF 2 BACK THEN this
    shuffle_2back(block_1_face, hardcode_target_num)
    shuffle_2back(block_2_face,hardcode_target_num)

    
    nback_order_face = block_1_face + block_2_face 

    shuffle_2back(block_1_object,hardcode_target_num)
    shuffle_2back(block_2_object,hardcode_target_num)

    nback_order_ob = block_1_object + block_2_object 
    

##############################################
#### ------INITIALIZE OBJECTS -----------#####
##############################################


# Initialize components for Routine "nback_ITI"
nback_ITIClock = core.Clock()

text = visual.TextStim(win=win, name='text',
    text='+',
    font='Arial',
    pos=(0, 0), height=20, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=5.0);

# Initialize components for Routine "nback_trial"
nback_trialClock = core.Clock()


polygon = visual.Rect(
    win=win, name='polygon',
    width=(500, 500)[0], height=(500, 500)[1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)

face_image = visual.ImageStim(
    win=win, name='face_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-0.5)
object_image = visual.ImageStim(
    win=win, name='object_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=0.5,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2)


# Initialize components for Routine "end"
endClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

##############################################
#### ------------START NBACK ---------- -#####
##############################################
block_cat = 'face'
curr_face_list = block_1_face
curr_object_list = block_1_object
curr_icon = 'images/face_icon.png'
for block_count in range(block_num):# FIND_ME
    if block_count == 1 :
        block_cat = 'object'
        curr_face_list = block_2_face
        curr_object_list = block_2_object
        
    if level == 1:
       if block_cat == 'face':
            inst_cat_path = 'images/face_inst/1/'
       else:
            inst_cat_path = 'images/thing_inst/1/'
    elif level == 2:
       if block_cat == 'face':
            inst_cat_path = 'images/face_inst/2/'
       else:
            inst_cat_path = 'images/thing_inst/2/'
        

    ###################
    # insert appropriate instructions loop here ####
    ###################
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
        image=inst_cat_path + '6.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)
    animate_2 = visual.ImageStim(
        win=win, name='animate_2',
        image=inst_cat_path + '7.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    animate_3 = visual.ImageStim(
        win=win, name='animate_3',
        image=inst_cat_path + '8.jpg', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    animate_4 = visual.ImageStim(
        win=win, name='animate_4',
        image=inst_cat_path + '9.jpg', mask=None,
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
    inst_trials = '0:5'
    if block_cat == 'object':
        inst_trials = '2:5' # skip first 2 instruction slides
        
        
    prac_inst_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('testtrialorderinst.xlsx', selection=inst_trials),
        seed=None, name='prac_inst_trials')
    thisExp.addLoop(prac_inst_trials)  # add the loop to the experiment
    thisPrac_inst_trial = prac_inst_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPrac_inst_trial.rgb)
    if thisPrac_inst_trial != None:
        for paramName in thisPrac_inst_trial:
            exec('{} = thisPrac_inst_trial[paramName]'.format(paramName))
            
    prac_redo = True 
    while prac_redo:
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
#            prac_inst_trials.addData('key_resp_2.keys',key_resp_2.keys)
#            prac_inst_trials.addData('key_resp_2.corr', key_resp_2.corr)
#            if key_resp_2.keys != None:  # we had a response
#                
#                prac_inst_trials.addData('key_resp_2.rt', key_resp_2.rt)
#            
            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 1 repeats of 'prac_inst_trials'


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
            trialList=data.importConditions('testtrialorderinst.xlsx', selection='9:14'),
            seed=None, name='prac_inst_trials_2')
        thisExp.addLoop(prac_inst_trials_2)  # add the loop to the experiment
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
#            prac_inst_trials_2.addData('key_resp_2.keys',key_resp_2.keys)
#            prac_inst_trials_2.addData('key_resp_2.corr', key_resp_2.corr)
#            if key_resp_2.keys != None:  # we had a response
#                prac_inst_trials_2.addData('key_resp_2.rt', key_resp_2.rt)
#            
            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        if key_resp_2.keys != 'r':
            print('yo')
            prac_redo = False
            
        # completed 1 repeats of 'prac_inst_trials_2'


    #rsets trial count
    nback_trial_count = 0
    if block_cat == 'object':
        curr_icon = 'images/ob_icon.png'
    
    icon = visual.ImageStim(
    win=win, name='icon',
    image= curr_icon, mask=None,
    ori=0, pos=(0,325), size=(850,160),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

    
    # set up handler to look after randomisation of conditions etc
    nback_loop = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=list(range(nback_trial_num)), # number of trials per block
        seed=None, name='nback_loop')
    thisExp.addLoop(nback_loop)  # add the loop to the experiment
    thisNback_loop = nback_loop.trialList[0]  # so we can initialise stimuli with some values

    
          
    #------ NBACK MAIN TRIAL LOOP ---------#
    for thisNback_loop in nback_loop: #CHANGE TO NBACK_LOOP  IN NBACK_LOOP NO CAPS
        currentLoop = nback_loop

        
        show_face = curr_face_list[nback_trial_count] # what face image to show
        show_object = curr_object_list[nback_trial_count] #what ob image to sho
        # ------Prepare to start Routine "nback_trial"-------
        t = 0
        nback_trialClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat

        object_image.setImage('practice_objects/' + str(show_object) + '.jpg')
        face_image.setImage('practice_faces/' + str(show_face) + '.jpg')
        key_resp_nback = event.BuilderKeyResponse()
        
        # keep track of which components have finished
        nback_trialComponents = [icon, polygon, face_image, object_image, key_resp_nback,text]
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
            
            # *object_image* updates
            if t >= 0.0 and object_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                object_image.tStart = t
                object_image.frameNStart = frameN  # exact frame index
                object_image.setAutoDraw(True)
            frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
            if object_image.status == STARTED and t >= frameRemains:
                object_image.setAutoDraw(False)
            
            # *face_image* updates
            if t >= 0.0 and face_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                face_image.tStart = t
                face_image.frameNStart = frameN  # exact frame index
                face_image.setAutoDraw(True)
            frameRemains = 0.0 + nback_image_dur - win.monitorFramePeriod * 0.75  # most of one frame period left
            if face_image.status == STARTED and t >= frameRemains:
                face_image.setAutoDraw(False)
            
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
        if nback_trial_count == 0:
          target_repeat  = 0
        
        if (block_cat == 'face') & (curr_face_list[nback_trial_count] == curr_face_list[nback_trial_count-level]):
          target_repeat = 1
        elif (block_cat == 'object') & (curr_object_list[nback_trial_count] == curr_object_list[nback_trial_count-level]): 
          target_repeat = 1
        else:
          target_repeat = 0
        
        if nback_trial_count == 0:
          lure_repeat = 0
        if (block_cat == 'object') & (curr_face_list[nback_trial_count] == curr_face_list[nback_trial_count-level]):
          lure_repeat = 1
        elif (block_cat == 'face') & (curr_object_list[nback_trial_count] == curr_object_list[nback_trial_count-level]):  
          lure_repeat = 1
        else:
          lure_repeat = 0
        
        #calculates if response was correct
        if nback_trial_count == 0:
            if key_resp_nback.keys != None:
                response_corr = 0
            else:
                response_corr = 1
            
        if (nback_trial_count == 1) & (level == 2):
          if key_resp_nback.keys != None:
                response_corr = 0
          else:
                response_corr = 1
            
        
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
           
            
            
        #adds other variables to dataframe
        nback_loop.addData('nback_level', level)
        nback_loop.addData('target_cat', block_cat)
        nback_loop.addData('face_img', show_face)
        nback_loop.addData('object_img', show_object)
        nback_loop.addData('response_corr', response_corr)
        nback_loop.addData('trial_num', nback_trial_count)
        nback_loop.addData('target_repeat', target_repeat)
        nback_loop.addData('lure_repeat', lure_repeat)
        
        #updates trial counts
        nback_trial_count = nback_trial_count + 1 
        
        # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'nback_loop'


# set up handler to look after randomisation of conditions etc
prac_inst_trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('testtrialorderinst.xlsx', selection='21:26'),
    seed=None, name='prac_inst_trials')
thisExp.addLoop(prac_inst_trials)  # add the loop to the experiment
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

    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'prac_inst_trials'



# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()


