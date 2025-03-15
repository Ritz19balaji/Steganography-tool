from PIL import Image

def encode_message(image_path, message, output_path):
    """Hides a message inside an image using LSB steganography."""
    img = Image.open(image_path)
    pixels = img.load()
    
    message += chr(0)  # Add a null character to mark the end
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    data_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if data_index < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & 0b11111110) | int(binary_message[data_index])  # Modify LSB of red channel
                pixels[x, y] = (r, g, b)
                data_index += 1

    img.save(output_path)
    print(f"[+] Message encoded into {output_path}")

def decode_message(image_path):
    """Extracts a hidden message from an image using LSB steganography."""
    img = Image.open(image_path)
    pixels = img.load()
    
    binary_message = ""
    for y in range(img.height):
        for x in range(img.width):
            r, _, _ = pixels[x, y]
            binary_message += str(r & 1)  # Extract LSB of red channel

    message = "".join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    message = message.split(chr(0), 1)[0]  # Stop at null character
    print(f"[+] Hidden message: {message}")

if __name__ == "__main__":
    choice = input("Choose (1) Encode or (2) Decode: ")
    
    if choice == "1":
        img_path = input("Enter input image path: ")
        msg = input("Enter message to hide: ")
        output_path = input("Enter output image path: ")
        encode_message(img_path, msg, output_path)
    
    elif choice == "2":
        img_path = input("Enter encoded image path: ")
        decode_message(img_path)
    
    else:
        print("[-] Invalid choice.")
