# XDCAM BiM Parser

A Python module which reads XDCAM EX BiM files and extracts data like iris, focus, zoom, white-balance etc.

Note that the XDCAM EX BiM file is an MPEG-7 meta-data file which should properly be decoded using the XML specification used by Sony.  Since this specification is not or may not be publicly available, the module reads the BiM file directly and interprets the values therein.  The results are very close to what the XDCAM Clip Browser's Acquisition Tab lists, albeit not as complete.

## Requirements
* python

## How to Use
`import bim_file_tools as bft\nbft.process_bim_data(filepath, clip_browser=False)`

Use `clip_browser=True` to format data as the XDCAM Clip Browser would.

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
