from PIL import Image
import logging

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

def pvd_decode_in_memory(input_buffer):
    logging.debug(f"PVD Decode: Starting for input buffer")
    try:
        img = Image.open(input_buffer)
        metadata = img.info
        if "ProcessingInfo" in metadata:
            codeword = metadata.get("ProcessingInfo")
            if codeword == "orange":
                logging.info("PVD Decode: Found PVD metadata tag")
            else:
                logging.warning(f"PVD Decode: Found metadata with unexpected codeword: {codeword}")
        
        pixels = img.load()
        width, height = img.size
    except Exception as e:
        logging.error(f"PVD Decode Error: {e}")
        return None
        
    extracted_bits = []
    current_byte = []
    
    for y in range(height):
        for x in range(0, width - 1, 2):
            try:
                p1 = pixels[x, y][2]
                p2 = pixels[x + 1, y][2]
                d = abs(p2 - p1)
                lower, upper = get_range(d)
                n = min(3, upper.bit_length() - 1)
                
                if n <= 0:
                    continue
                    
                value = d - lower
                if value < 0 or value > (2**n - 1):
                    continue
                    
                bits = format(value, f'0{n}b')
                extracted_bits.extend(list(bits))
                
                while len(extracted_bits) >= 9:
                    byte_bits = ''.join(extracted_bits[:8])
                    parity_bit = extracted_bits[8]
                    extracted_bits = extracted_bits[9:]
                    
                    expected_parity = '1' if byte_bits.count('1') % 2 != 0 else '0'
                    if parity_bit != expected_parity:
                        logging.warning("PVD Decode: Parity check failed")
                        continue
                        
                    if byte_bits == '00000000':
                        logging.info("PVD Decode: Found terminator byte")
                        return ''.join(current_byte)
                        
                    current_byte.append(chr(int(byte_bits, 2)))
            except Exception as e:
                logging.warning(f"PVD Decode: Error processing pixel pair at ({x},{y}): {e}")
                continue
                
    logging.warning("PVD Decode: No terminator found, message might be incomplete")
    return ''.join(current_byte) if current_byte else ""
