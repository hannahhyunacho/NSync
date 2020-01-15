#created in psychopy 3.0.0b12
# updated in psychopy 3.2.4

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
import csv # to read and write in csv files/logs
from psychopy.hardware import keyboard


#### ------------ EYETRACKING ------------ ####
# import libraries
import os, random, numpy, pylink
from psychopy import visual, core, event, monitors

# import custom calibration/validation routine for psychopy
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

dummyMode = True # Simulated connection to the tracker
# press ESCAPE twice to skip calibration/validataion
# True means that you're not connected to the eyetracker and have to create a simulated (dummy) connection

####------------TASK PARAMETERS------------ ####

#------------ NBACK PARAMETERS ------------ #
nback_ISI = 0.75 #in seconds 0.5; (0.75)
nback_image_dur = 1.5 #image exposure duration (1.5)
nback_trial_dur = nback_image_dur + nback_ISI  #in seconds 
nback_trial_num_all = 250 # number of nback trials overall
nback_block_num = 2 # number of blocks for n-back
nback_trial_num = int(nback_trial_num_all / nback_block_num) # number of nback trials per block
nback_p_targets = 0.16 # percentage of targets you want
total_targets = int(nback_trial_num_all*nback_p_targets) #80
targets_per_block =  total_targets/nback_block_num #20
nback_unique_images = int(nback_trial_num_all) - total_targets

#------------ MEMORY TEST PARAMETERS ------------ #
old_image_num = nback_unique_images  #number of old images that weren't repeated (per category?)
new_image_num = 84 #number of lures PER CATEGORY
mem_trial_num = old_image_num + new_image_num #number of memory trials (per category?)
mem_ISI = 0.5 # in seconds
mem_trial_dur = 30 # in seconds

#------------ GLOBAL PARAMETERS ------------ #
total_cat_image_num = old_image_num + new_image_num #number of unique images for things for the whole experiment
# total_face_image_num = nback_unique_images # number of face images needed for the nback phase (since none are needed for memory anymore)

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
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], 'nback_data', expInfo['date'])

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
# Create some handy timers
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 





#### ------------ EYETRACKING ------------ #####

#### SETP II: established a link to the tracker
if not dummyMode: 
    tk = pylink.EyeLink()
else:
    tk = pylink.EyeLink(None)
    
    #### STEP III: Open an EDF data file 
# here we create two folders, one for the spreadsheet type data we collect after each trial,
# one for the EDF data file recorded by Eyelink 
if not os.path.exists('edfData'): os.mkdir('edfData')

# STEP III: Open an EDF data file to save the eye movement data
# This needs to be done early, so as to record all user interactions with the tracker
# File name cannot exceed 8 characters
edfFileName = '%s' %(expInfo['participant'])+'_FM.EDF' 
tk.openDataFile(edfFileName)
tk.sendCommand("add_file_preamble_text 'Psychopy Object_choice'")

# STEP IV: Initialize custom graphics for camera setup & drift correction
scnWidth, scnHeight = (1920, 1080) 

#### STEP IV: Initialize custom graphics for camera setup & drift correction ##################

# initialize a monitor object to inform Psychopy the viewing distance, monitor gamma, etc.
mon = monitors.Monitor('myMon', width=32.0, distance=57.0)
mon.setSizePix((scnWidth, scnHeight))
# for the custom calibration/validation routine to work properly, we recommend setting display units to "pix"
win = visual.Window(size=(scnWidth, scnHeight), fullscr=True,screen=0,
    allowGUI=False, allowStencil=False, monitor=mon,color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='pix')

#win = visual.Window(size=(scnWidth, scnHeight), fullscr=True, monitor=mon, color='black', units='pix', colorSpace='rgb')
# Initialize the graphics for calibration/validation
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)


# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

#### STEP V: Set up the tracker ####

tk.setOfflineMode() # put tracker in offline mode before changing configuration
tk.sendCommand('sample_rate 1000') # sampling rate of 250, 500, 1000, or 2000 (won't work for EyeLink II/I)

# inform the tracker the resolution of the subject display
# [see Eyelink Installation Guide, Section 8.4: Customizing Your PHYSICAL.INI Settings ]
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# save display resolution in EDF data file for Data Viewer integration purposes
# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
tk.sendCommand("calibration_type = HV9") # tk.setCalibrationType('HV9') also works, see the Pylink manual

