import string

# Funkce pro převod čísla do libovolné base
def to_base(n, base):
    if n == 0:
        return "0"
    
    digits = string.ascii_letters + string.digits + string.punctuation + " "  # Znaková sada pro base > 62
    result = ""
    
    while n:
        result = digits[n % base] + result
        n //= base
    
    return result

# Funkce pro převod z libovolné base zpět na číslo
def from_base(s, base):
    digits = string.ascii_letters + string.digits + string.punctuation + " "
    char_to_val = {char: i for i, char in enumerate(digits)}
    
    num = 0
    for char in s:
        num = num * base + char_to_val[char]
    
    return num

# Funkce pro šifrování
def encrypt(text, base):
    encoded = "".join(to_base(ord(char), base) for char in text)
    return encoded

# Funkce pro dešifrování
def decrypt(text, base):
    decoded = "".join(chr(from_base(text[i:i+len(to_base(ord('A'), base))], base)) for i in range(0, len(text), len(to_base(ord('A'), base))))
    return decoded

# Funkce pro bruteforce dešifrování
def bruteforce(text):
    results = []
    
    for base in range(32, 10001):  # Prozkoumáme base nad 31
        try:
            decoded = decrypt(text, base)
            # Zkontrolujeme, zda výstup obsahuje jen ASCII znaky
            if all(32 <= ord(c) < 127 for c in decoded):
                results.append((base, decoded))
        except:
            pass  # Pokud nějaký base nefunguje, přeskočíme

    return results

# Hlavní funkce pro interakci s uživatelem
def main():
    action = input("Chceš šifrovat nebo dešifrovat? (šifrovat/dešifrovat): ").strip().lower()
    
    if action == "šifrovat":
        text = input("Zadej text k šifrování: ")
        base = int(input("Zadej základ (2-10000): "))
        encrypted = encrypt(text, base)
        print(f"Zašifrovaný text: {encrypted}")
    
    elif action == "dešifrovat":
        text = input("Zadej text k dešifrování: ")
        base = input("Zadej základ (nebo 'bruteforce' pro bruteforce): ").strip().lower()
        
        if base == "bruteforce":
            results = bruteforce(text)
            if results:
                print("Bruteforce výsledky:")
                for base, decoded in results:
                    print(f"Base {base}: {decoded}")
            else:
                print("Bruteforce nenašlo žádné platné výsledky.")
        else:
            base = int(base)
            decrypted = decrypt(text, base)
            print(f"Dešifrovaný text: {decrypted}")
    
    else:
        print("Neplatná volba. Zkus to znovu.")

# Spuštění programu
if __name__ == "__main__":
    main()
