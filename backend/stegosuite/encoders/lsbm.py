from PIL import Image, PngImagePlugin
import numpy as np
import random
import logging

METADATA_TAG_KEY = "ProcessingInfo"
CODEWORD = "apple"

def lsbm_encode_in_memory(input_buffer, secret_msg, output_buffer):
    try:
        img = Image.open(input_buffer).convert("RGB")
        img_array = np.array(img, dtype=np.uint8)
    except Exception as e:
        logging.error(f"LSBM Encode Error: {e}")
        return None
        
    binary_msg = ''.join([format(ord(c), '08b') for c in secret_msg])
    binary_msg += '1111111111111110'
    
    h, w, channels = img_array.shape
    total_pixels = h * w * channels
    
    if len(binary_msg) > total_pixels:
        raise ValueError(f"Message too large for LSB-M encoding. Max bits: {total_pixels}, Required: {len(binary_msg)}")
        
    flat = img_array.copy().flatten()
    
    for i in range(len(binary_msg)):
        target_bit = int(binary_msg[i])
        pixel_val = int(flat[i])
        
        if (pixel_val & 1) != target_bit:
            adjustments = []
            
            if pixel_val > 0:
                adjustments.append(-1)
            if pixel_val < 255:
                adjustments.append(1)
                
            if not adjustments:
                if pixel_val == 0:
                    adjustment = 1
                elif pixel_val == 255:
                    adjustment = -1
                else:
                    continue
            else:
                adjustment = random.choice(adjustments)
                
            new_val = pixel_val + adjustment
            new_val = max(0, min(255, new_val))
            flat[i] = np.uint8(new_val)
            
    stego_array = np.uint8(flat.reshape(img_array.shape))
    stego_image = Image.fromarray(stego_array)
    
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(METADATA_TAG_KEY, CODEWORD)
    
    stego_image.save(output_buffer, format='PNG', pnginfo=metadata)
    output_buffer.seek(0)
