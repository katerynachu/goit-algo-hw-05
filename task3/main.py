import timeit
import functools

"""Boyre-Moore"""


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


"""KMP"""


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0 

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1] 
        else:
            i += 1

        if j == M:
            return i - j
            
    return -1


"""Rabin-Karp"""


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1, modulus)
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1, modulus)

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus

            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def run_tests():
    try:
        with open("1.txt", "r", encoding="utf-8") as file:
            text1 = file.read()
        with open("2.txt", "r", encoding="utf-8") as file:
            text2 = file.read()
    except FileNotFoundError:
        print("Oops ,so sorry it happend again")

    pattern_exists = "алгоритм"
    fake_pattern = "фея"

    REPEAT_COUNT = 5
    NUMBER_COUNT = 100

    algorithms = {
        "Боєр-Мур": boyer_moore_search,
        "КМП": kmp_search,
        "Рабін-Карп": rabin_karp_search
    }

    texts = {
        "Стаття 1": text1,
        "Стаття 2": text2
    }

    patterns = {
        "Існує": pattern_exists,
        "Вигаданий": fake_pattern
    }

    results = {}
    
    for text_name, text in texts.items():
        results[text_name] = {}
        for pattern_type, pattern in patterns.items():
            results[text_name][pattern_type] = {}
            
            print(f"\n--- {text_name} з підрядком '{pattern_type}' (довжина: {len(pattern)}) ---")
            
            for algo_name, algo_func in algorithms.items():
                
                timer = timeit.Timer(functools.partial(algo_func, text, pattern))
                times = timer.repeat(repeat=REPEAT_COUNT, number=NUMBER_COUNT)
                
                min_time = min(times) / NUMBER_COUNT 
                
                results[text_name][pattern_type][algo_name] = min_time
                print(f"  - {algo_name}: {min_time:.6f} сек")

if __name__ == '__main__':
    run_tests()                