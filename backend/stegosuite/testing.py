import os
import glob
from tabulate import tabulate
from metrics import calculate_metrics
import time

# Import all encoding and decoding functions
from encoders.erde import erde_encode
from encoders.lsbm import lsbm_encode
from encoders.dct import dct_encode
from encoders.pvd import pvd_encode
from decoders.erde import erde_decode
from decoders.lsbm import lsbm_decode
from decoders.dct import dct_decode
from decoders.pvd import pvd_decode

def run_tests():
    # Test message
    message = "hello i am devansh goel"
    print(f"Test message: '{message}'")
    
    # Create output directories - using os.path.join for cross-platform compatibility
    output_dir = r"C:\Users\Devansh\Desktop\New folder\StegoSuiteOld\backend-2\stegosuite\sample_images\output"
    stego_imgs_dir = r"C:\Users\Devansh\Desktop\New folder\StegoSuiteOld\backend-2\stegosuite\stego_images"
    
    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(stego_imgs_dir, exist_ok=True)
    
    # Get all test images from the images directory - using os.path.join
    img_dir = r"C:\Users\Devansh\Desktop\New folder\StegoSuiteOld\backend-2\stegosuite\sample_images"
    
    image_names = ["s1.png", "s2.png", "s3.png", "s4.png", 
                  "t1.png", "t2.png", "t3.png", "t4.png", 
                  "t5.png", "t6.png"]
    
    img_paths = []
    for img_name in image_names:
        img_path = os.path.join(img_dir, img_name)
        if os.path.exists(img_path):
            img_paths.append(img_path)
        else:
            print(f"Warning: Image {img_path} not found!")
    
    if not img_paths:
        print(f"No images found in {img_dir}! Please check directory path.")
        return
    
    print(f"Found {len(img_paths)} images for testing.\n")
    
    # Prepare results table
    results = []
    header = ["Image", "Scheme", "Encoding Time", "Decoding Time", "PSNR (dB)", "SSIM", "BER", "Decoded Message", "Success"]
    
    # Schemes to test
    schemes = [
        ("ERDE", erde_encode, erde_decode),
        ("LSB-M", lsbm_encode, lsbm_decode),
        ("DCT", dct_encode, dct_decode),
        ("PVD", pvd_encode, pvd_decode)
    ]
    
    # For each image, test all schemes
    for img_path in img_paths:
        img_name = os.path.basename(img_path)
        print(f"\nTesting image: {img_name}")
        
        for scheme_name, encoder, decoder in schemes:
            print(f"  Testing {scheme_name}...")
            
            # Create output path for stego image
            stego_output = os.path.join(
                stego_imgs_dir, 
                f"{os.path.splitext(img_name)[0]}_{scheme_name.lower()}.png"
            )
            
            try:
                # Measure encoding time
                start_time = time.time()
                encoder(img_path, message, stego_output)
                encode_time = time.time() - start_time
                
                # Calculate quality metrics
                metrics = calculate_metrics(img_path, stego_output)
                
                # Measure decoding time
                start_time = time.time()
                decoded_msg = decoder(stego_output)
                decode_time = time.time() - start_time
                
                # Check if decoding was successful
                success = decoded_msg == message
                
                # Add results to table
                results.append([
                    img_name,
                    scheme_name,
                    f"{encode_time:.3f}s",
                    f"{decode_time:.3f}s",
                    f"{metrics['psnr']:.2f}" if metrics else "N/A",
                    f"{metrics['ssim']:.4f}" if metrics else "N/A",
                    f"{metrics['ber']:.6f}" if metrics else "N/A",
                    decoded_msg[:30] + ("..." if len(decoded_msg or "") > 30 else "") if decoded_msg else "None",
                    "✓" if success else "✗"
                ])
                
            except Exception as e:
                # Record failure
                print(f"    Error: {str(e)}")
                results.append([
                    img_name,
                    scheme_name,
                    "Failed",
                    "Failed",
                    "N/A",
                    "N/A",
                    "N/A",
                    f"Error: {str(e)[:50]}...",
                    "✗"
                ])
    
    # Display results in a table
    print("\n" + "="*80)
    print("TEST RESULTS")
    print("="*80)
    print(tabulate(results, headers=header, tablefmt="grid"))
    
    # Save results to a text file
    # Save results to a text file
    with open(os.path.join(output_dir, "test_results.txt"), "w", encoding="utf-8") as f:
        f.write("Steganography Testing Results\n")
        f.write(f"Test message: '{message}'\n\n")
        f.write(tabulate(results, headers=header, tablefmt="grid"))

    
    # Print summary statistics
    success_count = sum(1 for row in results if row[-1] == "✓")
    total_tests = len(results)
    if total_tests > 0:
        print(f"\nSuccess rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
        
        for scheme_name, _, _ in schemes:
            scheme_total = sum(1 for row in results if row[1] == scheme_name)
            if scheme_total > 0:
                scheme_success = sum(1 for row in results if row[1] == scheme_name and row[-1] == "✓")
                print(f"{scheme_name} success rate: {scheme_success}/{scheme_total} ({scheme_success/scheme_total*100:.1f}%)")
    
    print(f"\nAll stego images have been saved to: {stego_imgs_dir}")
    print(f"Detailed results saved to: {os.path.join(output_dir, 'test_results.txt')}")

if __name__ == "__main__":
    print("Starting steganography testing...")
    run_tests()