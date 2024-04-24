from collections import Counter
import numpy as np
from utils.log import THRESHOLD_ERROR_LOG
from utils.calculation import Calculation


class Result:
    timer: float

    ncc: float
    prd: float
    snr: float

    unhidden_secret_count: int = 0

    """
    Jumlah secret data yang tidak bisa tersimpan
    """

    def calculate(self, original_signal: np.ndarray, reconstructed_signal: np.ndarray, execution_time: float):
        self.ncc = Calculation.ncc(original_signal, reconstructed_signal)
        self.prd = Calculation.prd(original_signal, reconstructed_signal)
        self.snr = Calculation.snr(original_signal, reconstructed_signal)
        self.psnr = Calculation.psnr(original_signal, reconstructed_signal)
        self.timer = execution_time
        print(f'Unhidden secret: {self.unhidden_secret_count}')
        print(f'NCC: {self.ncc}')
        print(f'PRD: {self.prd}')
        print(f'SNR: {self.snr}')
        print(f'PSNR: {self.psnr}')
        print(f'Time: {self.timer}')

    @staticmethod
    def log_frequency(errors: int, threshold: int = 4, is_greater=True):
        # Gunakan Counter untuk menghitung frekuensi masing-masing angka
        frequency_counter = Counter(errors)
        greater_than_threshold_total = 0

        with open(THRESHOLD_ERROR_LOG, "a") as file_log:
            print(
                f"Frekuensi untuk threshold {threshold}:", file=file_log)

            if is_greater:
                for number, frequency in frequency_counter.items():
                    if abs(number) > threshold:
                        greater_than_threshold_total += frequency
                        print(
                            f"Angka {number}: {frequency} kali", file=file_log)

                print(
                    f"Total yang lebih dari threshold (T = {threshold}): {greater_than_threshold_total}", file=file_log)
                print(
                    f"Total yang lebih dari threshold (T = {threshold}): {greater_than_threshold_total}")
            else:
                for number, frequency in frequency_counter.items():
                    if abs(number) <= threshold:
                        greater_than_threshold_total += frequency
                        print(
                            f"Angka {number}: {frequency} kali", file=file_log)

                print(
                    f"Total yang kurang dari sama dengan threshold (T = {threshold}): {greater_than_threshold_total}", file=file_log)
                print(
                    f"Total yang kurang dari sama dengan threshold (T = {threshold}): {greater_than_threshold_total}")
