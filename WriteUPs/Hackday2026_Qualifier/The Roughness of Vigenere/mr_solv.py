import string
import sys

def load_ciphertext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    text = ''.join(c for c in text if c in string.ascii_lowercase)
    return text

def global_letter_probabilities(text):
    n = 26
    length = len(text)
    freq = [0]*n
    for c in text:
        freq[ord(c)-ord('a')] += 1
    probs = [f/length for f in freq]
    return probs

def measure_of_roughness_with_global_probs(text, key_len, global_probs):
    n = 26
    mr_values = []
    for i in range(key_len):
        group_chars = text[i::key_len]
        length = len(group_chars)
        if length == 0:
            mr_values.append(0)
            continue
        freq = [0]*n
        for c in group_chars:
            freq[ord(c)-ord('a')] += 1
        group_probs = [f/length for f in freq]
        mr = sum((group_probs[j] - global_probs[j])**2 for j in range(n))
        mr_values.append(mr)

    return sum(mr_values)/key_len

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <ciphertext_file>")
        sys.exit(1)
    filename = sys.argv[1]
    ciphertext = load_ciphertext(filename)
    global_probs = global_letter_probabilities(ciphertext)
    max_key_len = 700
    max_mr = 0
    best_key_len = 0
    for key_len in range(1, max_key_len + 1):
        mr = measure_of_roughness_with_global_probs(ciphertext, key_len, global_probs)
        if mr > max_mr:
            max_mr = mr
            best_key_len = key_len

    print(f"Max MR = {max_mr:.6f} for Key length = {best_key_len}")

