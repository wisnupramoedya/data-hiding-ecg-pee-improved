def check_difference(secret, extracted_secret):
    """
    Memeriksa perbedaan antara dua string.

    Parameters:
        secret (str): String rahasia.
        extracted_secret (str): String ekstraksi rahasia.

    Returns:
        None

    Prints:
        - Pesan yang menunjukkan apakah ada perbedaan di antara kedua string
        - Jika ada perbedaan, pesan juga akan mencantumkan indeks pertama di mana perbedaan terjadi
          serta karakter yang berbeda pada masing-masing string pada indeks tersebut.

    Examples:
        >>> check_difference('abc', 'abd')
        2
        Perbedaan ditemukan pada indeks 2: 'c' != 'd'
        >>> check_difference('xyz', 'xyz')
        Tidak ada perbedaan di antara keduanya.
    """
    def first_different_index(str1, str2):
        # Tentukan panjang string terpendek
        min_len = min(len(str1), len(str2))
        # Loop melalui karakter-karakter string
        for i in range(min_len):
            if str1[i] != str2[i]:
                return i

        # Jika semua karakter sama sampai panjang minimal, namun panjang string tidak sama,
        # kembalikan panjang minimal
        if len(str1) != len(str2):
            return min_len

        # Jika tidak ada perbedaan ditemukan sampai panjang minimal, kembalikan -1
        return -1

    max_len = len(secret) if len(secret) > len(
        extracted_secret) else len(extracted_secret)
    string1 = secret.ljust(max_len, '0')
    string2 = extracted_secret.ljust(max_len, '0')
    different_index = first_different_index(string1, string2)

    if different_index != -1:
        print(
            f"Perbedaan ditemukan pada indeks {different_index}: '{string1[different_index]}' != '{string2[different_index]}'")
    else:
        print("Tidak ada perbedaan di antara keduanya.")
