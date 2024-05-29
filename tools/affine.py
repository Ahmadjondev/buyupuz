alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.123456789"


def affine_encrypt(text, key):
    m = len(alphabet)

    a, b = key
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            x = alphabet.index(char)
            encrypted_text += alphabet[(a * x + b) % m]
        else:
            encrypted_text += char

    return encrypted_text
