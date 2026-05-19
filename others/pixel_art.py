from PIL import Image, ImageEnhance, ImageOps
import sys
import math
import os

BASE_SIZE = (192, 63)

def otsu_threshold(gray_image):
    hist = gray_image.histogram()
    if len(hist) < 256:
        hist.extend([0] * (256 - len(hist)))
        
    best_variance = 0
    best_threshold = 0
    
    total_pixels = sum(hist)
    sum_all = sum(i * count for i, count in enumerate(hist))
    
    sum_b = 0
    w_b = 0
    
    for t in range(256):
        w_b += hist[t]
        w_f = total_pixels - w_b
        if w_b == 0: continue
        if w_f == 0: break
        
        sum_b += t * hist[t]
        mu_b = sum_b / w_b
        mu_f = (sum_all - sum_b) / w_f
        
        variance_between = w_b * w_f * ((mu_b - mu_f)**2)
        
        if variance_between > best_variance:
            best_variance = variance_between
            best_threshold = t
            
    return best_threshold

def reverse_bits_in_hex(hex_string):
    REVERSE_TABLE = [
        int('{:08b}'.format(i)[::-1], 2)
        for i in range(256)
    ]
    data = bytes.fromhex(hex_string)
    reversed_data = bytes(REVERSE_TABLE[b] for b in data)
    return reversed_data.hex()

def hex_to_pixel_image(hex_string, size, output_path, scale_factor=1):
    """Creates scaled image from Hex string (1=Black, 0=White)."""
    try:
        binary_data = bytes.fromhex(hex_string)
    except:
        try:
            binary_data = bytes.fromhex(reverse_bits_in_hex(hex_string))
        except:
            raise ValueError("Hex data cannot be converted to bytes.")
    
    stride = (size[0] + 7) // 8
    expected_bytes = stride * size[1]
    current_bytes_len = len(binary_data)
    
    if current_bytes_len < expected_bytes:
        binary_data += b'\x00' * (expected_bytes - current_bytes_len)
    elif current_bytes_len > expected_bytes:
        binary_data = binary_data[:expected_bytes]
        
    img_reconstructed = Image.frombytes('1', size, binary_data)
    img_reconstructed = img_reconstructed.point(lambda x: 1 - x)
    
    if scale_factor > 1:
        output_width = size[0] * scale_factor
        output_height = size[1] * scale_factor
        img_reconstructed = img_reconstructed.resize((output_width, output_height), Image.Resampling.NEAREST)
        
    img_reconstructed.save(output_path)
    return output_path

def p2h_process(input_path, output_path, base_size=BASE_SIZE):
    """Processes image to sharp B&W, resizing proportionally and centering on canvas."""
    if not os.path.exists(input_path):
         raise FileNotFoundError(f"Input image not found: {input_path}")
    
    image = Image.open(input_path).convert("RGBA")
    
    background_white = Image.new("RGBA", image.size, (255, 255, 255, 255))
    image = Image.alpha_composite(background_white, image).convert("L")
    
    image = ImageEnhance.Contrast(image).enhance(1.5)
    
    image.thumbnail(base_size, Image.Resampling.LANCZOS)
    
    canvas = Image.new('L', base_size, 255)
    
    paste_x = (base_size[0] - image.width) // 2
    paste_y = (base_size[1] - image.height) // 2
    canvas.paste(image, (paste_x, paste_y))
    
    optimal_threshold = otsu_threshold(canvas)
    
    binary_image = canvas.point(lambda x: 0 if x > optimal_threshold else 1, '1')
    
    hex_data = binary_image.tobytes().hex()
    
    hex_to_pixel_image(hex_data, base_size, output_path, scale_factor=2)
    
    print(f"HEX_DATA_NEW:{hex_data}")

def h2p_process(hex_string, output_path, size=BASE_SIZE):
    if not hex_string:
        raise ValueError("Hex string is empty.")
    hex_to_pixel_image(hex_string, size, output_path, scale_factor=1)

def parse_size(size_str):
    try:
        w, h = size_str.lower().split("x")
        return (int(w), int(h))
    except:
        raise ValueError("Size format error (e.g., 192x63)")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if "x" in sys.argv[2]:
        size = parse_size(sys.argv[2])
        data_idx = 3
        out_idx = 4
    else:
        size = BASE_SIZE
        data_idx = 2
        out_idx = 3

    try:
        if command == "p2h":
            p2h_process(sys.argv[data_idx], sys.argv[out_idx], base_size=size)
        elif command == "h2p":
            h2p_process(sys.argv[data_idx], sys.argv[out_idx], size=size)
        else:
            sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
