# Labelling and Conflict Analysis

## How to Use

- Install dependencies listed in `pip install -r requirements.txt`.
- Provide your Hugging Face token in the `token` variable of the `labelling_and_conflict.py` script.
- Update the following paths in the `labelling_and_conflict.py` script:
  - `labelling_DIR`: path to the directory to store labelled data.
  - `conflict_DIR`: Path to the directory for storing conflict analysis excel results.
  - `data`: Path to the data file or directory containing the license data from license extraction module.
  - `output_folder`: path to store reports(txt) of each combination of licenses in conflict analsis.
- Run `python labelling_and_conflict.py`

## `labelling_and_conflict.py`

This script contains two primary modules of the framework:

### 1. License Term Labeller
- **Purpose**: This module labels the licenses extracted from the license extraction module.
- **Output**: An Excel (`.xlsx`) file that includes a "labels" column containing labelled information for each license.

### 2. Conflict Analysis
- **Purpose**: This module performs conflict analysis on all combinations of licenses produced by the License Term Labeller.
- **Output**: 
  - An Excel (`.xlsx`) file with the conflict analysis results for all combinations of licenses.
  - A `.txt` file for each combination, providing a detailed report and summary of the conflict between the respective licenses.
