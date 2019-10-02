#File renamer
#renames files conseuctively (i.e. 1,2,3,4,5) up to the amount of images in that folder,
#is not recursive so you have to manually set working directory to folder you want to rename
#Marlie

#set working directory to where you want it to rename folders
setwd("~/Desktop/LANDlab/NSYNCH_Pilot/object_images")

#rename

files <- dir()

for (i in 1:length(files)) {
  random_str = as.character(sample(1:10))
  file.rename(files[i], paste(random_str, collapse=''))
  
}

files <- dir()


for (i in 1:length(files)) {
file.rename(files[i], paste(as.character(i), sep = "",'.jpg'))

}


