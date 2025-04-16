import cv2
import numpy as np
from PIL import Image, PngImagePlugin
import logging

METADATA_TAG_KEY = "ProcessingInfo"
CODEWORD = "grape"

def erde_encode_in_memory(input_buffer, secret_msg, output_buffer):
    try:
        img = Image.open(input_buffer).convert('RGB')
        pixels = np.array(img)
    except Exception as e:
        logging.error(f"ERDE Encode Error: {e}")
        return None
        
    r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
    
    edges = cv2.Canny(g.astype(np.uint8), 90, 180)
    
    try:
        msg_bytes = secret_msg.encode('utf-8')
    except UnicodeEncodeError:
        return None
        
    msg_len_bytes = len(msg_bytes)
    binary_str = f"{msg_len_bytes:032b}" + ''.join(f"{byte:08b}" for byte in msg_bytes)
    total_bits_to_embed = len(binary_str)
    
    edge_coords = []
    for y in range(edges.shape[0]):
        for x in range(edges.shape[1]):
            if edges[y, x] > 0:
                edge_coords.append((y, x))
                
    available_edge_pixels = len(edge_coords)
    if total_bits_to_embed > available_edge_pixels:
        raise ValueError(f"Message too large for ERDE. Requires {total_bits_to_embed} edge pixels, but only found {available_edge_pixels}.")
        
    b_modified = b.copy()
    
    for i in range(total_bits_to_embed):
        y, x = edge_coords[i]
        bit_to_embed = int(binary_str[i])
        current_blue_val = b_modified[y, x]
        
        new_blue_val = (current_blue_val & 0xFE) | bit_to_embed
        b_modified[y, x] = new_blue_val
        
    stego_array = np.stack((r, g, b_modified), axis=2)
    stego_image = Image.fromarray(stego_array)
    
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(METADATA_TAG_KEY, CODEWORD)
    
    stego_image.save(output_buffer, format='PNG', pnginfo=metadata)
    output_buffer.seek(0)
