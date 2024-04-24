import numpy as np


class Calculation:
    @staticmethod
    def prd(original_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Calculate the Percentage Residual Difference (PRD) between original and reconstructed signals.

        Parameters:
        - original_signal (numpy.ndarray): The original signal.
        - reconstructed_signal (numpy.ndarray): The reconstructed signal.

        Returns:
        float: The PRD value in percentage.
        """
        diff = original_signal - reconstructed_signal
        numerator = np.linalg.norm(diff)
        denominator = np.linalg.norm(original_signal)
        prd = (numerator / denominator) * 100
        return prd

    @staticmethod
    def ncc(original_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Calculate the Normalized Cross-Correlation (NCC) between original and reconstructed signals.

        Parameters:
        - original_signal (numpy.ndarray): The original signal.
        - reconstructed_signal (numpy.ndarray): The reconstructed signal.

        Returns:
        float: The NCC value.
        """
        mean_original_signal = np.mean(original_signal)
        mean_reconstructed_signal = np.mean(reconstructed_signal)
        numerator = np.sum((original_signal - mean_original_signal)
                           * (reconstructed_signal - mean_reconstructed_signal))
        denominator = np.sqrt(np.sum((original_signal - mean_original_signal) ** 2)
                              * np.sum((reconstructed_signal - mean_reconstructed_signal) ** 2))
        ncc = numerator / denominator
        return ncc

    @staticmethod
    def snr(original_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Calculate the Signal-to-Noise Ratio (SNR) between original and reconstructed signals.

        Parameters:
        - original_signal (numpy.ndarray): The original signal.
        - reconstructed_signal (numpy.ndarray): The reconstructed signal.

        Returns:
        float: The SNR value in decibels.
        """
        signal_power = np.sum(original_signal ** 2)
        noise_power = np.sum((original_signal - reconstructed_signal) ** 2)
        snr = 10 * np.log10(signal_power / noise_power)
        return snr

    @staticmethod
    def psnr(original_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Calculate the Peak Signal-to-Noise Ratio (SNR) between original and reconstructed signals.

        Parameters:
        - original_signal (numpy.ndarray): The original signal.
        - reconstructed_signal (numpy.ndarray): The reconstructed signal.

        Returns:
        float: The PSNR value in decibels.
        """
        max_value = np.max(
            [np.max(original_signal), np.max(reconstructed_signal)])
        mse = np.mean((original_signal - reconstructed_signal) ** 2)
        if mse == 0:
            return 100  # Jika MSE nol, artinya tidak ada noise pada sinyal.
        psnr = 10 * np.log10(max_value**2 / mse)
        return psnr / 2
