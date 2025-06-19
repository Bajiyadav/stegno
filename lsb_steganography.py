
import cv2
import numpy as np
from tqdm import tqdm

# ========================== XOR ENCRYPTION ==========================

def xor_encrypt_decrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def get_capacity(image):
    return image.shape[0] * image.shape[1] * 3 // 8

# ========================== ENCODING FUNCTION ==========================

def encode_message(image_path, secret_message, key, output_path="encoded_output.png"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("❌ Image not found!")

    encrypted_message = xor_encrypt_decrypt(secret_message, key)
    max_bytes = get_capacity(image)

    if len(encrypted_message) > max_bytes:
        raise ValueError("❌ Message too long for the image.")

    message_binary = ''.join(format(ord(c), '08b') for c in encrypted_message)
    message_binary += '1111111111111110'  # End marker

    encoded_image = np.copy(image)
    data_index = 0

    for row in tqdm(encoded_image, desc="Encoding", unit="row"):
        for pixel in row:
            for c in range(3):
                if data_index < len(message_binary):
                    pixel[c] = (pixel[c] & 0xFE) | int(message_binary[data_index])
                    data_index += 1

    cv2.imwrite(output_path, encoded_image)

    with open("encrypted_message.txt", "w") as f:
        f.write(encrypted_message)

    with open("encrypted_binary.txt", "w") as f:
        f.write(message_binary)

    print(f"✅ Encoded image saved to {output_path}")

# ========================== DECODING FUNCTION ==========================

def decode_message(image_path, key):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("❌ Image not found!")

    binary_data = ""
    for row in tqdm(image, desc="Decoding", unit="row"):
        for pixel in row:
            for c in range(3):
                binary_data += str(pixel[c] & 1)

    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == '11111111' and binary_data[i+8:i+16] == '11111110':
            break
        try:
            message += chr(int(byte, 2))
        except ValueError:
            break

    decrypted_message = xor_encrypt_decrypt(message, key)
    print(f"🔓 Decoded Message: {decrypted_message}")
    return decrypted_message

# ========================== CLI TEST (OPTIONAL) ==========================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="XOR LSB Steganography Tool")
    parser.add_argument("mode", choices=["encode", "decode"], help="Mode: encode or decode")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--key", required=True, type=int, help="XOR key (number)")
    parser.add_argument("--message", help="Secret message to encode (required for encode mode)")
    parser.add_argument("--output", default="encoded_output.png", help="Output image path")

    args = parser.parse_args()

    if args.mode == "encode":
        if not args.message:
            print("❌ Please provide a message using --message for encoding.")
        else:
            encode_message(args.image, args.message, args.key, args.output)
    elif args.mode == "decode":
        decode_message(args.image, args.key)
