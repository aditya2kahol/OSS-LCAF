import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import re

def load_spdx_identifiers(file_path):
    df = pd.read_excel(file_path)
    return df['Ref license'].tolist()

file_path = "Knowledgebase for Referenced licenses.xlsx"
spdx_df = pd.read_excel(file_path)
spdx_identifiers = load_spdx_identifiers(file_path)



def normalize_identifier(identifier):
    return identifier.lower().strip()

def find_best_matches(extracted_identifiers, spdx_identifiers, threshold=80):
    matches = {}
    scores = []
    for identifier in extracted_identifiers:
        normalized_id = normalize_identifier(identifier)
        best_match, score = process.extractOne(normalized_id, spdx_identifiers)
        scores.append(score)
        if score >= threshold:
            matches[identifier] = best_match
        else:
            matches[identifier] = None 
    return matches, scores

def get_license_from_knowledgebase(license_text):
    extracted_identifiers = [license_text]
    #print(extracted_identifiers)
    matches, scores = find_best_matches(extracted_identifiers, spdx_identifiers)
    for extracted, match in matches.items():
        print("match - ", match)
        if match:
            results = spdx_df.loc[spdx_df['Ref license'] == match, 'License text']
            result = results.iloc[0]
            print(result)
            return result
        else:
            return license_text

def normalize_license_texts(texts):
    return re.sub(r'\s+', ' ', texts).strip()

def compare_license_texts(license_text_1, license_text_2):
    license_text_1 = normalize_license_texts(license_text_1)
    license_text_2 = normalize_license_texts(license_text_2)
    score = fuzz.partial_ratio(license_text_1, license_text_2)
    print(f"Fuzzy matching score: {score}")
    if score > 90:
        return True
    else:
        return False


def main(license_1, license_2):
    license_1 = get_license_from_knowledgebase(str(license_1))
    license_2 = get_license_from_knowledgebase(str(license_2))

    #print("License 1 used for comparison - ",license_1)
    #print("License 2 used for comparison - ",license_2)

    result = compare_license_texts(license_1, license_2)
    return result
