import numpy as np
from PIL import Image
import cv2
import logging

def dct_decode_in_memory(input_buffer):
    quality = 50
    
    try:
        img_pil = Image.open(input_buffer)
        metadata = img_pil.info
        img = np.array(img_pil.convert('YCbCr'))
        img_pil.close()
    except Exception as e:
        logging.error(f"DCT Decode Error: {e}")
        return None
        
    h_orig, w_orig = img.shape[:2]
    h = (h_orig // 8) * 8
    w = (w_orig // 8) * 8
    
    if h == 0 or w == 0:
        return None
        
    img = img[:h, :w]
    
    binary_msg_bits = []
    delimiter = '1111111111111110'
    coeffs_to_use = [(3,3), (2,3), (3,2)]
    
    decoding_complete = False
    for y in range(0, h, 8):
        if decoding_complete:
            break
        for x in range(0, w, 8):
            if decoding_complete:
                break
                
            block = img[y:y+8, x:x+8, 0].astype(np.float32) - 128.0
            try:
                dct_block = cv2.dct(block)
            except cv2.error:
                continue
                
            for i, j in coeffs_to_use:
                if decoding_complete:
                    break
                    
                try:
                    if i >= 8 or j >= 8:
                        continue
                        
                    coeff = dct_block[i, j]
                    quantized = round(coeff / quality)
                    extracted_bit = str(quantized % 2)
                    binary_msg_bits.append(extracted_bit)
                    
                    if len(binary_msg_bits) >= len(delimiter):
                        last_bits = ''.join(binary_msg_bits[-len(delimiter):])
                        if last_bits == delimiter:
                            decoding_complete = True
                            break
                            
                except IndexError:
                    continue
                except Exception:
                    continue
                    
    bit_str = ''.join(binary_msg_bits)
    delimiter_pos = bit_str.find(delimiter)
    
    if delimiter_pos == -1:
        return None
        
    msg_bin = bit_str[:delimiter_pos]
    
    padding = (8 - len(msg_bin) % 8) % 8
    if padding > 0:
        msg_bin += '0' * padding
        
    try:
        byte_array = bytearray()
        for i in range(0, len(msg_bin), 8):
            byte_chunk = msg_bin[i:i+8]
            if len(byte_chunk) < 8:
                continue
            byte_val = int(byte_chunk, 2)
            byte_array.append(byte_val)
            
        decoded_message = byte_array.decode('utf-8', errors='ignore')
        return decoded_message
    except Exception:
        return None
