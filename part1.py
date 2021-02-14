import numpy as np
import os, cv2
import moviepy.editor as mpy

main_dir = 'cat\\cat_'
image_list = []
background = cv2.imread('Malibu.jpg')
##################################################################################Part1 starts here.
background_height = background.shape[0]
background_width = background.shape[1]
ratio = 360/background_height
background = cv2.resize(background, (int(background_width*ratio),360))

for i in range(180):
    image = cv2.imread(main_dir + str(i) + '.png')
    image_g_channel = image[:,:,1] #green channel
    image_r_channel = image[:,:,0] #red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image[nonzero_x, nonzero_y,:]
    new_frame = background.copy()
    new_frame[nonzero_x, nonzero_y,:] = nonzero_cat_values
    image_list.append(new_frame)
################################################################################## PART 1-video creation
clip = mpy.ImageSequenceClip(image_list, fps = 25)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip = audio)
clip.write_videofile('part1_video.mp4', codec = 'libx264')
##################################################################################Part1 ends here.