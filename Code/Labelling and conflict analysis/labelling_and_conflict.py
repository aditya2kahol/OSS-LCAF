import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import BitsAndBytesConfig
from huggingface_hub import login
import json
import pandas as pd
from itertools import combinations
import os
from fuzzywuzzy import process
from license_match import *
from prompts import *

token = "<hugging_face_token>"

login(token=token)

torch.random.manual_seed(0)


labelling_DIR = '<output_path_for_labelled_licenses>/<file_name>.xlsx'
conflict_DIR = '<output_path_for_conflict_analysis>/<file_name>.xlsx'

def extract_first_json(text):
    start = text.find('{')
    if start == -1:
        return None

    bracket_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            bracket_count += 1
        elif text[i] == '}':
            bracket_count -= 1

        if bracket_count == 0:
            return text[start:i+1]
    
    return None

def load_spdx_identifiers(file_path):
    df = pd.read_excel(file_path)
    return df['Ref license'].tolist()


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

file_path = "Knowledgebase for Referenced licenses.xlsx"
spdx_df = pd.read_excel(file_path)
spdx_identifiers = load_spdx_identifiers(file_path)

data = pd.read_excel('<path_to_licenses_output_of_license_extraction_module>')

model_id = "meta-llama/Llama-3.1-8B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto", 
    torch_dtype="auto", 
    trust_remote_code=True, 
    #quantization_config=quantization_config
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 4000,
    "return_full_text": False,
    "temperature": 0.9,
    "do_sample": False,
}

classes = {
    "Distribute": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether distribution is allowed."
    },
    "Modify": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether modification is allowed."
    },
    "Commercial Use": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether commercial use is allowed."
    },
    "Relicense": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether re-licensing is permitted."
    },
    "Hold Liable": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether holding contributors liable is allowed."
    },
    "Use Patent": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether using patent claims is allowed."
    },
    "Sublicense": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether sublicensing is allowed."
    },
    "Statically Link": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of static linking in the license text."
    },
    "Private Use": {
        "label": "NOT MENTIONED",
        "reasoning": "No information is available to determine whether private use is allowed."
    },
    "Use Trademark": {
        "label": "NOT MENTIONED",
        "reasoning": "The text does not mention any rights related to trademarks."
    },
    "Place Warranty": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of placing a warranty on the licensed software."
    },
    "Include Copyright": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of retaining the copyright notice in copies or substantial uses."
    },
    "Include License": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of including license when distributing."
    },
    "Include Notice": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of including notice when distributing."
    },
    "Disclose Source": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of a requirement to disclose source code."
    },
    "State Changes": {
        "label": "NOT MENTIONED",
        "reasoning": "The license does not specify any obligation to state changes made to the software."
    },
    "Include Original": {
        "label": "NOT MENTIONED",
        "reasoning": "The text does not address whether the original software must be included."
    },
    "Give Credit": {
        "label": "NOT MENTIONED",
        "reasoning": "The requirement to give credit to the author is not mentioned in the license."
    },
    "Rename Change": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no reference to changing the software name to avoid misrepresentation."
    },
    "Contact Author": {
        "label": "NOT MENTIONED",
        "reasoning": "The text does not require contacting the author."
    },
    "Include Install Instructions": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of including installation instructions."
    },
    "Compensate for Damages": {
        "label": "NOT MENTIONED",
        "reasoning": "There is no mention of obligation to compensate the contributors for damages."
    },
    "Pay Above Use Threshold": {
        "label": "NOT MENTIONED",
        "reasoning": "The document does not specify any payment requirements after a certain amount of use."
    }
}

def labelling(data):
    license_text = list(data['License text'])
    labels = []
    for i in range(len(license_text)):
        output = None
        print('===================================================================================')
        try:
            text = None
            if data.iloc[i]['License type'] == 'Referenced':
                extracted_identifiers = [license_text[i]]
                matches, scores = find_best_matches(extracted_identifiers, spdx_identifiers)
                for extracted, match in matches.items():
                    if match:
                        results = spdx_df.loc[spdx_df['Ref license'] == match, 'License text']
                        result = results.iloc[0]
                        if result:
                            text = result
                        else:
                            text = license_text[i]
                        print("found a match for referenced license......")
                    else:
                        text = license_text[i]
            if text:
                if len(text) > 20000:
                    check = True
                else:
                    check = False
                prompt = get_labelling_prompt(text, check)
            else:
                if len(license_text[i]) > 20000:
                    check = True
                else:
                    check = False
                prompt = get_labelling_prompt(license_text[i], check)
            
            if prompt:
                output = pipe(prompt, **generation_args)
                print('Before JSON - ', output[0]["generated_text"])
                json_output = json.loads(output[0]["generated_text"])
                labels.append(output[0]["generated_text"])
            else:
                labels.append(json.dumps(classes))
        except Exception as e:
            print('something went wrong in classification - ', str(e))
            try:
                first_json = extract_first_json(output[0]["generated_text"])
                if first_json:
                    first_json_value = first_json
                    print("Labels in output - ", first_json_value)
                    if 'Distribute' in first_json_value:
                        labels.append(first_json_value)
                    else:
                        print("classification - ",classes)
                        labels.append(json.dumps(classes))
                else:
                    print("classification - ",classes)
                    labels.append(json.dumps(classes))        
            except Exception as e:
                print("classification - ",classes)
                labels.append(json.dumps(classes))
        
        if output:
            del output
        torch.cuda.empty_cache()
        gpu_id = torch.cuda.current_device()
        gpu_memory = torch.cuda.get_device_properties(gpu_id).total_memory
        gpu_memory_allocated = torch.cuda.memory_allocated(gpu_id)
        gpu_memory_free = gpu_memory - gpu_memory_allocated

        print(f"Available GPU Memory: {gpu_memory_free // (1024 ** 2)} MB")
        print('=========================================================================================')


    data['labels'] = labels

    data.to_excel(labelling_DIR, index = False)

    return True

