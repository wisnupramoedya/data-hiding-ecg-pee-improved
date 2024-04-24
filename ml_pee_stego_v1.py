import numpy as np
import warnings
from typing import Literal
import math
import time
from utils.result import Result

# Disable only the specific NumPy deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)


class MLPEEStego:
    """
    ML PEE Steganografi versi 1:
    - hanya menampilkan cek fase.
    """

    def __init__(self, model, is_frequency_log=True):
        self.model = model
        self.is_frequency_log = is_frequency_log

    def embed(self, original_data: np.ndarray[np.any, np.int64], secret_data: str,
              threshold: int = 4, secret_key: str = '000'):
        """
        Embed data for PEE
        """
        start_time = time.time()

        watermarked_data = original_data.copy()
        secret_index = 0

        result = Result()
        errors = []

        for phase in range(1, 4):
            if secret_key[phase - 1] == '0':
                continue

            for i in self.get_phase_indexes(phase, len(watermarked_data)):
                if i + 4 >= len(watermarked_data):
                    break

                # Get error from predicted value and original value
                original_value = watermarked_data[i+2]
                predicted_value = int(self.model.predict(
                    [[watermarked_data[i], watermarked_data[i+1], watermarked_data[i+3], watermarked_data[i+4]]]))
                error_embedding = original_value - predicted_value

                errors.append(error_embedding)

                expanded_error = 0
                # check threshold
                if abs(error_embedding) < threshold:
                    bit = 1 if secret_index < len(
                        secret_data) and secret_data[secret_index] == '1' else 0
                    expanded_error = 2*error_embedding + bit
                    secret_index += 1
                else:
                    if error_embedding > 0:
                        expanded_error = error_embedding + threshold
                    else:
                        expanded_error = error_embedding - threshold + 1

                watermarked_value = predicted_value + expanded_error

                # if (i + 2 == 8):
                #     print('Index', i+2, 'Original', original_value, 'Predicted', predicted_value,
                #           'Error Emb', error_embedding, 'Bit', bit, 'Watermark', watermarked_value)

                watermarked_data[i+2] = watermarked_value

        end_time = time.time()

        print(watermarked_data[0: 10])
        result.unhidden_secret_count = len(secret_data) - secret_index

        # Log frekuensi yang muncul
        if self.is_frequency_log:
            Result.log_frequency(errors, threshold)

        # Log result
        result.calculate(original_data, watermarked_data,
                         end_time - start_time)

        return watermarked_data, result

    def extract(self, watermarked_data: np.ndarray[np.any, np.int64],
                threshold: int = 4, secret_key: str = '000'):
        original_data = watermarked_data.copy()
        secret_data = ''

        for phase in reversed(range(1, 4)):
            if secret_key[phase - 1] == '0':
                continue

            for i in reversed(self.get_phase_indexes(phase, len(original_data))):
                if i + 4 >= len(original_data):
                    continue

                # Get error from predicted value and watermarked value
                watermarked_value = original_data[i+2]
                predicted_value = int(self.model.predict(
                    [[original_data[i], original_data[i+1], original_data[i+3], original_data[i+4]]]))
                error_extraction = watermarked_value - predicted_value

                # Check threshold
                if error_extraction >= 2*threshold:
                    original_value = watermarked_value - threshold
                elif error_extraction <= -2*threshold + 1:
                    original_value = watermarked_value + threshold - 1
                else:
                    # Extract the watermark bit
                    bit = error_extraction - 2 * \
                        math.floor(error_extraction / 2)

                    # Get the original value
                    original_value = watermarked_value - \
                        math.floor(error_extraction / 2) - bit
                    secret_data = ('1' if bit else '0') + secret_data

                # if (i + 2 == 8):
                #     print('Index', i+2, 'Original', original_value, 'Predicted', predicted_value,
                #           'Error Ext', error_extraction, 'Bit', bit, 'Watermark', watermarked_value)

                # Repack the ECG and secret data
                original_data[i+2] = original_value

            print(original_data[0: 10])
        return original_data, secret_data

    def get_phase_indexes(self, phase: Literal[1, 2, 3], max_len: int = 3_600):
        """
        Memberikan range untuk fase ke-x dengan panjang maksimal ke-sekian
        """
        return range(phase - 1, max_len, 3)
