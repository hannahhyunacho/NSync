## About NSync
TBA

## Getting Started
### Prerequisites
In order to run the experiment, please make sure that you have:
- downloaded this repo
- psychopy3 installed (any psychopy3 version has worked so far)

## How to run Nsync
1. Open up psychopy (coder)
2. Drag the scripts into the window (1Calibration_Eyetracker.py, 3Nback_Eyetracking.py, and 4M_Phase.py)
3. Run each section in order.
4. For the Nback phase, if you ARE NOT connected to an eyetracker, make sure to change so that `dummyMode = True` Press [ESCAPE] twice to skip the eyetracker calibration.

Note: The test participant ID for this experiment is 33. Use this if you want to test something out but don't want to run through the whole experiment.

## The parts of NSync
### Calibration
This section takes approximately 10-15 minutes. The participant will be introduced to the n-back task on images consisting of an animal and face overlaid on top of each other. The participant will play:
- 1-back on animal images
- 1-back on face images
- 2-back on animal images
- 2-back on face images

NOTE: the face images for this section is stored under the folders with "scene" in their names. This is a byproduct of the way this project was initially designed, and can easily be patched out.

This calls the files and folders:
- animal_images, scene_images, practice_animals, practice_faces (for the images themselves)
- in ./images, animal_1back, animal_2back, scene_1back, scene_2back (for instruction slides)
- testtrialorderinst.xlsx (for the order of images to present, which is hard-coded)

This creates the files:
- ./data/logs/[particiapant id].csv (stores the participant's id, age, and n-back level)
- ./data/[participant id]_calibration_phase_[date].csv (the actual responses from the participant)

The goal of this section is to introduce the n-back instructions to the participants (some of which are very young children), as well as calibrate the actual n-back task to their performance. This is because attentional filtering abilities and working memory capacity are suggested to be related, and attentional filtering has been shown to increase across development. Therefore, we wanted to ensure that those with higher working memory capacity wouldn't (potentially) be scoring higher simply because the working memory task (n-back) wasn't challenging enough for them.

### Instructions
This section takes approximately 5 minutes, and has been excluded from the eyetracking version. This was introduced for the MEG version of NSync, where participants would be instructed on the specific task they would be playing inside of the scanner. This involves the n-back level (1-back or 2-back) and the new classes of images (faces, objects). 

We use faces for both the calibration and the n-back because participants showed difficulty with face images for this experiment, and we wanted the calibration to reflect the participants' performance on the actual task as accurately as possible.

This calls the files and folders:
- practice_faces, practice_objects (for the images themselves)
- in ./images, face_inst, thing_inst (for the instruction slides)

This creates the file:
- ./data/[participant id]_instrutions_[date].csv

### N-back
This section is done with the eyetracker, and consists of an n-back phase (calibrated to the participant) using face and object images.

This calls the files and folders:
- face_images, object_images (for the images themselves)
- in ./images/nback_reminders (for the instruction slides)

This creates the files:
- ./data/[participant_id]_nback_data_[date].csv (for the participants' responses)
- ./data/logs/[participant id]_mem_trial_order.csv (for determining the order of images to be shown in the memory phase)
- ./edfData/[participant_id]_FM.EDF (eyetracking data)

### Memory
This section tests the participants for their memory of the face and object images presented during the nback (excluding those that were presented more than once), where participants make an old/new judgement and a confidence judgement.

This calls the files and folders:
- face_images, object_images (for the images themselves)
- ./images/mem_inst (for the instruction slides)

This creates the files:
- ./data/[participant id]_memory_data_[date].csv (participant's responses)

---

## Versions
### Demo
TBA
### Pilot 1
This version of NSync serves as the foundation for the other versions, with the timing for each trial, the length of the study, etc.

### Pilot 2
From the data for pilot 1, we found that the memory for face images was poor, and the memory section was too long (too many trials). As we could not reduce the number of stimuli in the n-back phase, we instead cut out the memory trials for face images. We also changed the calibration to be on animals/faces, to better reflect participant's ability for the n-back task on faces.

Changes:
- calibration now uses animal and face objects instead of animal and place images
- participants are set at a 2-back if accuracy is above 80% rather than 85%
- participants are no longer tested on face memory, halving the number of trials in the memory phase to be 440 trials instead of 880

### MEG
This is largely the same as the Pilot 2 version, but was written to be compatible with PsychoPy2 as the driver for PsychoPy2 was compatible with their MEG.

### Eyetracking
This is our current version, developed off of the Pilot 2 scripts. As we were no longer constrained by the MEG, we could reduce the number of images in the n-back phase so that we can test for the memory for both image classes (rather than omitting the face images like we did in Pilot 2).

Changes:
- eyetracking added to the nback phase script, as well as the file `EyeLinkCoreGraphicsPsychoPy.py` which contains the class required for us to communicate with the eyetracker
- nback now halved to be 250 trials total, with 2 blocks of 125 trials rather than 4 blocks
- participants are now tested on face memory again along with object memory
- memory phase is now pseudorandom in order. half are random, the other half present the face and object shown in one trial back-to-back (half are face-object, the other half is object-face).
