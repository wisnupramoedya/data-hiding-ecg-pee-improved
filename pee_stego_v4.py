import numpy as np
import warnings
from typing import Literal, List
import math
import time
from utils.result import Result

# Disable only the specific NumPy deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)


def llp(arr: np.ndarray[np.any, np.int64]):
    return round(np.mean(arr))


class PEEStego:
    """
    PEE Steganografi versi 3:
    - memakai sistem mirror embedding
    """

    def __init__(self, is_frequency_log=True):
        self.is_frequency_log = is_frequency_log

    def embed(self, original_data: np.ndarray[np.any, np.int64],
              secret_data: str,
              payload_rate: int = 1,
              threshold: int = 0):
        """
        Embeds data using the PEE technique.

        Args:
            original_data (np.ndarray): Original data (e.g., an image) as a NumPy array.
            secret_data (str): Secret data to be embedded.
            payload_rate (int, optional): Payload rate (number of bits to embed per phase). Defaults to 1.
            threshold (int, optional): Threshold for embedding. Defaults to 0.

        Returns:
            Tuple[np.ndarray, List[int], int, int, int, Result]: A tuple containing:
                - watermarked_data (np.ndarray): Watermarked data after embedding.
                - mirror_data (List[int]): List of mirror differences.
                - last_phase (int): Last phase used during embedding.
                - last_i (int): Last index processed during embedding.
                - last_embedded_bit_total (int): Total number of bits embedded in the last embedding.
                - result (Result): Result object with performance metrics.
        """
        start_time = time.time()

        watermarked_data = original_data.copy()
        secret_index = 0

        errors = []
        mirror_data = []
        last_phase = 0
        last_i = 0
        last_embedded_bit_total = 0
        result = Result()

        has_embedding_end = False

        # PEE for hiding the secret
        for phase in range(1, 4):
            if has_embedding_end:
                break

            for i in self.get_phase_indexes(phase, len(watermarked_data)):
                secret_remainder = len(secret_data) - secret_index
                if secret_remainder <= 0:
                    has_embedding_end = True
                    # print(has_embedding_end)
                    break

                if i + 4 >= len(watermarked_data):
                    break

                # Get error from predicted value and original value
                original_value = watermarked_data[i+2]
                predicted_value = int(llp(
                    np.array([watermarked_data[i], watermarked_data[i+1], watermarked_data[i+3], watermarked_data[i+4]])))
                embedding_error = abs(original_value - predicted_value)
                if embedding_error <= 1:
                    errors.append(embedding_error)
                    continue

                available_bit = math.floor(math.log2(embedding_error))
                available_bit = secret_remainder if available_bit > secret_remainder else available_bit

                embedded_bit_total = math.ceil(
                    payload_rate + threshold) if available_bit >= payload_rate + threshold else available_bit
                last_embedded_bit_total = embedded_bit_total

                secret_value_limit = 2**embedded_bit_total
                half_secret_value_limit = int((secret_value_limit/2) - 1)
                mirror_total = math.floor(
                    (embedding_error - half_secret_value_limit)/secret_value_limit) + 1

                first_mirror_point = original_value - \
                    half_secret_value_limit if predicted_value <= original_value else original_value + \
                    half_secret_value_limit

                secret_value = int(
                    secret_data[secret_index:secret_index+embedded_bit_total], 2)
                embedding_diff = secret_value if mirror_total % 2 else (
                    secret_value_limit - secret_value) % secret_value_limit

                watermarked_value = first_mirror_point + \
                    embedding_diff if predicted_value <= original_value else first_mirror_point - embedding_diff
                mirror_diff = watermarked_value - original_value
                mirror_data.append(mirror_diff)

                secret_index += embedded_bit_total
                watermarked_data[i+2] = watermarked_value
                last_i = i

                # print("EMB -> i:", i, "OV:", original_value, "PV:", predicted_value,
                #       "WV:", watermarked_value, "sv:", secret_value, "I:", mirror_diff)

            last_phase = phase

        end_time = time.time()

        print(watermarked_data[0: 10])

        # Log frekuensi yang muncul
        if self.is_frequency_log:
            Result.log_frequency(errors, 1, is_greater=False)
        # Log result
        result.calculate(original_data, watermarked_data,
                         end_time - start_time)

        return watermarked_data, mirror_data, last_phase, last_i, last_embedded_bit_total, result

    def extract(self, watermarked_data: np.ndarray[np.any, np.int64],
                mirror_data: List[int],
                last_phase: int,
                last_i: int,
                last_embedded_bit_total: int,
                payload_rate: int = 1,
                threshold: int = 0):
        """
        Extracts secret data from watermarked data using the PEE (Phase-Encoded Embedding) technique.

        Args:
            watermarked_data (np.ndarray): Watermarked data (e.g., an image) as a NumPy array.
            mirror_data (List[int]): List of mirror differences obtained during embedding.
            last_phase (int): Last phase used during embedding.
            last_i (int): Last index processed during embedding.
            last_embedded_bit_total (int): Total number of bits embedded in the last phase.
            payload_rate (int, optional): Payload rate (number of bits embedded per phase). Defaults to 1.
            threshold (int, optional): Threshold for embedding. Defaults to 0.

        Returns:
            Tuple[np.ndarray, str]: A tuple containing:
                - original_data (np.ndarray): Original data after extraction.
                - secret_data (str): Extracted secret data.
        """
        original_data = watermarked_data.copy()
        secret_data = ''
        has_last_phase = False
        has_last_i = False
        has_last_embedded_bit = False

        for phase in reversed(range(1, 4)):
            if not has_last_phase:
                has_last_phase = phase == last_phase
                if not has_last_phase:
                    continue

            for i in reversed(self.get_phase_indexes(phase, len(original_data))):
                if not has_last_i:
                    has_last_i = i == last_i
                    if not has_last_i:
                        continue

                if i + 4 >= len(original_data):
                    continue

                # Get error from predicted value and watermarked value
                watermarked_value = original_data[i+2]
                predicted_value = int(llp(
                    np.array([original_data[i], original_data[i+1], original_data[i+3], original_data[i+4]])))

                if len(mirror_data) == 0:
                    continue

                mirror_value = mirror_data[-1]
                extraction_error = abs(watermarked_value - predicted_value) - mirror_value if predicted_value <= watermarked_value else abs(
                    watermarked_value - predicted_value) + mirror_value

                if abs(watermarked_value - predicted_value) <= 1:
                    continue

                original_value = watermarked_value - mirror_value
                original_data[i+2] = original_value

                available_bit = math.floor(math.log2(extraction_error))
                if not has_last_embedded_bit:
                    available_bit = last_embedded_bit_total
                    has_last_embedded_bit = True

                extraction_bit_total = math.ceil(
                    payload_rate + threshold) if available_bit >= payload_rate + threshold else available_bit

                secret_value_limit = 2**extraction_bit_total
                half_secret_value_limit = int((secret_value_limit/2) - 1)
                mirror_total = math.floor(
                    (extraction_error - half_secret_value_limit)/secret_value_limit) + 1

                first_mirror_point = original_value - \
                    half_secret_value_limit if predicted_value <= watermarked_value else original_value + \
                    half_secret_value_limit

                secret_value = abs(watermarked_value - first_mirror_point) if mirror_total % 2 else (
                    secret_value_limit - abs(watermarked_value - first_mirror_point)) % secret_value_limit
                secret_data = bin(secret_value)[
                    2:].zfill(extraction_bit_total) + secret_data

                mirror_data = mirror_data[:-1]

                # print("EXT -> i:", i, "OV:", original_value, "PV:", predicted_value,
                #       "WV:", watermarked_value, "sv:", secret_value, "I:", mirror_value)

                # print("191 -> SEC VALUE LIMIT: ", secret_value_limit,
                #       "MIRROR TOTAL: ", mirror_total)
                # print(i, secret_value, bin(secret_value)[
                #     2:].zfill(extraction_bit_total))

            print(original_data[0: 10])
        return original_data, secret_data

    def get_phase_indexes(self, phase: Literal[1, 2, 3], max_len: int = 3_600):
        """
        Memberikan range untuk fase ke-x dengan panjang maksimal ke-sekian
        """
        return range(phase - 1, max_len, 3)
