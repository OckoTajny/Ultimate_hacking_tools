def generate_charset(base=10000):
    """
    Generates a charset of up to `base` unique Unicode characters.
    Prioritizes printable ASCII, then CJK Unified Ideographs, then other Unicode characters.
    """
    charset = []
    
    # 1. Add printable ASCII characters (space to ~)
    charset += [chr(i) for i in range(32, 127)]
    
    # 2. Add CJK Unified Ideographs ranges
    cjk_ranges = [
        (0x4E00, 0x9FFF),    # Basic CJK Unified Ideographs
        (0x3400, 0x4DBF),    # CJK Unified Ideographs Extension A
        (0x20000, 0x2A6DF)   # CJK Unified Ideographs Extension B (Python 3.3+ supports these)
    ]
    
    for start, end in cjk_ranges:
        for code_point in range(start, end + 1):
            if len(charset) >= base:
                break
            try:
                charset.append(chr(code_point))
            except Exception:
                # Skip invalid code points
                continue
        if len(charset) >= base:
            break
    
    # 3. Fill remaining slots with other Unicode characters starting from U+00A1
    code_point = 0x00A1
    while len(charset) < base and code_point <= 0x10FFFF:
        try:
            char = chr(code_point)
            if char not in charset:
                charset.append(char)
        except Exception:
            # Skip invalid code points
            pass
        code_point += 1
    
    if len(charset) < base:
        print(f"Warning: Only generated {len(charset)} characters out of requested {base}.")
    
    return charset[:base]

def to_base(n, base):
    """
    Converts a non-negative integer n to its string representation in the given base,
    using the generated charset.
    """
    try:
        if n < 0:
            raise ValueError("Negative numbers are not supported.")
        digits = generate_charset(base)
        if n == 0:
            return digits[0]
        result = ""
        while n > 0:
            result = digits[n % base] + result
            n //= base
        return result
    except Exception as e:
        raise ValueError(f"Error in to_base conversion: {e}")

def from_base(s, base):
    """
    Converts a string s representing a number in the given base back to an integer.
    """
    try:
        digits = generate_charset(base)
        char_to_val = {char: i for i, char in enumerate(digits)}
        num = 0
        for char in s:
            if char not in char_to_val:
                raise ValueError(f"Character '{char}' not in base {base} charset.")
            num = num * base + char_to_val[char]
        return num
    except Exception as e:
        raise ValueError(f"Error in from_base conversion: {e}")

def max_encoding_length(base):
    """
    Returns the maximum length of encoding needed for any Unicode character in the given base.
    """
    try:
        max_unicode_code_point = 0x10FFFF
        return len(to_base(max_unicode_code_point, base))
    except Exception as e:
        raise ValueError(f"Error calculating max encoding length: {e}")

def encrypt(text, base):
    """
    Encrypts the input text by converting each character's Unicode code point to the specified base.
    Pads each encoded character to a fixed length for consistent decoding.
    """
    try:
        encoding_length = max_encoding_length(base)
        encoded = ""
        for char in text:
            char_code = to_base(ord(char), base)
            # Pad with leading zeros to fixed length
            char_code = char_code.zfill(encoding_length)
            encoded += char_code
        return encoded
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")

def decrypt(text, base):
    """
    Decrypts the encoded text by splitting into fixed-length segments and converting each back to a character.
    """
    try:
        encoding_length = max_encoding_length(base)
        if len(text) % encoding_length != 0:
            raise ValueError(f"Input length {len(text)} is not a multiple of encoding length {encoding_length}.")
        decoded = ""
        for i in range(0, len(text), encoding_length):
            part = text[i:i+encoding_length]
            # Remove leading zeros before conversion
            val = from_base(part.lstrip(generate_charset(base)[0]), base)
            decoded += chr(val)
        return decoded
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

def bruteforce(text):
    """
    Attempts to decrypt the text by trying bases from 32 to 127 and returns plausible results.
    """
    results = []
    for base in range(32, 128):
        try:
            decoded = decrypt(text, base)
            # Check if all characters are printable ASCII
            if all(32 <= ord(c) < 127 for c in decoded) and len(decoded) > 0:
                results.append((base, decoded))
        except Exception:
            continue  # Ignore errors and try next base
    return results

def main():
    try:
        action = input("Do you want to encrypt or decrypt? (encrypt/decrypt): ").strip().lower()
        
        if action == "encrypt":
            text = input("Enter text to encrypt: ")
            base = int(input("Enter base (2-10000): "))
            if base < 2 or base > 10000:
                print("Base must be between 2 and 10000.")
                return
            encrypted = encrypt(text, base)
            print(f"Encrypted text:\n{encrypted}")
        
        elif action == "decrypt":
            text = input("Enter text to decrypt: ")
            base_input = input("Enter base (or 'bruteforce' for brute force): ").strip().lower()
            
            if base_input == "bruteforce":
                results = bruteforce(text)
                if results:
                    print("Brute force results:")
                    for base, decoded in results:
                        print(f"Base {base}: {decoded}")
                else:
                    print("Brute force found no valid results.")
            else:
                base = int(base_input)
                if base < 2 or base > 10000:
                    print("Base must be between 2 and 10000.")
                    return
                decrypted = decrypt(text, base)
                print(f"Decrypted text:\n{decrypted}")
        
        else:
            print("Invalid option. Please choose 'encrypt' or 'decrypt'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
