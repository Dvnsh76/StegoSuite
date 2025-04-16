import cv2
import numpy as np
from PIL import Image
import logging

def erde_decode_in_memory(input_buffer):
    logging.debug(f"ERDE Decode: Starting for input buffer")
    try:
        img = Image.open(input_buffer).convert('RGB')
        pixels = np.array(img)
        r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
        
        edges = cv2.Canny(g.astype(np.uint8), 90, 180)
        
        edge_coords = []
        for y in range(edges.shape[0]):
            for x in range(edges.shape[1]):
                if edges[y, x] > 0:
                    edge_coords.append((y, x))
                    
        binary_str = ''.join(str(b[y, x] & 1) for (y, x) in edge_coords)
        
        try:
            length = int(binary_str[:32], 2)
            msg_bits = binary_str[32:32+length*8]
            return bytes(int(msg_bits[i:i+8], 2) for i in range(0, len(msg_bits), 8)).decode('utf-8')
        except Exception as e:
            logging.error(f"ERDE Decode Error: Failed to extract message: {e}")
            return ""
    except Exception as e:
        logging.error(f"ERDE Decode Error: {e}")
        return None