def conflict_analysis(labelled_data):
    print("====================================conflict analysis starts========================================")
    repository_name = []
    path_1 = []
    path_2 = []
    license_text_1 = []
    labels_1 = []
    license_text_2 = []
    labels_2 = []
    conflict_details = []

    grouped = labelled_data.groupby('Repository name')

    for repo_name, group in grouped:
        # If there's only one license in the repository, handle it accordingly
        if len(group) < 2:
            single_row = group.iloc[0]
            repository_name.append(repo_name)
            path_1.append(single_row['Repository path'])
            path_2.append('')
            license_text_1.append(single_row['License text'])
            labels_1.append(single_row['labels'])
            license_text_2.append('')
            labels_2.append('')
            conflict_details.append("No conflict present here as there is only one license in the project.")
            continue

        for (index1, row1), (index2, row2) in combinations(group.iterrows(), 2):
            print("========================================================================================")
            license_1 = row1['License text']
            label_1 = row1['labels']
            license_2 = row2['License text']
            label_2 = row2['labels']

            try:
                if main(license_1, license_2):
                    print('Both licenses are of same kind')
                    continue
            except Exception as e:
                print("cannot check if both are same licenses or not, so skipping this step.")
                print("Reason is - ", str(e))

            if len(license_1.strip()) > 100 and len(license_2.strip()) > 100 :
                if license_1.strip()[-50:] == license_2.strip()[-50:0]:
                    print("We are having two same licenses in checking for conflict analysis and hence we are skipping this.")
                    continue
            prompt = get_conflict_prompt(label_1, label_2)
            output = pipe(prompt, **generation_args)
            print('Before JSON - ', output[0]["generated_text"])
            try:
                json_output = json.loads(output[0]['generated_text'])
                json_output = output[0]["generated_text"]
                print("Succesfully got json conflict output")
            except Exception as e:
                print("something went wrong in conflict analysis - ", str(e))
                json_output = extract_first_json(output[0]["generated_text"])
                if json_output == None:
                    json_output = "We could not detect conflict between these 2 licenses, Please check them manually."
                
            repository_name.append(repo_name)
            path_1.append(row1['Repository path'])
            path_2.append(row2['Repository path'])
            license_text_1.append(license_1)
            labels_1.append(label_1)
            license_text_2.append(license_2)
            labels_2.append(label_2)
            conflict_details.append(json_output)

            del output
            torch.cuda.empty_cache()
            gpu_id = torch.cuda.current_device()
            gpu_memory = torch.cuda.get_device_properties(gpu_id).total_memory
            gpu_memory_allocated = torch.cuda.memory_allocated(gpu_id)
            gpu_memory_free = gpu_memory - gpu_memory_allocated
            print(f"Available GPU Memory: {gpu_memory_free // (1024 ** 2)} MB")
            print('=========================================================================================')



    conflict_df = pd.DataFrame({
        'Repository Name': repository_name,
        'File path 1': path_1,
        'File path 2': path_2,
        'License Text 1': license_text_1,
        'Label 1': labels_1,
        'License Text 2': license_text_2,
        'Label 2': labels_2,
        'Conflict Details': conflict_details
    })

    conflict_df.to_excel(conflict_DIR, index= False)

    return True

def Write_to_text(df):
    repo_counts = {}  
    for index, row in df.iterrows():
        # Folder to save text files
        output_folder = f"<path_to_output_directory>/{row['Repository Name']}"
        os.makedirs(output_folder, exist_ok=True)

        if output_folder not in repo_counts:
            repo_counts[output_folder] = 1
        else:
            repo_counts[output_folder] += 1

        file_name = f"Report {repo_counts[output_folder]}.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, 'w') as f:
            f.write(f"Project Name - {row['Repository Name']}\n\n")
            f.write(f"File path 1 - {row['File path 1']}\n\n")
            #f.write(f"License 1 - {row['License Text 1']}\n\n")
            f.write(f"File path 2 - {row['File path 2']}\n\n")
            #f.write(f"License 2 - {row['License Text 2']}\n\n")
            
            f.write("Conflict Analysis:\n\n")
            
            conflict_details = row['Conflict Details']

            if "No conflict present here as there is only one license in the project." in conflict_details:
                f.write("No conflict present here as there is only one license in the project.\n")
                continue

            try:
                conflict_json = json.loads(conflict_details)
                for key, value in conflict_json.items():
                    f.write(f"{key} - {value}\n")
            except json.JSONDecodeError:
                f.write("Please check the conflict manually.\n")

            f.write("Summary:\n\n")
            
            try:
                prompt = get_conclusion_prompt(conflict_details)
                output = pipe(prompt, **generation_args)
                f.write(output[0]["generated_text"])

            except Exception as e:
                print("could not get conclusion - ", str(e))
                f.write("Please check the conflict manually.\n")
        

    print("Text files have been created.")
    
def main(data):
    try:
        labels_status = labelling(data)
    except Exception as e:
        print("something went wrong in labelling process - ", str(e))
    
    
    if labels_status:
        try:
            labelled_data = pd.read_excel(labelling_DIR)
            conflict_status = conflict_analysis(labelled_data)
        except Exception as e:
            print("something went wrong in conflict analysis - ", str(e))
    
    if conflict_status:
        print("Conflicts saved to excel in path")
        df = pd.read_excel(conflict_DIR)
        Write_to_text(df)

if __name__==__main__:
    main(data)
