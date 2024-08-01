# Improved ECG PEE Steganography
## Overview
Improved ECG PEE Steganography is a project designed to embed secret messages within media electrocardiogram (ECG) using various innovative techniques. This project provides multiple versions of steganography implementations, each with its unique method for embedding and extracting hidden information, such as machine learning regression, etc. The project supports multiple versions with improved features to enhance security and efficiency. This project is developed as final thesis project.

## Getting Started
### Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system.
- A valid API token from a Telegram bot for message handling.
- Necessary Python packages listed in `requirements.txt`.

### Installation
Follow these steps to set up the project:
1. Clone the repository:

```bash
git clone https://github.com/wisnupramoedya/data-hiding-ecg-pee-improved
cd improved-pee-steganography
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Configure the Telegram Bot API:
  - Copy `utils/token.py.example` to `utils/token.py`.
  - Open `utils/token.py` and replace the placeholder with your actual Telegram bot API token.

4. Download the database [MIT-BIH](https://physionet.org/content/mitdb/1.0.0/) and place the extracted data on folder `data`

### Running the Code
To execute the steganography implementation, run the corresponding Jupyter Notebook file with format `stego_v{version}_{test/trial}.ipynb`

Replace `{version}` with the version number you wish to use and `{test/trial}` with the appropriate label for your testing or trial session.

## Code Reference
The project is divided into several versions, each introducing new features and improvements.

### Version 1 (v1)
- Utilizes a key-based steganography approach.
- The key ensures that only authorized users can extract the hidden message.

### Version 2 (v2)
- Builds upon v1 by adding a stopper point with an inverse key.
- Enhances security by introducing a stopping mechanism for incorrect keys.

### Version 3 (v3)
- Introduces mirror embedding system.
- Offers a more sophisticated method of embedding data within ECG.
- For academic purposes, please cite the following reference:

```
@article{2024,
  volume = {17},
  ISSN = {2185-3118},
  url = {http://dx.doi.org/10.22266/ijies2024.0831.85},
  DOI = {10.22266/ijies2024.0831.85},
  number = {4},
  journal = {International Journal of Intelligent Engineering and Systems},
  publisher = {The Intelligent Networks and Systems Society},
  year = {2024},
  month = aug,
  pages = {1146–1155}
}
```

### Version 4 (v4)
- Implements a middle mirror embedding system.
- Further refines the embedding technique for better performance and security.

## Testing
To ensure the integrity and functionality of the project, unit tests are included. You can run the unit tests using the following command:

```bash
python -m unittest discover -s tests -p '*_test.py'
```

## Contact
If you have any questions or suggestions, please feel free to contact the project maintainer at wisnupramoedya@gmail.com.