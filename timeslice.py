from PIL import Image
import glob
import os

# set parameters
frame_resolution_x = 1648
frame_resolution_y = 1080
loops = 2

# creates file name list
img_list = sorted(glob.glob('source/*.jpg'))  # reverse=True

# number of source photos
number_of_photos = len(img_list)

# calculates the width of each slice
slice_width = int(frame_resolution_x/number_of_photos)

# creates empty frame
frame = Image.new('RGB', (number_of_photos*slice_width, frame_resolution_y))

# creates new list for permutations
img_list_i = img_list[:]
for i in range(number_of_photos * loops):
    print('frame', i+1)
    x_offset = 0
    for filename in img_list_i:
        # print(filename)
        img = Image.open(filename)
        slice_box = (x_offset, 0, x_offset + slice_width, frame_resolution_y)
        img_sliced = img.crop(slice_box)
        # img_sliced.save('output/test_%s.jpg' % filename[-5:-4])
        frame.paste(img_sliced, (x_offset, 0))
        x_offset += slice_width
    img_list_i = [img_list_i[-1]] + img_list_i[:-1]
    frame.save('output/frame_%03d.tif' % (i+1))

# creates animation with ffmpeg
# os.system('ffmpeg -framerate 4 -i output/frame_%03d.jpg -r 30 video.webm')