#specify the proportion of subject display to calibrate/validate (OPTIONAL, useful for wide screen monitors)
tk.sendCommand("calibration_area_proportion 0.85 0.83")
tk.sendCommand("validation_area_proportion  0.85 0.83")

#Using a button from the EyeLink Host PC gamepad to accept calibration/dirft check target (optional)
tk.sendCommand("button_function 1 'accept_target_fixation'")

# the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (100/1000Plus/DUO)
eyelinkVer = tk.getTrackerVersion()

#turn off scenelink camera stuff (EyeLink II/I only)
if eyelinkVer == 2: tk.sendCommand("scene_camera_gazemap = NO")

# Set the tracker to parse Events using "GAZE" (or "HREF") data
tk.sendCommand("recording_parse_type = GAZE")

# Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
# the Parser for EyeLink I is more conservative, see below
# [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
if eyelinkVer>=2: tk.sendCommand('select_parser_configuration 0')
else:
    tk.sendCommand("saccade_velocity_threshold = 35")
    tk.sendCommand("saccade_acceleration_threshold = 9500")

# get Host tracking software version
hostVer = 0
if eyelinkVer == 3:
    tvstr  = tk.getTrackerVersionString()
    vindex = tvstr.find("EYELINK CL")
    hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

# specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
# See Section 4 Data Files of the EyeLink user manual
tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
if hostVer>=4: 
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
    tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
else:          
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
    tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")
    
    # Calibrate the camera
calInstruct = visual.TextStim(win, text='Press ENTER twice to calibrate the tracker', color='white')
calInstruct.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()





#### ------------ SET UP EXPERIMENT ------------ ####

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True   , screen=0,
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


#gets level from calibration_phase by participant id string and reading the last (3rd) value in the list
os.chdir(os.getcwd() + '/data/logs') #set wd to data

with open(expInfo['participant'] + '.csv', 'r') as f:
  reader = csv.reader(f)
  level_log = list(reader)

level = int(level_log[2][0]) #gets set level! (either 1 or 2)

os.chdir(_thisDir) #resets dir back to normal

#adds age to data
expInfo['age'] = int(level_log[1][0])

#### ------ CREATES TRIAL LISTS -------- ####

#creates an array of numbers representing all the images for each category
object_list = list(range(total_cat_image_num))
face_list = list(range(total_cat_image_num))

#shuffles lists
shuffle(object_list)
shuffle(face_list)

#assigns certain images to nback vs lures on the mem test
nback_object_list = object_list[0:nback_unique_images] #objects assigned to nback
mem_lure_object_list = object_list[nback_unique_images:total_cat_image_num] #objects assigned as lures 


nback_face_list = face_list #faces assigned to nback
mem_lure_face_list = face_list[nback_unique_images:total_cat_image_num] #faces assigned as lures 

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

#stores faces into blocks
block_1_face = nback_face_list[0:nback_trial_num-target_jitter[0]]
nback_face_list = nback_face_list[len(block_1_face):]

block_2_face = nback_face_list[0:nback_trial_num-target_jitter[1]]
nback_face_list = nback_face_list[len(block_2_face):]

# block_3_face = nback_face_list[0:nback_trial_num-target_jitter[2]]
# nback_face_list = nback_face_list[len(block_3_face):]

# block_4_face = nback_face_list[0:nback_trial_num-target_jitter[3]]


#stores objects into blocks
block_1_object = nback_object_list[0:nback_trial_num-target_jitter[0]]
nback_object_list = nback_object_list[len(block_1_object):]

block_2_object = nback_object_list[0:nback_trial_num-target_jitter[1]]
nback_object_list = nback_object_list[len(block_2_object):]

# block_3_object = nback_object_list[0:nback_trial_num-target_jitter[2]]
# nback_object_list = nback_object_list[len(block_3_object):]

# block_4_object = nback_object_list[0:nback_trial_num-target_jitter[3]]

