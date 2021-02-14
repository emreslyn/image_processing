import numpy as np
import os, cv2
import moviepy.editor as mpy

main_dir = 'cat\\cat_'

################################################################################## Part4 starts here.
matched_image_list = []  # flashed video frames
for i in range(180):
    image = cv2.imread(main_dir + str(i) + '.png')
    image_r = cv2.flip(image, 1)
    new_frame_r = background.copy()
    image_g_channel = image_r[:, :, 1]  # green channel
    image_r_channel = image_r[:, :, 0]  # red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image_r[nonzero_x, nonzero_y, :]
    outputImage = np.zeros(np.shape(nonzero_cat_values))
    for j in range(2):  # maps cdf of input to cdf of target image for each channel for cat on right
        PI = get_PI(nonzero_cat_values, j)
        PJ = get_PJ(target_image, j)
        noise = np.random.normal(0, 0.2 ** 0.5, PJ.shape)
        noise = noise.reshape(PJ.shape)
        PJ = PJ + noise
        LUT = get_LUT(PI, PJ)
        outputImage[:, j] = LUT[nonzero_cat_values[:, j]]

    width_diff = background.shape[1] - image_r.shape[1]
    new_frame_r[nonzero_x, (nonzero_y + width_diff), :] = outputImage

    image_g_channel = image[:, :, 1]  # green channel
    image_r_channel = image[:, :, 0]  # red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image[nonzero_x, nonzero_y, :]
    outputImage = np.zeros(np.shape(nonzero_cat_values))
    for k in range(2):  # maps cdf of input to cdf of target image for each channel for cat on left
        PI = get_PI(nonzero_cat_values, k)
        noise = np.random.normal(0, 0.1 ** 0.5, PI.shape)
        noise = noise.reshape(PI.shape)
        PJ = PI + noise
        LUT = get_LUT(PI, PJ)
        outputImage[:, k] = LUT[nonzero_cat_values[:, k]]
    new_frame_r[nonzero_x, nonzero_y, :] = outputImage

    new_frame_r = new_frame_r[:, :, [2, 1, 0]]
    matched_image_list.append(new_frame_r)
################################################################################## PART 4-video creation
clip = mpy.ImageSequenceClip(matched_image_list, fps=25)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('part4_video.mp4', codec='libx264')
################################################################################## Part4 ends here.