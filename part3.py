import numpy as np
import os, cv2
import moviepy.editor as mpy

main_dir = 'cat\\cat_'

##################################################################################Part3.1 starts here.
reflected_image_list = []
g = 180 # parameter of darkness
for i in range(180):
    image = cv2.imread(main_dir + str(i) + '.png')
    image_r = cv2.flip(image, 1)
    image_g_channel = image_r[:,:,1] #green channel
    image_r_channel = image_r[:,:,0] #red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image_r[nonzero_x, nonzero_y,:]
    nonzero_cat_values = np.clip(np.float32(nonzero_cat_values) - g,0,255)
    width_diff = background.shape[1]-image_r.shape[1]
    new_frame_r = image_list[i].copy()
    new_frame_r[nonzero_x, (nonzero_y+width_diff),:] = nonzero_cat_values
    reflected_image_list.append(new_frame_r)
################################################################################## PART 3.1-video creation
clip = mpy.ImageSequenceClip(reflected_image_list, fps = 25)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip = audio)
clip.write_videofile('part3_video.mp4', codec = 'libx264')
################################################################################## Part3.1 ends here.

##################################################################################Part3.2 starts here.
def get_LUT(PI,PJ): #returns lookup table
    LUT = np.arange(256)
    for i in range(255):
        if (PI[i] > np.amax(PJ)):
            LUT[i] = 255
        else:
            LUT[i] = np.argmax(np.where( PJ >= PI[i], 1, 0 ))
    return LUT

def get_PI(nonzero_cat_values,channel): #returns cdf of input image
    hist,bins = np.histogram(nonzero_cat_values[:,channel].flatten(),256,[0,256])
    hist = hist / np.prod(np.shape(nonzero_cat_values[:,channel]))
    cdf = hist.cumsum()
    return cdf

def get_PJ(target_image,channel): #returns cdf of target image
    hist = cv2.calcHist([target_image],[channel],None,[256],[0,256])
    hist = hist / np.prod(np.shape(target_image[:,:,channel]))
    cdf = hist.cumsum()
    return cdf

matched_image_list = [] #matched video frames
target_image = cv2.imread('hist_match.jpg') # read target image
for i in range(180):
    image = cv2.imread(main_dir + str(i) + '.png')
    image_r = cv2.flip(image, 1)
    image_g_channel = image_r[:,:,1] #green channel
    image_r_channel = image_r[:,:,0] #red channel
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image_r[nonzero_x, nonzero_y,:]
    outputImage = np.zeros(np.shape(nonzero_cat_values))
    for j in range(2): #maps cdf of input to cdf of target image for each channel
        PI = get_PI(nonzero_cat_values,j)
        PJ = get_PJ(target_image,j)
        LUT = get_LUT(PI,PJ)
        outputImage[:,j] = LUT[nonzero_cat_values[:,j]]

    width_diff = background.shape[1]-image_r.shape[1]
    new_frame_r = image_list[i].copy()
    new_frame_r[nonzero_x, (nonzero_y+width_diff),:] = outputImage
    new_frame_r = new_frame_r[:,:,[2,1,0]]
    matched_image_list.append(new_frame_r)
################################################################################## PART 3.2-video creation
clip = mpy.ImageSequenceClip(matched_image_list, fps = 25)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip = audio)
clip.write_videofile('part3.2_video.mp4', codec = 'libx264')
################################################################################## Part3.2 ends here.