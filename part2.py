import numpy as np
import os, cv2
import moviepy.editor as mpy

main_dir = 'cat\\cat_'

##################################################################################Part2 starts here.
reflected_image_list = []  # two cats on the background image
for i in range(180):
    image = cv2.imread(main_dir + str(i) + '.png')
    image_r = cv2.flip(image, 1)
    image_g_channel = image_r[:, :, 1]  # green channel
    image_r_channel = image_r[:, :, 0]  # red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image_r[nonzero_x, nonzero_y, :]
    width_diff = background.shape[1] - image_r.shape[1]
    new_frame_r = image_list[i].copy()
    new_frame_r[nonzero_x, (nonzero_y + width_diff), :] = nonzero_cat_values
    reflected_image_list.append(new_frame_r)

################################################################################## PART 2-video creation
clip = mpy.ImageSequenceClip(reflected_image_list, fps=25)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('part2_video.mp4', codec='libx264')
################################################################################## Part2 ends here.