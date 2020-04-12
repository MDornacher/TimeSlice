# Sliced Time Lapse
Python script to create sliced image sequence for time lapse.

## Requires
- Python
- PIL package
- ffmpeg (optional)

## Usage
`python timeslice.py [-h] -i <images_path> -x <images_ext> [--animation] [-fps <framerate>]`

It is possible to slice images in sections with `--start_image <start_index>` and/or `--final_image <final_index>`  

## Sample:
![](./sample.gif)

## Limitations
- Images need to be stabilized beforehand, because even small tripod bumps will be noticeable. 
All my attempts with `ffmpeg` and `vid.stab` to automatically iron out tiny movements have been unsuccessful so far. 
- The performance for large number of input images with high resolution is pretty bad. 
This is due to `n^2` PIL load/save operations with `n` images.
- The whole sliced time lapse effect works best with big changes in the images - small changes almost disappear.