#Shuffles face list and object list based on level
if level == 1: # if 1 back 
    shuffle_1back(block_1_face,target_jitter[0])
    shuffle_1back(block_2_face,target_jitter[1])
    # shuffle_1back(block_3_face,target_jitter[2])
    # shuffle_1back(block_4_face,target_jitter[3])
    
    nback_order_face = block_1_face + block_2_face # + block_3_face + block_4_face

    shuffle_1back(block_1_object,target_jitter[0])
    shuffle_1back(block_2_object,target_jitter[1])
    # shuffle_1back(block_3_object,target_jitter[2])
    # shuffle_1back(block_4_object,target_jitter[3])

    nback_order_ob = block_1_object + block_2_object # + block_3_object + block_4_object
    

else:# IF 2 BACK THEN this
    shuffle_2back(block_1_face,target_jitter[0])
    shuffle_2back(block_2_face,target_jitter[1])
    # shuffle_2back(block_3_face,target_jitter[2])
    # shuffle_2back(block_4_face,target_jitter[3])
    
    nback_order_face = block_1_face + block_2_face # + block_3_face + block_4_face

    shuffle_2back(block_1_object,target_jitter[0])
    shuffle_2back(block_2_object,target_jitter[1])
    # shuffle_2back(block_3_object,target_jitter[2])
    # shuffle_2back(block_4_object,target_jitter[3])

    nback_order_ob = block_1_object + block_2_object # + block_3_object + block_4_object





#### ------------ MEMORY TEST CREATOR ------------ ####

#makes list of the target faces and lure faces
list_targets_face = []
if level == 1:
    for i in range(len(nback_order_face)):
        if (i > 0) & (nback_order_face[i] == nback_order_face[i-1]):
            list_targets_face.append(nback_order_face[i])
else:
    for i in range(len(nback_order_face)):
        if (i > 1) & (nback_order_face[i] == nback_order_face[i-2]):
            list_targets_face.append(nback_order_face[i])

#does same for objects
list_targets_ob = []
if level == 1:
    for i in range(len(nback_order_ob)):
        if (i > 0) & (nback_order_ob[i] == nback_order_ob[i-1]):
            list_targets_ob.append(nback_order_ob[i])
else:
    for i in range(len(nback_order_ob)):
        if (i > 1) & (nback_order_ob[i] == nback_order_ob[i-2]):
            list_targets_ob.append(nback_order_ob[i])

old_face_list = [x for x in nback_order_face if x not in list_targets_face]
old_object_list = [x for x in nback_order_ob if x not in list_targets_ob]

#rename dataframes for legibility

new_face_list = mem_lure_face_list
new_object_list = mem_lure_object_list

#shuffle
shuffle(old_face_list)
shuffle(old_object_list)

#determines block category order for the nback (F-O-F-O or O-F-0-F)
block_type = int(expInfo['participant'])%2 

if block_type == 1:
   block_order = ['face','object']
   block_str = 'FO'
else:
   block_order = ['object','face']
   block_str = 'OF'
   

#### ------------ MEM TEST TRIAL PREP ------------ ####
# assigns face trial identifiers (image, face/object, old/new, attended)
for i in range(len(old_face_list)): # adds unique identifier to face trials
    for j in range(len(nback_order_face)):
        if old_face_list[i] == nback_order_face[j]:
            if j < nback_trial_num: # get the trials before the number of trials per block
               block_num = 1
            elif (j > nback_trial_num - 1) & (j < nback_trial_num * 2):
               block_num = 2
            elif (j > (nback_trial_num*2) - 1) & (j < nback_trial_num * 3):
                block_num = 3
            else:
                block_num = 4
            #figures out whether the face was attended or not
            if block_str == 'FO': # faces attended first
                if block_num%2 == 0: #if block_num is even, faces are unattended
                    attended = 0
                else:
                    attended = 1
            else: # if 'OF', faces attended second
                if block_num%2 == 0: #if block_num is even, faces are attended
                    attended = 1
                else:
                    attended = 0

            break
        
    #adds attended 
    old_face_list[i] = old_face_list[i],'f','old', attended

# for the new faces
for i in range(len(new_face_list)):
    new_face_list[i] = new_face_list[i] ,'f', 'new','NA'


