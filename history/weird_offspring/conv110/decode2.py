import re
import unicodedata

# Helper function to remove diacritics from Greek text
def strip_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) 
                   if unicodedata.category(c) != 'Mn')

# Read in the encrypted Greek text  
encrypted_text = open("8hXR7Qas.txt").read()

# Strip out diacritics and special characters
cleaned_text = strip_diacritics(encrypted_text)
cleaned_text = re.sub(r'[^\u0370-\u03FF\s]', '', cleaned_text)

# Perform frequency analysis on characters and character pairs
char_freq = {}
pair_freq = {}

for char in cleaned_text:
    if char.isalpha():
        if char not in char_freq:
            char_freq[char] = 1
        else:
            char_freq[char] += 1

for i in range(len(cleaned_text)-1):        
    pair = cleaned_text[i:i+2]
    if pair.isalpha():
        if pair not in pair_freq:
            pair_freq[pair] = 1
        else:
            pair_freq[pair] += 1
            
# Sort frequency dictionaries by value in descending order            
sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True) 
sorted_pairs = sorted(pair_freq.items(), key=lambda x: x[1], reverse=True)

# Analyze frequency patterns and cross-reference with Greek language stats
# (Placeholder for more complex decryption logic)

print("Decryption in progress...")   
print("Most frequent characters:", sorted_chars[:10])
print("Most frequent character pairs:", sorted_pairs[:10]) 
