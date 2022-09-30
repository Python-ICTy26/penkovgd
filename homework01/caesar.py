import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    ord_array = [ord(c) for c in plaintext]
    ord_array_encrypted = []
    for c in ord_array:
        if ord('a') <= c <= ord('z'):  # ord(a) = 97 ord(z) = 122
            c = (c - 97 + shift) % 26 + 97
        if ord('A') <= c <= ord('Z'):    # ord(A) = 97 ord(Z) = 122
            c = (c - 65 + shift) % 26 + 65
        ord_array_encrypted.append(c)
    ciphertext = ''.join(chr(c) for c in ord_array_encrypted)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    ord_array_encrypted = [ord(c) for c in ciphertext]
    ord_array_decrypted = []
    for c in ord_array_encrypted:
        if ord('a') <= c <= ord('z'):  # ord(a) = 97 ord(z) = 122
            c = (c - 97 - shift) % 26 + 97
        if ord('A') <= c <= ord('Z'):    # ord(A) = 97 ord(Z) = 122
            c = (c - 65 - shift) % 26 + 65
        ord_array_decrypted.append(c)
    plaintext = ''.join(chr(c) for c in ord_array_decrypted)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    for shift in range(1, 27):
        plaintext = decrypt_caesar(ciphertext, shift)
        if plaintext in dictionary:
            best_shift = shift
    print('Слово %s расшифровывается как: %s' %(ciphertext, decrypt_caesar(ciphertext, best_shift)))
    return best_shift
