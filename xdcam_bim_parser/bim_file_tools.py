import struct
from math import pow

# From Sony's EX1R spec: "f = 5.8mm to 81.2mm (equivalent to 31.4mm to 439mm on 35mm lens)"
# 35mm             36.0mm width / 24.0mm height / 43.27mm diagonal / 1.5 aspect ratio
# 1/2-inch 16:9    6.97mm width / 3.92mm height / 8mm diagonal / 1.78 aspect ratio
# Therefore 43.27 / 8 = 5.408 is our crop factor (but note different aspect ratios).
# Source: Sony Guide to Sensor Sizes v1.0


def read_bytes_from_file(filepath, chunk=1024):
    with open(filepath, "rb") as f:
        bytes_read = f.read(chunk)
        while bytes_read:
            yield bytes_read
            bytes_read = f.read(chunk)


def process_bim_data(filepath, clip_browser=True, focal_multiplied=True, 
                     crop_factor=5.41, hoz_film_ap=6.79, ver_film_ap=3.92):
    bim_data = {'hoz_film_ap':hoz_film_ap, 'ver_film_ap':ver_film_ap}
    counter = 1
    header_block = 64
    for bytes_read in read_bytes_from_file(filepath, 1024):
        # skip the first 64 chunks of 1024 bytes
        if counter > header_block:
            frame_dict = {}
            
            # frame number
            frame_dict['frame'] = int(struct.unpack('>i', bytes_read[5:9])[0] / 16.0)
            
            # auto iris
            auto_iris = {03:False, 04:True}
            if clip_browser:
                auto_iris = {03:'Manual', 04:'Auto'}
            frame_dict['auto_iris'] = auto_iris[struct.unpack('b', bytes_read[92])[0]]
            
            # iris
            iris_data = struct.unpack('>H', bytes_read[95:97])[0]
            iris_min, iris_max = 24576, 65535
            stop_min, stop_max = 0, 9
            sqrt_2 = 1.4142135624
            stop_number = (stop_max - stop_min + 1.0) * (iris_max - iris_data) / (iris_max - iris_min)
            frame_dict['iris'] = pow(sqrt_2, stop_number)
            if clip_browser:
                frame_dict['iris'] = 'F%.1f'%frame_dict['iris']
            
            # focus
            focus_data = struct.unpack('>H', bytes_read[98:100])[0]
            focus_4_4m = 25012
            focus_50m = 28881
            focus_100m = 29618
            focus_1000m = 33768
            if focus_data < (focus_4_4m + 1):
                focus_data = 0.001 * focus_data - 20.5
            elif focus_data < (focus_50m + 1):
                focus_data = 0.01 * focus_data - 245.8
            elif focus_data < (focus_100m + 1):
                focus_data = 0.1 * focus_data - 2867.2
            elif focus_data < (focus_1000m + 1):
                focus_data = 1 * focus_data - 32768
            else:
                focus_data = None
            frame_dict['focus'] = focus_data
            if clip_browser:
                frame_dict['focus'] = 'Infinity'
                if not focus_data is None:
                    frame_dict['focus'] = '%.1fm'%focus_data
            
            # macro
            macro_dict = {00:False, 01:True}
            if clip_browser:
                macro_dict = {00:'OFF', 01:'ON'}
            frame_dict['macro'] = macro_dict[struct.unpack('b', bytes_read[101])[0]]
            
            # zoom
            zoom_data = struct.unpack('>h', bytes_read[103:105])[0]
            zoom_40mm = 16252
            zoom_409mm = 20473
            if zoom_data < (zoom_40mm + 1):
                zoom_data = 0.01 * zoom_data - 122.7
            elif zoom_data < (zoom_409mm + 1):
                zoom_data = 0.1 * zoom_data - 1638.3
            else:
                zoom_data = 1 * zoom_data - (4096 * 5)
            frame_dict['zoom'] = zoom_data
            if not focal_multiplied:
                frame_dict['zoom'] = frame_dict['zoom'] / crop_factor
            if clip_browser:
                frame_dict['zoom'] = '%.0fmm'%frame_dict['zoom']
            
            # ND
            frame_dict['nd'] = int(struct.unpack('b', bytes_read[109])[0])
            if clip_browser:
                frame_dict['nd'] = 'ND%d'%frame_dict['nd']
    
            # white balance
            frame_dict['white_balance'] = int(struct.unpack('>h', bytes_read[120:122])[0])
            if clip_browser:
                frame_dict['white_balance'] = '%iK'%frame_dict['white_balance']
            
            # shutter
            frame_dict['shutter'] = float(struct.unpack('>h', bytes_read[113:115])[0]/2)
            if clip_browser:
                frame_dict['shutter'] = '%.0fdeg'%frame_dict['shutter']
    
            # gain
            frame_dict['gain'] = int(struct.unpack('>h', bytes_read[115:117])[0] - 128)
            if clip_browser:
                frame_dict['gain'] = '%ddB'%frame_dict['gain']
            
            bim_data[counter - header_block] = frame_dict
        counter += 1

    return bim_data
