import wfdb
import numpy as np
import os
from typing import List

ECG_FOLDER_PATH = 'data/mit-bih-arrhythmia-database-1.0.0/'


def get_secret_file(secret_path: str) -> str:
    """
    Membaca isi file rahasia dari path yang diberikan.

    Parameters:
    - secret_path (str): Nama path dan file secret dengan ekstensi.

    Returns:
    str: Isi file rahasia dalam bentuk string.

    Raises:
    FileNotFoundError: Jika file tidak ditemukan.
    Exception: Jika terjadi kesalahan selama pembacaan file.

    Example:
    get_secret_file('secret_0.15_bps')
    """
    try:
        # Membuka file untuk membaca
        with open(secret_path, 'r') as file:
            # Membaca isi file ke dalam string
            secret_content = file.read()
            return secret_content
    except FileNotFoundError:
        print(f"File '{secret_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_original_data(patient_code: str, batch_index: int = 0) -> np.ndarray:
    """
    Mengambil data asli dari pasien berdasarkan kode pasien.

    Parameters:
    - patient_code (str): Kode pasien/nama file tanpa ekstensi.
    - batch_index (int): Index batch pengambilan data.

    Returns:
    numpy.ndarray: Data asli dari pasien dalam bentuk array NumPy.

    Notes:
    Fungsi ini menggunakan data dari MIT-BIH Arrhythmia Database. Pastikan
    folder_path sesuai dengan lokasi dataset pada sistem Anda.

    Example:
    get_original_data('100')

    """
    record, information = wfdb.rdsamp(
        ECG_FOLDER_PATH + patient_code, channel_names=['MLII'])

    duration_seconds = 10
    sampling_frequency = information['fs']  # Sampling frequency in Hz
    duration_samples = int(duration_seconds * sampling_frequency)

    return (np.array(record[(batch_index * duration_samples):((batch_index * duration_samples) + duration_samples)]).flatten() * 1000).astype(np.int64)


def slice_batch_data(patient_code: str, max_batch: int = 10) -> List[np.ndarray]:
    """
    Mengambil data pasien berdasarkan kode pasien dan membaginya menjadi beberapa batch.

    Parameters:
    - patient_code (str): Kode pasien.
    - max_batch (int, opsional): Jumlah batch maksimal yang dihasilkan. Default: 10.

    Returns:
    List[np.ndarray]: Daftar batch data pasien dalam bentuk array NumPy.

    Notes:
    Fungsi ini menggunakan data dari MIT-BIH Arrhythmia Database. Pastikan
    folder_path sesuai dengan lokasi dataset pada sistem Anda.

    Example:
    slice_batch_data('100', max_batch=5)

    """
    record, information = wfdb.rdsamp(
        ECG_FOLDER_PATH + patient_code, channel_names=['MLII'])

    duration_seconds = 10
    sampling_frequency = information['fs']  # Sampling frequency in Hz
    duration_samples = int(duration_seconds * sampling_frequency)

    if record is None:
        return []

    return [(np.array(record[(i*duration_samples):(i*duration_samples)+duration_samples]).flatten() * 1000).astype(np.int64)
            for i in range(max_batch)]


def get_filenames_from_folder(extension: str, folder_path: str):
    """
    Mengambil semua nama file dengan ekstensi tertentu dari sebuah folder.

    Parameters:
        extension (str): Ekstensi file yang dicari (contoh: 'txt', 'jpg', 'png').
        folder_path (str): Path ke folder yang akan dicari.

    Returns:
        list: Daftar nama file tanpa ekstensi yang cocok dengan ekstensi yang diberikan.
    """
    # Dapatkan semua nama file dengan ekstensi yang sesuai dari folder
    files = [f for f in os.listdir(folder_path) if f.endswith(f'.{extension}')]

    # Ambil nama file tanpa ekstensi
    file_names_without_extension = [os.path.splitext(f)[0] for f in files]

    return file_names_without_extension
