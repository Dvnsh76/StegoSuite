from PIL import Image
import logging

def auto_decode_using_metadata_in_memory(input_buffer):
    logging.debug(f"AutoDecode: Starting for input buffer")
    
    try:
        img_pil = Image.open(input_buffer)
        metadata = img_pil.info
        logging.debug(f"AutoDecode: Metadata found in image: {metadata}")
        
        codeword = metadata.get("ProcessingInfo")
        if not codeword:
            logging.error(f"AutoDecode Error: Required metadata tag 'ProcessingInfo' not found in the image.")
            return "AutoDecode Error: Image does not contain required metadata for auto-detection."
            
        logging.info(f"AutoDecode: Found metadata tag 'ProcessingInfo' with codeword: '{codeword}'")
        
        input_buffer.seek(0)  # Reset buffer position
        
        if codeword == "banana":  # DCT
            from .dct import dct_decode_in_memory
            result = dct_decode_in_memory(input_buffer)
        elif codeword == "apple":  # LSBM
            from .lsbm import lsbm_decode_in_memory
            result = lsbm_decode_in_memory(input_buffer)
        elif codeword == "orange":  # PVD
            from .pvd import pvd_decode_in_memory
            result = pvd_decode_in_memory(input_buffer)
        elif codeword == "grape":  # ERDE
            from .erde import erde_decode_in_memory
            result = erde_decode_in_memory(input_buffer)
        else:
            logging.error(f"AutoDecode Error: Unknown or unsupported codeword '{codeword}' found in metadata.")
            return f"AutoDecode Error: Unsupported encoding scheme indicated by metadata ('{codeword}')."
            
        if result is not None and result != "":
            logging.info("AutoDecode: Decoding successful using metadata.")
            return result
        elif result == "":
            logging.warning(f"AutoDecode: Decoder returned an empty string (potentially no message embedded).")
            return ""
        else:
            logging.warning(f"AutoDecode: Decoder returned None (decoding failed).")
            return f"AutoDecode Error: Identified scheme '{codeword}' but failed to decode."
            
    except Exception as e:
        logging.error(f"An unexpected error occurred during auto-decoding: {type(e).__name__} - {e}")
        return f"AutoDecode Error: An unexpected error occurred ({type(e).__name__})."
