import os
import utils
import pandas as pd
from declared_license import extract_declared_licenses
from inline_license import get_inline_license_dict
from referenced_license import get_referenced_license_dict

BASE_FILE_PATH = '<path_to_your_repositories_directory>'
BASE_SAVE_FILE_PATH = '<path_to_your_output_directory>'

class DatasetBuilder:
    def __init__(self, root_path:str=None):
        self.ROOT = root_path
        if root_path:
            self.repository_paths = [self.ROOT + repo_name for repo_name in os.listdir(self.ROOT)]

    def fetch_and_clone(self, num_links, page_num):
        repository_links = utils.fetch_top_repositories(num_links=num_links, page_num=page_num, run=True)
        utils.clone_repos(repos=repository_links, run=True)
    
    def get_declared_licenses(self):
        print("\n\nExtracting Declared Licenses...\n\n")
        declared_license_dict = extract_declared_licenses(self.repository_paths)
        return declared_license_dict
    
    def get_inline_licenses(self):
        print("\n\nExtracting Inline Licenses...\n\n")
        inline_license_dict = get_inline_license_dict(self.repository_paths)
        return inline_license_dict

    def get_referenced_licenses(self):
        print("\n\nExtracting Referenced Licenses...\n\n")
        referenced_license_dict = get_referenced_license_dict(self.repository_paths)
        return referenced_license_dict
    
    @staticmethod
    def remove_extra_lines(text:str):
        while True:
            new_text = text.replace('\n\n','\n')
            if new_text == text:
                break
            else:
                text = new_text
        return new_text
    
    @staticmethod
    def clean_dataframe(df, col1, col2):
        df[col1] = df[col1].apply(lambda row: str(row))
        df[col2] = df[col2].apply(lambda row: str(row))
        try:
            df[col1] = df[col1].apply(lambda row: DatasetBuilder.remove_extra_lines(row))
            df[col1] = df[col1].apply(lambda row: utils.remove_spaces(row))
        except:
            pass
        try:
            df.drop_duplicates(subset=[col1,col2], inplace=True, ignore_index=True, keep='first')
        except:
            pass
        return df
    
    @staticmethod
    def check_text(text):
        # Check if any of the words 'copyright', 'permission', or 'grant' appear in the text
        keywords_true = ['copyright', 'permission', 'grant', 'license']
        if any(word in text.lower() for word in keywords_true):
            return text
        else:
            return None
    
    @staticmethod
    def remove_invalid_rows(df):
        """
        This function removes any rows from a DataFrame where the value in column 'License text' 
        is None, an empty string, or NaN. The function returns a new DataFrame with
        the filtered rows, without modifying the original DataFrame.
        """
        # Create a mask for valid values (i.e., not None, NaN, or empty string)
        mask = df['License text'].notna() & (df['License text'] != '')
        # Return a new DataFrame with only valid rows
        return df[mask].copy()

    def save_files(self, Declared:bool=False, Inline:bool=False, Referenced:bool=False, file_version:str=''):
        if Declared:
            declared_license_dict = self.get_declared_licenses()
            df = pd.DataFrame(declared_license_dict)
            df = DatasetBuilder.clean_dataframe(df, 'License text', 'Repository name')
            df['License text'] = df['License text'].apply(lambda row: DatasetBuilder.check_text(row))
            df = DatasetBuilder.remove_invalid_rows(df)
            df.to_excel(BASE_SAVE_FILE_PATH+'Declared Licenses'+file_version+'.xlsx', index=False, engine='xlsxwriter')
            print("Declared Licenses are saved!")
        elif Inline:
            inline_license_dict = self.get_inline_licenses()
            df = pd.DataFrame(inline_license_dict)
            df = DatasetBuilder.clean_dataframe(df, 'License text', 'Repository name')
            df = DatasetBuilder.remove_invalid_rows(df)
            df.to_excel(BASE_SAVE_FILE_PATH+'Inline Licenses'+file_version+'.xlsx', index=False, engine='xlsxwriter')
            print("Inline Licenses are saved!")
        elif Referenced:
            referenced_license_dict = self.get_referenced_licenses()
            df = pd.DataFrame(referenced_license_dict)
            print("Done with creating the dataframe.")
            df = DatasetBuilder.clean_dataframe(df, 'License text', 'Repository name')
            df = DatasetBuilder.remove_invalid_rows(df)
            print("Done with cleaning the dataframe.")
            try:
                df.to_excel(BASE_SAVE_FILE_PATH+'Referenced Licenses'+file_version+'.xlsx', index=False, engine='openpyxl')
                print("Done with saving the file in excel format.")
            except:
                df.to_csv(BASE_SAVE_FILE_PATH+'Referenced Licenses'+file_version+'.csv', index=False)
                print("Done with saving the file in csv format.")
            print("Referenced Licenses are saved!")
        else:
            # Extract all the licenses.
            declared_df = pd.DataFrame(self.get_declared_licenses())
            inline_df = pd.DataFrame(self.get_inline_licenses())
            referenced_df = pd.DataFrame(self.get_referenced_licenses())
            declared_df['License text'] = declared_df['License text'].apply(lambda row: DatasetBuilder.check_text(row))
            
            df = pd.concat([declared_df, inline_df, referenced_df], axis=0, ignore_index=True)
            df = DatasetBuilder.clean_dataframe(df, 'License text', 'Repository name')
            df = DatasetBuilder.remove_invalid_rows(df)
            df.to_excel(BASE_SAVE_FILE_PATH+'Complete License Data'+file_version+'.xlsx', index=False, engine='xlsxwriter')
            print("File saved!")


if __name__=='__main__':
    class_object = DatasetBuilder(BASE_FILE_PATH)
    class_object.save_files(file_version='_v1') 
