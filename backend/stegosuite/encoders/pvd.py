from PIL import Image, PngImagePlugin
import logging

METADATA_TAG_KEY = "ProcessingInfo"
CODEWORD = "orange"

def get_range(d):
    ranges = [
        (0, 7),
        (8, 15),
        (16, 31),
        (32, 63),
        (64, 127),
        (128, 255)
    ]
    for r in ranges:
        if r[0] <= d <= r[1]:
            return r
    return (0, 7)

def pvd_encode_in_memory(input_buffer, secret_msg, output_buffer):
    try:
        img = Image.open(input_buffer).convert('RGB')
    except Exception as e:
        logging.error(f"PVD Encode Error: {e}")
        return None
        
    pixels = img.load()
    width, height = img.size
    
    msg_bits = []
    for c in secret_msg:
        byte = format(ord(c), '08b')
        parity = '1' if byte.count('1') % 2 else '0'
        msg_bits.append(byte + parity)
    msg_bits = ''.join(msg_bits)
    msg_bits += '000000000'
    
    bit_index = 0
    total_bits = len(msg_bits)
    
    for y in range(height):
        for x in range(0, width - 1, 2):
            if bit_index >= total_bits:
                break
                
            p1 = pixels[x, y][2]
            p2 = pixels[x + 1, y][2]
            d = abs(p2 - p1)
            lower, upper = get_range(d)
            n = min(3, upper.bit_length() - 1)
            
            if n <= 0:
                continue
                
            bits = msg_bits[bit_index:bit_index+n]
            if len(bits) < n:
                bits = bits.ljust(n, '0')
            bit_index += n
            
            new_d = lower + int(bits, 2)
            new_d = min(new_d, upper)
            
            if p2 > p1:
                new_p2 = min(p1 + new_d, 255)
            else:
                new_p2 = max(p1 - new_d, 0)
                
            pixels[x + 1, y] = (pixels[x + 1, y][0], pixels[x + 1, y][1], new_p2)
            
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text(METADATA_TAG_KEY, CODEWORD)
    
    img.save(output_buffer, format='PNG', pnginfo=metadata)
    output_buffer.seek(0)
