import re
import unicodedata

# Helper function to remove diacritics from Greek text
def strip_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) 
                   if unicodedata.category(c) != 'Mn')

encrypted_text = open("8hXR7Qas.txt").read()
print(strip_diacritics(encrypted_text))
