import string
import argparse


def read_ciphertext_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().replace(" ", "").replace("\n", "")

def parse_key_lengths(key_lengths_str):
    return [int(k) for k in key_lengths_str.split(",")]

# ----------- Frequency Analysis and Measure of Roughness -----------

def calculate_frequencies(column):
    frequencies = {letter: 0 for letter in string.ascii_uppercase}
    total_letters = 0
    
    for letter in column:
        if letter in frequencies:
            frequencies[letter] += 1
            total_letters += 1
    
    return frequencies, total_letters

def calculate_mr(frequencies, total_letters):
    if total_letters < 2:
        return 0
    mr = sum(f * (f - 1) for f in frequencies.values())
    mr /= total_letters * (total_letters - 1)
    return mr

# ----------- Ciphertext Division and Key Length Analysis -----------

def divide_into_columns(ciphertext, key_length):
    columns = ['' for _ in range(key_length)]
    for index, letter in enumerate(ciphertext):
        if letter.isalpha():
            columns[index % key_length] += letter.upper()
    return columns

def average_mr_for_key_length(ciphertext, key_length):
    columns = divide_into_columns(ciphertext, key_length)
    total_mr = 0
    
    for column in columns:
        frequencies, total_letters = calculate_frequencies(column)
        total_mr += calculate_mr(frequencies, total_letters)
    
    return total_mr / key_length

def find_most_likely_key_length(ciphertext, key_lengths, mr_english=0.0686):
    best_key_length = None
    closest_mr = float('inf')
    
    for key_length in key_lengths:
        avg_mr = average_mr_for_key_length(ciphertext, key_length)
        print(f"Key Length: {key_length}, Average MR: {avg_mr:.4f}")
        
        if abs(avg_mr - mr_english) < closest_mr:
            closest_mr = abs(avg_mr - mr_english)
            best_key_length = key_length
    
    return best_key_length



def main():
    parser = argparse.ArgumentParser(description="Vigenère cipher key length guesser based on Measure of Roughness (MR).")
    parser.add_argument("ciphertext_file", help="Path to the text file containing the ciphertext", type=str)
    parser.add_argument("key_lengths", help="List of possible key lengths, separated by commas", type=str)
    
    args = parser.parse_args()
    
    ciphertext = read_ciphertext_from_file(args.ciphertext_file)
    key_lengths = parse_key_lengths(args.key_lengths)
    most_likely_key_length = find_most_likely_key_length(ciphertext, key_lengths)
    
    print(f"\nMost likely key length: {most_likely_key_length}")

if __name__ == "__main__":
    main()