# same thing for object trial identifiers
for i in range(len(old_object_list)): # adds unique identifier to object trials
    for j in range(len(nback_order_ob)):
        if old_object_list[i] == nback_order_ob[j]:
            if j < nback_trial_num:
               block_num = 1
            elif (j > nback_trial_num - 1) & (j < nback_trial_num * 2):
               block_num = 2
            elif (j > (nback_trial_num * 2) - 1) & (j < nback_trial_num * 3):
                block_num = 3
            else:
                block_num = 4
            #figures out whether the obj was attended or not
            if block_str == 'FO': # objects attended second
                if block_num%2 == 0: #if block_num is even, obj are attended
                    attended = 1
                else:
                    attended = 0
            else: # if 'OF', objects attended first
                if block_num%2 == 0: #if block_num is even, obj are unattended
                    attended = 0
                else:
                    attended = 1

            break
        
    #adds attended 
    old_object_list[i] = old_object_list[i],'o','old', attended
    

for i in range(len(new_object_list)):
    new_object_list[i] = new_object_list[i] ,'o', 'new','NA'
    

#combines and then shuffles all lists into one trial order for memory trials
mem_trial_order = old_face_list + new_face_list + old_object_list + new_object_list 
shuffle(mem_trial_order)

#exports csv of what imgaes to save as NEW for the memory phase !!!! this is super important

os.chdir(os.getcwd() + '/data/logs') #set wd to data
with open(expInfo['participant'] + '_mem_trial_order' + '.csv','w')  as f:
    writer=csv.writer(f, delimiter=",", lineterminator="\n") 
    writer.writerows(mem_trial_order)

os.chdir(_thisDir) # changes back to main directory




##############################################
#### ------INITIALIZE OBJECTS ----------- #####
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

