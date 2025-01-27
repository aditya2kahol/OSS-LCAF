# Extract inline licenses

import os
import re
import utils
import pandas as pd
from typing import List

def extract_comments_from_repo(repo_path: str):
    # Define patterns for different types of multi-line comments
    patterns = {
        '.py': r'\'\'\'(.*?)\'\'\'|"""(.*?)"""',  # Python triple-quoted strings
        '.cpp': r'/\*(.*?)\*/',  # C++ multi-line comments
        '.c': r'/\*(.*?)\*/',  # C multi-line comments
        '.h': r'/\*(.*?)\*/',  # C/C++ header files multi-line comments
        '.java': r'/\*(.*?)\*/',  # Java multi-line comments
        '.js': r'/\*(.*?)\*/',  # JavaScript multi-line comments
        '.ts': r'/\*(.*?)\*/',  # TypeScript multi-line comments
        '.html': r'<!--(.*?)-->',  # HTML multi-line comments
        '.css': r'/\*(.*?)\*/'  # CSS multi-line comments
    }
    
    # Function to extract comments with keywords from a single file's content
    def extract_comments(file_content, ext):
        # Get the pattern for the current file extension
        if ext in patterns:
            combined_pattern = patterns[ext]
            # Perform the search using re.DOTALL to allow newlines in matches
            matches = re.findall(combined_pattern, file_content, re.DOTALL | re.IGNORECASE)
            # Filter matches containing the keywords 'copyright' or 'agreement'
            filtered_comments = []
            for match in matches:
                # 'match' is a tuple of matches from different patterns
                if isinstance(match, tuple):
                    for comment in match:
                        if comment and re.search(r'copyright\b|agreement\b', comment, re.IGNORECASE):
                            if re.search(r'permission\b|grant\b|modify\b|warranty\b', comment, re.IGNORECASE):
                                filtered_comments.append(comment.strip())
                else:
                    if match and re.search(r'copyright\b|agreement\b', match, re.IGNORECASE):
                        if re.search(r'permission\b|grant\b|modify\b|warranty\b', match, re.IGNORECASE):
                            filtered_comments.append(match.strip())
            return filtered_comments
        return []
    
    # Dictionary to hold all extracted comments by file
    extracted_comments = dict()
    
    # Walk through the directory
    for root, _, files in os.walk(repo_path):
        for file in files:
            ext = os.path.splitext(file)[1]  # Get the file extension
            if ext in patterns:
                # Build the full file path
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and os.path.getsize(file_path) > 0: # Checks if the file exists and is not empty
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                        comments = extract_comments(file_content, ext)
                        if comments:
                            print(f"Inline License found at: {file_path}....")
                            extracted_comments[file_path] = comments
    
    return extracted_comments

def get_inline_license_dict(repo_paths:List)->dict:
    # repo_paths: ["<path_to_your_directory>/<repo_name>",...]
    license_dict = {'Repository name':[],
                    'Repository path':[],
                    'License text':[],
                    'License type':[]}
    
    for repo_path in repo_paths:
        inline_license_dict = extract_comments_from_repo(repo_path)
        
        for file_path, comments in inline_license_dict.items():
            for comment in comments:
                license_dict['Repository name'].append(repo_path.split('/')[-1])
                license_dict['Repository path'].append(file_path)
                license_dict['License text'].append(comment)
                license_dict['License type'].append('Inline')

    return license_dict


if __name__=='__main__':
    print("Nothing to see here!")
