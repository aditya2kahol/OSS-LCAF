## License Extraction

## How to Use
- Install dependencies listed in `pip install -r requirements.txt`.

- Update the following paths in the `main.py` script:
	- BASE_FILE_PATH: Path to the folder containing all the repositories for which you wish to extract the licenses.
	- BASE_SAVE_FILE_PATH: Path to save all the extracted licenses from the repositories.

- Update the following path in the `utils.py` script:
	- BASE_FILE_PATH: Path to download (clone) random repositories from GitHub.
	Note: The functions 'fetch_top_repositories` and 'clone_repos' in utils.py were used to build the benchmark dataset, hence will not be of any use in-case the user wishes to use the modules for license extraction and conflict analysis.

- run `python main.py`

## main.py
This script primarily uses 4 modules: utils.py, declared_license.py, inline_license.py and referenced_license.py.

- declared_license.py 
	- *Purpose*: used to extract all the declared licenses.
	- *Output*: Returns all the declared licenses in the form of a dictionary
- inline_license.py
	- *Purpose*: used to extract all the inline licenses.
	- *Output*: Returns all the inline licenses in the form of a dictionary
- referenced_license.py
	- *Purpose*: used to extract all the referenced licenses.
	- *Output*: Returns all the referenced licenses in the form of a dictionary

*Final Output*: A .xlsx file (stored in BASE_SAVE_FILE_PATH) containing with 4 columns:
	- Repository name: contains the name of the repository
	- Repository path: Path from where the license was extracted from the repository
	- License text: The string containing the License
	- License type: Whether it is Declared, Inline or Referenced.