icon = visual.ImageStim(
    win=win, name='icon',
    image='images/face_icon.png', mask=None,
    ori=0, pos=(0,325), size=(850,160),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

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
    ori=0, pos=(0, 0), size=None,
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


# Initialize components for Routine "mem_inst"
mem_instClock = core.Clock()
image = visual.ImageStim(
    win=win, name='image',
    image=None, mask=None,
    ori=0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "mem_trial"
mem_trialClock = core.Clock()
mem_trial_image = visual.ImageStim(
    win=win, name='mem_trial_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
new_button = visual.ImageStim(
    win=win, name='new_button',
    image='images/new_button.png', mask=None,
    ori=0, pos=(-200, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
old_button = visual.ImageStim(
    win=win, name='old_button',
    image='images/old_button.png', mask=None,
    ori=0, pos=(200, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
# Initialize components for Routine "mem_trial_rate"
mem_trial_rateClock = core.Clock()
mem_trial_image_con = visual.ImageStim(
    win=win, name='mem_trial_image_con',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(500,500),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
    
mem_con_scale = visual.ImageStim(
    win=win, name='mem_con_scale',
    image= 'images/mem_rating_scale.png', mask=None,
    ori=0, pos=(0, -350), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "end"
endClock = core.Clock()


##############################################
#### ------------START NBACK ---------- -#####
##############################################

#determines block category order (F-O-F-O or O-F-0-F)



block_type = int(expInfo['participant'])%2 

if block_type == 1:
   block_order = ['face','object']
   block_str = 'FO'
else:
   block_order = ['object','face']
   block_str = 'OF'

for block_count in range(len(block_order)):# FIND_ME
    block_cat = block_order[block_count]
    if block_cat == 'face':   
        target_order = nback_order_face
        lure_order = nback_order_ob
        icon.setImage('images/face_icon.png')
        if level == 1:
            inst_path = 'images/nback_reminders/face_1back/'
        else:
            inst_path = 'images/nback_reminders/face_2back/'
    elif block_cat == 'object': 
        target_order = nback_order_ob
        lure_order = nback_order_face
        icon.setImage('images/thing_icon.png')
        if level == 1:
            inst_path = 'images/nback_reminders/ob_1back/'
        else:
            inst_path = 'images/nback_reminders/ob_2back/'
            
    if block_count == 0: # if first block
        nback_order_face_block = block_1_face
        nback_order_ob_block = block_1_object
    if block_count == 1: # if second block
        nback_order_face_block = block_2_face
        nback_order_ob_block = block_2_object
    if block_count == 2: # if third block
        nback_order_face_block = block_3_face
        nback_order_ob_block = block_3_object
    if block_count == 3: # if fourth block
        nback_order_face_block = block_4_face
        nback_order_ob_block = block_4_object

    ###################
    # insert appropriate instructions loop here ####
    ###################
    
    # Initialize components for Routine "demo_1_t1"
    demo_1_t1Clock = core.Clock()
    image = visual.ImageStim(
        win=win, name='image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)

    # Initialize components for Routine "demo_2_t1"
    demo_2_t1Clock = core.Clock()
    image_2 = visual.ImageStim(
        win=win, name='image_2',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1200,675),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)


    # ------Prepare to start Routine "demo_1_t1"-------
    t = 0
    demo_1_t1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2 = event.BuilderKeyResponse()
    image.setImage(inst_path + '1.jpg')

    # keep track of which components have finished
    demo_1_t1Components = [image, key_resp_2]
    for thisComponent in demo_1_t1Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "demo_1_t1"-------
    while continueRoutine:
        # get current time
        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        t = demo_1_t1Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image* updates
        if t >= 0.0 and image.status == NOT_STARTED:
            # keep track of start time/frame for later
            image.tStart = t
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)
            tk.sendMessage("SYNCTIME_image") # message to mark the onset of visual stimuli

        
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
            theseKeys = event.getKeys(keyList=['space', 'f', 'j'])
            
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
        for thisComponent in demo_1_t1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "demo_1_t1"-------
    for thisComponent in demo_1_t1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys=None

    if key_resp_2.keys != None:  # we had a response
        thisExp.nextEntry()
    # the Routine "demo_1_t1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # send a message to mark the end of trial
    tk.sendMessage('TRIAL_RESULTS')

    # ------Prepare to start Routine "demo_2_t1"-------
    t = 0
    demo_2_t1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse()
    image_2.setImage(inst_path + '2.jpg')
    # keep track of which components have finished
    demo_2_t1Components = [image_2, key_resp_3]
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "demo_2_t1"-------
    while continueRoutine:
        # get current time
        t = demo_2_t1Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image_2* updates
        if t >= 0.0 and image_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_2.tStart = t
            image_2.frameNStart = frameN  # exact frame index
            image_2.setAutoDraw(True)
            tk.sendMessage("SYNCTIME_image") # message to mark the onset of visual stimuli

        
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
            theseKeys = event.getKeys(keyList=['space', 'f','j'])
            
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
        for thisComponent in demo_2_t1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "demo_2_t1"-------
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys=None

    if key_resp_3.keys != None:  # we had a response

        thisExp.nextEntry()
    # the Routine "demo_2_t1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    

    # ------Prepare to start Routine "demo_2_t1"-------
    t = 0
    demo_2_t1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse()
    image_2.setImage(inst_path + '3.jpg')
    # keep track of which components have finished
    demo_2_t1Components = [image_2, key_resp_3]
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "demo_2_t1"-------
    while continueRoutine:
        # get current time
        t = demo_2_t1Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image_2* updates
        if t >= 0.0 and image_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_2.tStart = t
            image_2.frameNStart = frameN  # exact frame index
            image_2.setAutoDraw(True)
            tk.sendMessage("SYNCTIME_image") # message to mark the onset of visual stimuli

        
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
            theseKeys = event.getKeys(keyList=['space','f','j'])
            
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
        for thisComponent in demo_2_t1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "demo_2_t1"-------
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys=None

    if key_resp_3.keys != None:  # we had a response

        thisExp.nextEntry()
    # the Routine "demo_2_t1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "demo_2_t1"-------
    t = 0
    demo_2_t1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse()
    image_2.setImage(inst_path + '4.jpg')
    # keep track of which components have finished
    demo_2_t1Components = [image_2, key_resp_3]
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "demo_2_t1"-------
    while continueRoutine:
        # get current time
        t = demo_2_t1Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image_2* updates
        if t >= 0.0 and image_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_2.tStart = t
            image_2.frameNStart = frameN  # exact frame index
            image_2.setAutoDraw(True)
            tk.sendMessage("SYNCTIME_image") # message to mark the onset of visual stimuli

        
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
            theseKeys = event.getKeys(keyList=['space','f','j'])
            
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
        for thisComponent in demo_2_t1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "demo_2_t1"-------
    for thisComponent in demo_2_t1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys=None

    if key_resp_3.keys != None:  # we had a response

        thisExp.nextEntry()
    # the Routine "demo_2_t1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    






    #rsets trial count
    nback_trial_count = 0
    
    total_trial_count = 0
    if block_count == 1:
        total_trial_count = nback_trial_num
    elif block_count == 2:
        total_trial_count = nback_trial_num * 2
    elif block_count == 3:
        total_trial_count = nback_trial_num * 3



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

        
        show_face = nback_order_face_block[nback_trial_count] # what face image to show
        show_object = nback_order_ob_block[nback_trial_count] #what ob image to sho
        # ------Prepare to start Routine "nback_trial"-------
        t = 0
        nback_trialClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        object_image.setImage('object_images/' + str(show_object) + '.png')
        face_image.setImage('face_images/' + str(show_face) + '.jpg')
        key_resp_nback = event.BuilderKeyResponse()
        
        # keep track of which components have finished
        nback_trialComponents = [icon, polygon, face_image, object_image, key_resp_nback,text]
        for thisComponent in nback_trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "nback_trial"-------
        while continueRoutine:
            # get current time
            time_elapsed = globalClock.getTime()
            time_elapsed_M = core.monotonicClock.getTime()
            t = nback_trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *icon* updates
            if t >= 0.0 and icon.status == NOT_STARTED:
                # keep track of start time/frame for later
                icon.tStart = t
                icon.frameNStart = frameN  # exact frame index
                icon.setAutoDraw(True)
                tk.sendMessage("SYNCTIME_image") # message to mark the onset of visual stimuli

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
        if nback_trial_count == 0:
          target_repeat  = 0
        
        if (block_cat == 'face') & (nback_order_face_block[nback_trial_count] == nback_order_face_block[nback_trial_count-level]):
          target_repeat = 1
        elif (block_cat == 'object') & (nback_order_ob_block[nback_trial_count] == nback_order_ob_block[nback_trial_count-level]): 
          target_repeat = 1
        else:
          target_repeat = 0
        
        if nback_trial_count == 0:
          lure_repeat = 0
        if (block_cat == 'object') & (nback_order_face_block[nback_trial_count] == nback_order_face_block[nback_trial_count-level]):
          lure_repeat = 1
        elif (block_cat == 'face') & (nback_order_ob_block[nback_trial_count] == nback_order_ob_block[nback_trial_count-level]): 
          lure_repeat = 1
        else:
          lure_repeat = 0
        
        #calculates if response was correct
        if target_repeat == 1: # if the target repeated
            if key_resp_nback.keys == 'j':
                response_corr = 1 # correctly identified as repeated
            else:
                response_corr = 0
        elif target_repeat == 0: # if the target was not repeated
            if key_resp_nback.keys == 'f':
                response_corr = 1 # correctly identified as not repeated
            else:
                response_corr = 0

        #adds other variables to dataframe
        nback_loop.addData('nback_level', level)
        nback_loop.addData('target_cat', block_cat)
        nback_loop.addData('face_img', show_face)
        nback_loop.addData('object_img', show_object)
        nback_loop.addData('response_corr', response_corr)
        nback_loop.addData('trial_num', total_trial_count+1)
        nback_loop.addData('block_trial_num', nback_trial_count+1)
        nback_loop.addData('block_num', block_count+1)
        nback_loop.addData('target_repeat', target_repeat)
        nback_loop.addData('lure_repeat', lure_repeat)
        nback_loop.addData('block_order', block_str)
        nback_loop.addData('first_screen_time_elapsed', time_elapsed)
        nback_loop.addData('total_time_elapsed', time_elapsed_M)
        #updates trial counts
        nback_trial_count = nback_trial_count + 1 
        total_trial_count = total_trial_count + 1
        
        # the Routine "nback_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'nback_loop'



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
#close EDF data File
tk.closeDataFile()

#EyeLink - copy EDF file to Display PC and put it in the 'edfData' folder
edfTransfer = visual.TextStim(win, text='Gaze data is transfering from EyeLink Host PC, please wait...', color='white')
edfTransfer.draw()
win.flip()
tk.receiveDataFile(edfFileName, os.getcwd() + os.sep + 'edfData' + os.sep + edfFileName)

#EyeLink - Close connection to tracker
tk.close()
# thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()



