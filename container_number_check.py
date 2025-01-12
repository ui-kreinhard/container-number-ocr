def calculate_iso_checksum(container_number):
    if len(container_number) != 10:
        raise ValueError("Die Container-Nummer muss genau 10 Zeichen lang sein.")

    letter_values = {
    'A': 10, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20,
    'K': 21, 'L': 23, 'M': 24, 'N': 25, 'O': 26, 'P': 27, 'Q': 28, 'R': 29, 'S': 30, 'T': 31,
    'U': 32, 'V': 34, 'W': 35, 'X': 36, 'Y': 37, 'Z': 38
    }

    digits = []
    for char in container_number:
        if char.isdigit():  # Ziffer bleibt gleich
            digits.append(int(char))
        elif char.isalpha():  # Buchstabe wird in Wert umgewandelt
            digits.append(letter_values[char])
        else:
            raise ValueError("Ungültiges Zeichen in der Container-Nummer.")

    weighted_sum = 0
    for i, value in enumerate(digits):
        weight = 2 ** i
        weighted_sum += value * weight

    checksum = weighted_sum % 11

    return 0 if checksum == 10 else checksum

def is_valid_iso_container(container_number):
    if len(container_number) != 11:
        return False

    base_number = container_number[:10]

    try:
        given_checksum = int(container_number[10])
    except ValueError:
        return False
    calculated_checksum = calculate_iso_checksum(base_number)
    return given_checksum == calculated_checksum

if __name__ == "__main__":
    print(is_valid_iso_container("HBSU2020428"))