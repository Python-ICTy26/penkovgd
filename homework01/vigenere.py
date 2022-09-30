def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_sequence = ""
    while len(key_sequence) < len(plaintext):
        key_sequence += keyword
    key_sequence = key_sequence[:len(plaintext)]
    for i in range(len(plaintext)):
        shift = ord(key_sequence[i]) - (65 if ord(key_sequence[i]) < 97 else 97)
        c = ord(plaintext[i])
        if ord('a') <= c <= ord('z'):    # ord(a) = 97 ord(z) = 122
            c = (c - 97 + shift) % 26 + 97
        if ord('A') <= c <= ord('Z'):    # ord(A) = 65 ord(Z) =
            c = (c - 65 + shift) % 26 + 65
        ciphertext += chr(c)
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    return plaintext
