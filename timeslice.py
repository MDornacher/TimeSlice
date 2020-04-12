import argparse
import glob
import os

from PIL import Image

# set parameters
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images_path', help='Path to images', required=True)
ap.add_argument('-x', '--images_ext', help='Extension of images', required=True)
ap.add_argument('--start_image', help='nth image to start with', type=int)
ap.add_argument('--final_image', help='nth image to end with', type=int)
ap.add_argument('--animation', help='Create animation of frames as webm with ffmpeg', action='store_true')
ap.add_argument('-fps', help='Framerate for animation', type=int, default=10)
args = vars(ap.parse_args())

images_path = os.path.normpath(args['images_path'])
if not os.path.isdir(images_path):
    raise ValueError(f'Path {images_path} is not a directory.')
images_ext = args['images_ext']

# creates file name list
img_list = sorted(glob.glob(os.path.join(images_path, f'*.{images_ext}')))
if not img_list:
    raise ValueError(f'No {images_ext} images in {images_path} found.')

# number of source photos
number_of_photos = len(img_list)
print(f'{number_of_photos} images found')

# determine image size
with Image.open(img_list[0]) as ref_img:
    frame_resolution_x = ref_img.width
    frame_resolution_y = ref_img.height

# calculates the width of each slice
slice_width = frame_resolution_x // number_of_photos

# creates empty frame
for i in range(number_of_photos):
    frame = Image.new('RGB', (number_of_photos * slice_width, frame_resolution_y))
    frame.save(f'frame_{i+1:03}.tif')
    frame.close()

start_image = args['start_image'] if args['start_image'] else 0
final_image = args['final_image'] if args['final_image'] else number_of_photos
for k in range(start_image, final_image):
    print(f'Slicing image {k+1} of {number_of_photos}')
    img = Image.open(img_list[k])
    for i in range(number_of_photos):
        slice_x_start = i * slice_width
        slice_x_end = (i+1) * slice_width
        slice_box = (slice_x_start, 0, slice_x_end, frame_resolution_y)
        img_slice = img.crop(slice_box)

        frame_number = (k - i) % number_of_photos  # time evolution from left to right
        frame_name = f'frame_{frame_number+1:03}.tif'
        with Image.open(frame_name) as frame:
            frame.paste(img_slice, (slice_x_start, 0))
            frame.save(f'frame_{i + 1:03}.tif')
    img.close()

# creates animation with ffmpeg
if args['animation']:
    print('Creating webm...')
    os.system(f'ffmpeg -f image2 -framerate {args["fps"]} -pattern_type sequence -start_number 001 -i frame%03d.tif timeslice.webm')
