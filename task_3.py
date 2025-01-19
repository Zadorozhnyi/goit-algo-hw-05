# Re-run the script after the execution state reset

import requests
import timeit
import re
import pandas as pd

# Function to download text files from Google Drive
def download_text_file(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# File IDs extracted from the Google Drive links
file_id_1 = "18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh"
file_id_2 = "18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w"

# Download the text files
text1 = download_text_file(file_id_1)
text2 = download_text_file(file_id_2)

# Boyer-Moore Algorithm
def boyer_moore_search(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0 or n == 0 or m > n:
        return -1

    last = {pattern[i]: i for i in range(m)}

    i = m - 1
    j = m - 1

    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i  # Match found
            i -= 1
            j -= 1
        else:
            lo = last.get(text[i], -1)
            i += m - min(j, lo + 1)
            j = m - 1
    return -1

# Knuth-Morris-Pratt Algorithm
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        j = 0
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = lps[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
                lps[i] = j
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            j = lps[j - 1] if j > 0 else 0
            i += 1 if j == 0 else 0
    return -1

# Rabin-Karp Algorithm
def rabin_karp_search(text, pattern, prime=101):
    d = 256
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    pattern_hash = text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % prime

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
        text_hash = (d * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash and text[i:i + m] == pattern:
            return i

        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime

    return -1

# Define substrings for search
existing_substring = text1[50:100]  
fake_substring = "thissubstringdoesnotexist"  

# Measure execution time
def measure_time(search_function, text, pattern):
    return timeit.timeit(lambda: search_function(text, pattern), number=1000)

# Test on both texts
results = []
for text, text_name in [(text1, "Text 1"), (text2, "Text 2")]:
    for pattern, pattern_type in [(existing_substring, "Existing"), (fake_substring, "Non-Existing")]:
        times = {
            "Boyer-Moore": measure_time(boyer_moore_search, text, pattern),
            "Knuth-Morris-Pratt": measure_time(kmp_search, text, pattern),
            "Rabin-Karp": measure_time(rabin_karp_search, text, pattern)
        }
        fastest_algo = min(times, key=times.get)
        results.append({
            "Text": text_name,
            "Pattern Type": pattern_type,
            "Boyer-Moore Time": times["Boyer-Moore"],
            "Knuth-Morris-Pratt Time": times["Knuth-Morris-Pratt"],
            "Rabin-Karp Time": times["Rabin-Karp"],
            "Fastest Algorithm": fastest_algo
        })

# Create DataFrame and display results
df_results = pd.DataFrame(results)

# Display results
print("Comparison of Search Algorithms:")
print(df_results.to_string(index=False))
