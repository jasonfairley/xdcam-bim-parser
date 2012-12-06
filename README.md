# XDCAM BiM Parser

A Python module which reads XDCAM EX BiM files and extracts EX1 data like iris, focus, zoom, white-balance etc.

Note that the XDCAM EX BiM file is an MPEG-7 meta-data file which should properly be decoded using the proper XML specification used by Sony.  Since this specification may not be publicly available, the module reads the BiM file directly and interprets the values therein.  The results are very close to what the XDCAM Clip Browser's Acquisition Tab lists, albeit not as complete.

## Requirements
* python

## How to Use
`import bim_file_tools as bft`

`clip_data = bft.process_bim_data(filepath, clip_browser=True, focal_multiplied=True)`

The resulting `clip_data` is a dictionary of frame numbers each with their own dictionary of key/value pairs for the camera data related to that frame.  Use `clip_browser=True` to format camera data as the XDCAM Clip Browser would, `focal_multiplied=False` to use unmultiply focal lengths and use true focal length instead (i.e. with no applied crop factor).

Further options and wider usage will require looking 'under the hood' as the module was designed to work with XDCAM EX BiM files coming from an EX1 camera.

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
