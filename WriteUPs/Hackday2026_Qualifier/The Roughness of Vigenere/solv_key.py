import string

ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
    0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
    0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]

def load_ciphertext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    text = ''.join(c for c in text if c in string.ascii_lowercase)
    return text

def frequency(text):
    freq = [0]*26
    for c in text:
        freq[ord(c) - ord('a')] += 1
    total = len(text)
    return [f / total for f in freq]

def chi_squared_stat(observed_freq, expected_freq=ENGLISH_FREQ):
    chi2 = 0
    for o, e in zip(observed_freq, expected_freq):
        if e > 0:
            chi2 += ((o - e) ** 2) / e
    return chi2

def find_key(ciphertext, key_len):
    key = []
    for i in range(key_len):
        subtext = ciphertext[i::key_len]
        min_chi2 = float('inf')
        best_shift = 0
        for shift in range(26):
            shifted_text = [(ord(c) - ord('a') - shift) % 26 for c in subtext]
            freq_shifted = [0]*26
            for val in shifted_text:
                freq_shifted[val] += 1
            total = len(shifted_text)
            freq_shifted = [f/total for f in freq_shifted]
            chi2 = chi_squared_stat(freq_shifted)
            if chi2 < min_chi2:
                min_chi2 = chi2
                best_shift = shift
        key.append(chr(ord('A') + best_shift))
    return ''.join(key)

if __name__ == "__main__":
    filename = "mr_cipher.txt" 
    key_len = 372

    ciphertext = load_ciphertext(filename)
    key_guess = find_key(ciphertext, key_len)

    with open("key_retreived", "w", encoding="utf-8") as f:
        f.write(key_guess)

    print(f"Key retreived (len {key_len}): {key_guess}")

