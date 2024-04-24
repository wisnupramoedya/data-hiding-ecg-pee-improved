import unittest
import numpy as np
from utils.calculation import Calculation


class TestCalculation(unittest.TestCase):
    def test_calculate_prd(self):
        # Example signals (you can replace these with your own data)
        original_signal = np.array([1.0, 2.0, 3.0, 4.0])
        reconstructed_signal = np.array([1.1, 2.1, 3.2, 4.3])

        expected_prd = 7.071067812  # Calculated manually
        actual_prd = Calculation.prd(original_signal, reconstructed_signal)

        # Check if the calculated PRD is approximately equal to the expected value
        self.assertAlmostEqual(actual_prd, expected_prd, places=6)

    def test_calculate_ncc(self):
        # Example signals (you can replace these with your own data)
        original_signal = np.array([1.0, 2.0, 3.0, 4.0])
        reconstructed_signal = np.array([1.1, 2.1, 3.2, 4.3])

        expected_ncc = 0.99973807132  # Calculated manually
        actual_ncc = Calculation.ncc(original_signal, reconstructed_signal)

        # Check if the calculated NCC is approximately equal to the expected value
        self.assertAlmostEqual(actual_ncc, expected_ncc, places=6)

    def test_calculate_snr(self):
        # Example signals (you can replace these with your own data)
        original_signal = np.array([1.0, 2.0, 3.0, 4.0])
        reconstructed_signal = np.array([1.1, 2.1, 3.2, 4.3])

        expected_snr = 23.01029995663  # Calculated manually
        actual_snr = Calculation.snr(original_signal, reconstructed_signal)

        # Check if the calculated SNR is approximately equal to the expected value
        self.assertAlmostEqual(actual_snr, expected_snr, places=6)


if __name__ == "__main__":
    unittest.main()
