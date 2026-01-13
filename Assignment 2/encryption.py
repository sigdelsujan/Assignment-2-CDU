SEPARATOR = "<<<META_END>>>"  # used to split tag section and encrypted section


def encrypt_one_char(ch, shift1, shift2):
    

    # lowercase letters
    if 'a' <= ch <= 'z':
        if 'a' <= ch <= 'm':
            # tag 0 = lowercase first half (a-m)
            shift = shift1 * shift2
            pos = ord(ch) - ord('a')
            new_pos = (pos + shift) % 26
            return chr(new_pos + ord('a')), '0'
        else:
            # tag 1 = lowercase second half (n-z)
            shift = shift1 + shift2
            pos = ord(ch) - ord('a')
            new_pos = (pos - shift) % 26
            return chr(new_pos + ord('a')), '1'

    # uppercase letters
    if 'A' <= ch <= 'Z':
        if 'A' <= ch <= 'M':
            # tag 2 = uppercase first half (A-M)
            shift = shift1
            pos = ord(ch) - ord('A')
            new_pos = (pos - shift) % 26
            return chr(new_pos + ord('A')), '2'
        else:
            # tag 3 = uppercase second half (N-Z)
            shift = shift2 * shift2
            pos = ord(ch) - ord('A')
            new_pos = (pos + shift) % 26
            return chr(new_pos + ord('A')), '3'

    # other characters unchanged
    # tag 4 = other
    return ch, '4'


def decrypt_one_char(ch, tag, shift1, shift2):
    

    # tag 0: lowercase a-m was shifted forward by shift1*shift2, so reverse is backward
    if tag == '0':
        shift = shift1 * shift2
        pos = ord(ch) - ord('a')
        new_pos = (pos - shift) % 26
        return chr(new_pos + ord('a'))

    # tag 1: lowercase n-z was shifted backward by shift1+shift2, so reverse is forward
    if tag == '1':
        shift = shift1 + shift2
        pos = ord(ch) - ord('a')
        new_pos = (pos + shift) % 26
        return chr(new_pos + ord('a'))

    # tag 2: uppercase A-M was shifted backward by shift1, so reverse is forward
    if tag == '2':
        shift = shift1
        pos = ord(ch) - ord('A')
        new_pos = (pos + shift) % 26
        return chr(new_pos + ord('A'))

    # tag 3: uppercase N-Z was shifted forward by shift2^2, so reverse is backward
    if tag == '3':
        shift = shift2 * shift2
        pos = ord(ch) - ord('A')
        new_pos = (pos - shift) % 26
        return chr(new_pos + ord('A'))

    # tag 4: other character, unchanged
    return ch


def encrypt_file(shift1, shift2):
    f = open("raw_text.txt", "r", encoding="utf-8", newline="")
    text = f.read()
    f.close()

    tags = ""
    encrypted = ""

    # Encrypt character by character
    for ch in text:
        enc_ch, tag = encrypt_one_char(ch, shift1, shift2)
        encrypted += enc_ch
        tags += tag

    
    f = open("encrypted_text.txt", "w", encoding="utf-8", newline="")
    f.write(tags)
    f.write("\n" + SEPARATOR + "\n")
    f.write(encrypted)
    f.close()


def decrypt_file(shift1, shift2):
    f = open("encrypted_text.txt", "r", encoding="utf-8", newline="")
    content = f.read()
    f.close()

    
    parts = content.split("\n" + SEPARATOR + "\n")
    tags = parts[0]
    encrypted = parts[1]

    # Decrypt character by character using tags
    decrypted = ""
    for i in range(len(encrypted)):
        decrypted += decrypt_one_char(encrypted[i], tags[i], shift1, shift2)

    
    f = open("decrypted_text.txt", "w", encoding="utf-8", newline="")
    f.write(decrypted)
    f.close()


def verify_files():
    f = open("raw_text.txt", "r", encoding="utf-8", newline="")
    original = f.read()
    f.close()

    f = open("decrypted_text.txt", "r", encoding="utf-8", newline="")
    decrypted = f.read()
    f.close()

    if original == decrypted:
        print("Decryption successful! Files match.")
    else:
        print("Decryption failed! Files do not match.")


shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

encrypt_file(shift1, shift2)
decrypt_file(shift1, shift2)
verify_files()



