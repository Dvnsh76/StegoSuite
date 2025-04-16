import numpy as np
from PIL import Image, PngImagePlugin
import cv2
import logging

METADATA_TAG_KEY = "ProcessingInfo"
CODEWORD = "banana"

def dct_encode_in_memory(input_buffer, secret_msg, output_buffer):
    quality = 50
    binary_msg = ''.join([format(ord(c), '08b') for c in secret_msg])
    binary_msg += '1111111111111110'
    
    img_pil = Image.open(input_buffer)
    img = np.array(img_pil.convert('YCbCr'))
    img_pil.close()
    
    h, w = img.shape[:2]
    
    coeffs_to_use = [(3,3), (2,3), (3,2)]
    num_coeffs_per_block = len(coeffs_to_use)
    
    full_blocks_h = h // 8
    full_blocks_w = w // 8
    dct_blocks = full_blocks_h * full_blocks_w
    dct_bits = dct_blocks * num_coeffs_per_block
    
    if len(binary_msg) > dct_bits:
        raise ValueError(f"Message too large for DCT encoding. Max: {dct_bits // 8} bytes.")
    
    img_float = img.astype(np.float32)
    msg_index = 0
    encoding_complete = False
    
    for y in range(0, h - 7, 8):
        if encoding_complete:
            break
        for x in range(0, w - 7, 8):
            if encoding_complete:
                break
                
            block = img_float[y:y+8, x:x+8, 0] - 128.0
            try:
                dct_block = cv2.dct(block)
            except cv2.error:
                continue
                
            for i, j in coeffs_to_use:
                if msg_index >= len(binary_msg):
                    encoding_complete = True
                    break
                    
                try:
                    if i >= 8 or j >= 8:
                        continue
                        
                    coeff = dct_block[i, j]
                    target_bit = int(binary_msg[msg_index])
                    
                    quantized = round(coeff / quality)
                    
                    if (quantized % 2) != target_bit:
                        adjustment = -1 if quantized > 0 else 1
                        if quantized + adjustment == 0 and target_bit == 1:
                            adjustment = adjustment * -1
                        quantized += adjustment
                        if quantized == 0 and target_bit == 1:
                            quantized = 1
                            
                    dct_block[i, j] = float(quantized * quality)
                    msg_index += 1
                    
                except IndexError:
                    continue
                except Exception:
                    continue
                    
            try:
                idct_block = cv2.idct(dct_block) + 128.0
                idct_block = np.clip(idct_block, 0, 255)
                img_float[y:y+8, x:x+8, 0] = idct_block
            except Exception:
                continue
                
    stego_y = np.clip(img_float[:, :, 0], 0, 255).astype(np.uint8)
    stego_cb = img[:, :, 1]
    stego_cr = img[:, :, 2]
    stego_img_array_ycbcr = np.stack((stego_y, stego_cb, stego_cr), axis=-1)
    
    try:
        stego_pil_img = Image.fromarray(stego_img_array_ycbcr, 'YCbCr').convert('RGB')
    except Exception as e:
        logging.error(f"DCT Encode Error: {e}")
        return None
        
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(METADATA_TAG_KEY, CODEWORD)
    
    stego_pil_img.save(output_buffer, format='PNG', pnginfo=metadata)
    output_buffer.seek(0)
