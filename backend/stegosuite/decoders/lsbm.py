from PIL import Image
import numpy as np
import logging

def lsbm_decode_in_memory(input_buffer):
    logging.debug(f"LSBM Decode: Starting for input buffer")
    try:
        img = Image.open(input_buffer)
        binary_str = ''.join(str(pixel & 1) for pixel in np.array(img).flatten())
        
        delimiter = '1111111111111110'
        delimiter_pos = binary_str.find(delimiter)
        
        if delimiter_pos == -1:
            logging.warning("LSBM Decode: Delimiter not found in extracted bitstream")
            return None
            
        msg_bin = binary_str[:delimiter_pos]
        
        try:
            message = ''.join(chr(int(msg_bin[i:i+8], 2)) 
                            for i in range(0, len(msg_bin), 8))
            return message
        except Exception as e:
            logging.error(f"LSBM Decode Error: Failed to convert binary to text: {e}")
            return ""
    except Exception as e:
        logging.error(f"LSBM Decode Error: {e}")
        return None
