import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import logging

def calculate_metrics_in_memory(cover_buffer, stego_buffer):
    """
    Calculate image quality metrics between cover and stego images.
    
    Args:
        cover_buffer: BytesIO buffer containing the cover image
        stego_buffer: BytesIO buffer containing the stego image
        
    Returns:
        Dictionary with PSNR, SSIM, and BER metrics
    """
    logging.debug("Calculating metrics between cover and stego images")
    
    try:
        # Open images from buffers
        cover_buffer.seek(0)
        stego_buffer.seek(0)
        
        cover_img = cv2.imdecode(np.frombuffer(cover_buffer.read(), np.uint8), cv2.IMREAD_COLOR)
        
        stego_buffer.seek(0)
        stego_img = cv2.imdecode(np.frombuffer(stego_buffer.read(), np.uint8), cv2.IMREAD_COLOR)
        
        if cover_img is None or stego_img is None:
            raise ValueError("Failed to decode image from buffer")
            
        # Ensure same dimensions for comparison
        if cover_img.shape != stego_img.shape:
            logging.warning(f"Cover ({cover_img.shape}) and stego ({stego_img.shape}) dimensions differ. Resizing stego for comparison.")
            stego_img = cv2.resize(stego_img, (cover_img.shape[1], cover_img.shape[0]))
            
        # Convert to float for calculations
        cover_float = cover_img.astype(np.float32) / 255.0
        stego_float = stego_img.astype(np.float32) / 255.0
        
        # Calculate PSNR
        try:
            psnr_value = psnr(cover_float, stego_float, data_range=1.0)
            if np.isinf(psnr_value):
                psnr_value = 100.0  # Cap infinite PSNR
        except Exception as e:
            logging.error(f"PSNR calculation failed: {e}")
            psnr_value = 0.0
            
        # Calculate SSIM
        try:
            ssim_value = ssim(cover_float, stego_float, data_range=1.0, channel_axis=2, win_size=7)
        except Exception as e:
            logging.error(f"SSIM calculation failed: {e}")
            ssim_value = 0.0
            
        # Calculate BER (Bit Error Rate)
        try:
            # Flatten arrays and convert to binary
            cover_bits = np.unpackbits(cover_img.flatten().astype(np.uint8))
            stego_bits = np.unpackbits(stego_img.flatten().astype(np.uint8))
            
            # Ensure same length
            min_len = min(len(cover_bits), len(stego_bits))
            cover_bits = cover_bits[:min_len]
            stego_bits = stego_bits[:min_len]
            
            # Calculate BER
            ber_value = np.sum(cover_bits != stego_bits) / min_len
        except Exception as e:
            logging.error(f"BER calculation failed: {e}")
            ber_value = 0.0
            
        metrics = {
            'psnr': float(psnr_value),
            'ssim': float(ssim_value),
            'ber': float(ber_value)
        }
        
        logging.info(f"Metrics calculated: PSNR={psnr_value:.2f}dB, SSIM={ssim_value:.4f}, BER={ber_value:.6f}")
        return metrics
        
    except Exception as e:
        logging.error(f"Metrics calculation failed: {e}")
        return {
            'psnr': 0.0,
            'ssim': 0.0,
            'ber': 0.0
        }
