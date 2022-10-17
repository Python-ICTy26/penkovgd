import caesar


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
    key_sequence = key_sequence[: len(plaintext)]
    for i in range(len(plaintext)):
        shift = ord(key_sequence[i]) - (65 if ord(key_sequence[i]) < 97 else 97)
        c = ord(plaintext[i])
        c = caesar.shift_chr(c, shift)
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
    key_sequence = ""
    while len(key_sequence) < len(ciphertext):
        key_sequence += keyword
    key_sequence = key_sequence[: len(ciphertext)]
    for i in range(len(ciphertext)):
        shift = ord(key_sequence[i]) - (65 if ord(key_sequence[i]) < 97 else 97)
        c = ord(ciphertext[i])
        c = caesar.shift_chr(c, -shift)
        plaintext += chr(c)
    return plaintext
