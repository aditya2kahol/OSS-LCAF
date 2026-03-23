def get_labelling_prompt(query_license, check_20k):
    if check_20k:
        if "GNU GENERAL PUBLIC LICENSE" in query_license:
            text = 'GNU GENERAL PUBLIC LICENSE'

        elif "GNU AFFERO GENERAL PUBLIC LICENSE" in query_license:
            text = 'GNU AFFERO GENERAL PUBLIC LICENSE'
        else:
            text = None
        
        if text:
            messages = [
                {
                    "role": "system",
                    "content": '''
                    As an experienced legal assistant in the software industry, you must analyse the provided license text. Your output should be in a nested JSON format which consists of outer and inner keys. Note that the outer keys contain the permissions, and the inner-keys consists of (a) label and (b) reasoning. You must assign an appropriate label for the license statement given at the end, and a short step-by-step rationale for the reasoning key. Avoid any assumptions or interpretations beyond the text. Ignore any kind of text in input license text that doesn't mean like a license. Use the following outer and inner keys.```json{  "Distribute": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Modify": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Commercial Use": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Relicense": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Hold Liable": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Use Patent": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Sublicense": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Statically Link": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Private Use": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Use Trademark": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Place Warranty": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Copyright": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include License": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Notice": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Disclose Source": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "State Changes": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Original": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Give Credit": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Rename Change": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Contact Author": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Install Instructions": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Compensate for Damages": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Pay Above Use Threshold": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  }}
                    '''
                },
                {
                    "role" : "user",
                    "content": f'''License statement:```f{text}```'''
                }
                
            ]
            return messages
        else:
            return None
    
    messages = [
        {
            "role": "system",
            "content": '''
            You are a knowledgeable legal assistant. Your task is to analyze a given license document and assign appropriate labels in JSON format based solely on the text provided. For each right and obligation, you should also provide a brief explanation of your reasoning for the assigned label. Avoid any assumptions or interpretations beyond the text. Ignore any kind of text in input license text that doesn't mean like a license. For each of the following rights and obligations, please use the specified key values in the JSON output:
            ```
            1. Distribute  
                - Description: Distribute original or modified derivative works  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            2. Modify  
                - Description: Modify the software and create derivatives  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            3. Commercial Use  
                - Description: Use the software for commercial purposes  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            4. Relicense  
                - Description: Add other licenses to the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            5. Hold Liable  
                - Description: Hold the author responsible for subsequent impacts  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            6. Use Patent  
                - Description: Practice patent claims of contributors  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            7. Sublicense  
                - Description: Incorporate the work into something with a more restrictive license  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            8. Statically Link  
                - Description: Compile the library into the program linked at compile time  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            9. Private Use  
                - Description: Use or modify software freely without distribution  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            10. Use Trademark  
                - Description: Use contributors’ names, trademarks, or logos  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            11. Place Warranty  
                - Description: Place a warranty on the licensed software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            12. Include Copyright  
                - Description: Retain the copyright notice in copies or substantial uses  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            13. Include License  
                - Description: Include the full text of the license in modified software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            14. Include Notice  
                - Description: Include a NOTICE when distributing if present  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            15. Disclose Source  
                - Description: Disclose your source code when distributing the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            16. State Changes  
                - Description: State significant changes made to the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            17. Include Original  
                - Description: Distribute copies of the original software or provide instructions to obtain copies  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            18. Give Credit  
                - Description: Give explicit credit to the author with the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            19. Rename Change  
                - Description: Change the software name to avoid misrepresentation  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            20. Contact Author  
                - Description: Obtain permission or contact the author about the module used  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            21. Include Install Instructions  
                - Description: Include necessary installation information  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            22. Compensate for Damages  
                - Description: Compensate the author for damages caused by your work  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            23. Pay Above Use Threshold  
                - Description: Pay the licensor after a certain amount of use  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            ```
            **Note:** If any information regarding a field is not mentioned in the document, label it as "NOT MENTIONED."

            '''
        },
        {
            "role": "user",
            "content": '''
            ### Input License text -
            Board minutes SPDX short identifier: BlueOak-1.0.0 Link to license steward's version Version 1.0.0 Purpose This license gives everyone as much permission to work with this software as possible, while protecting contributors from liability. Acceptance In order to receive this license, you must agree to its rules.  The rules of this license are both obligations under that agreement and conditions to your license. You must not do anything with this software that triggers a rule that you cannot or will not follow. Copyright Each contributor licenses you to do everything with this software that would otherwise infringe that contributor’s copyright in it. Notices You must ensure that everyone who gets a copy of any part of this software from you, with or without changes, also gets the text of this license or a link to https://blueoakcouncil.org/license/1.0.0. Excuse If anyone notifies you in writing that you have not complied with [Notices](#notices), you can keep your license by taking all practical steps to comply within 30 days after the notice.  If you do not do so, your license ends immediately. Patent Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license. Reliability No contributor can revoke this license. No Liability As far as the law allows, this software comes as is, without any warranty or condition, and no contributor will be liable to anyone for any damages related to this software or this license, under any kind of legal claim. '''
        },
        {

            "role": "assistant",
            "content": ''' 
            {
                "Distribute": {
                    "label": "CAN",
                    "reasoning": "The license gives everyone permission to work with the software, which implies that distribution is allowed."
                },
                "Modify": {
                    "label": "CAN",
                    "reasoning": "The license states that each contributor licenses users to do everything with the software, including modifications."
                },
                "Commercial Use": {
                    "label": "CAN",
                    "reasoning": "The purpose of the license indicates that it grants maximum permission, which includes commercial use."
                },
                "Relicense": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The text does not specify whether re-licensing is permitted."
                },
                "Hold Liable": {
                    "label": "CANNOT",
                    "reasoning": "The license explicitly states that no contributor will be liable for damages related to the software."
                },
                "Use Patent": {
                    "label": "CAN",
                    "reasoning": "Each contributor licenses the use of any patent claims they can license, allowing this action."
                },
                "Sublicense": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The license does not address sublicensing."
                },
                "Statically Link": {
                    "label": "NOT MENTIONED",
                    "reasoning": "There is no mention of static linking in the license text."
                },
                "Private Use": {
                    "label": "CAN",
                    "reasoning": "The license allows users to work with the software freely, implying private use is permitted."
                },
                "Use Trademark": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The text does not mention any rights related to trademarks."
                },
                "Place Warranty": {
                    "label": "CANNOT",
                    "reasoning": "The license states that the software comes 'as is,' indicating no warranties can be placed."
                },
                "Include Copyright": {
                    "label": "MUST",
                    "reasoning": "The license requires that everyone who gets a copy also receives the license text, which implies retaining copyright notices."
                },
                "Include License": {
                    "label": "MUST",
                    "reasoning": "The text explicitly requires including the license text or a link when distributing the software."
                },
                "Include Notice": {
                    "label": "MUST",
                    "reasoning": "Notices must be included when distributing the software if they are present."
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
                    "label": "CANNOT",
                    "reasoning": "The license states no obligation to compensate contributors for damages."
                },
                "Pay Above Use Threshold": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The document does not specify any payment requirements after a certain amount of use."
                }
            }
            
            '''
        },
        {
            "role": "user",
            "content": f'''
            ### Input License text -
            {query_license} 
            '''
        }
    ]
    
    return messages


def get_gemma_labelling_prompt(query_license, check_20k):
    if check_20k:
        if "GNU GENERAL PUBLIC LICENSE" in query_license:
            text = 'GNU GENERAL PUBLIC LICENSE'

        elif "GNU AFFERO GENERAL PUBLIC LICENSE" in query_license:
            text = 'GNU AFFERO GENERAL PUBLIC LICENSE'
        else:
            text = None
        
        if text:
            messages = '''
                As an experienced legal assistant in the software industry, you must analyse the provided license text. Your output should be in a nested JSON format which consists of outer and inner keys. Note that the outer keys contain the permissions, and the inner-keys consists of (a) label and (b) reasoning. You must assign an appropriate label for the license statement given at the end, and a short step-by-step rationale for the reasoning key. Avoid any assumptions or interpretations beyond the text. Ignore any kind of text in input license text that doesn't mean like a license. Use the following outer and inner keys.```json{  "Distribute": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Modify": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Commercial Use": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Relicense": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Hold Liable": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Use Patent": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Sublicense": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Statically Link": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Private Use": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Use Trademark": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Place Warranty": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Copyright": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include License": {    "Label": "can be either CAN/CANNOT, MUST/NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Notice": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Disclose Source": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "State Changes": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Original": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Give Credit": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Rename Change": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Contact Author": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Include Install Instructions": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Compensate for Damages": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  },  "Pay Above Use Threshold": {    "Label": "can be either CAN, CANNOT, MUST, NO NEED or NOT MENTIONED",    "Reasoning": ""  }}```

            **Input:**
            f'License statement:```{text}```'
            
            **Output:**
            '''
            return messages
        else:
            return None
    
    messages = '''
            You are a knowledgeable legal assistant. Your task is to analyze a given license document and assign appropriate labels in JSON format based solely on the text provided. For each right and obligation, you should also provide a brief explanation of your reasoning for the assigned label. Avoid any assumptions or interpretations beyond the text. Ignore any kind of text in input license text that doesn't mean like a license. For each of the following rights and obligations, please use the specified key values in the JSON output:
            ```
            1. Distribute  
                - Description: Distribute original or modified derivative works  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            2. Modify  
                - Description: Modify the software and create derivatives  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            3. Commercial Use  
                - Description: Use the software for commercial purposes  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            4. Relicense  
                - Description: Add other licenses to the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            5. Hold Liable  
                - Description: Hold the author responsible for subsequent impacts  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            6. Use Patent  
                - Description: Practice patent claims of contributors  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            7. Sublicense  
                - Description: Incorporate the work into something with a more restrictive license  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            8. Statically Link  
                - Description: Compile the library into the program linked at compile time  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            9. Private Use  
                - Description: Use or modify software freely without distribution  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            10. Use Trademark  
                - Description: Use contributors’ names, trademarks, or logos  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            11. Place Warranty  
                - Description: Place a warranty on the licensed software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            12. Include Copyright  
                - Description: Retain the copyright notice in copies or substantial uses  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            13. Include License  
                - Description: Include the full text of the license in modified software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            14. Include Notice  
                - Description: Include a NOTICE when distributing if present  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            15. Disclose Source  
                - Description: Disclose your source code when distributing the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            16. State Changes  
                - Description: State significant changes made to the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            17. Include Original  
                - Description: Distribute copies of the original software or provide instructions to obtain copies  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            18. Give Credit  
                - Description: Give explicit credit to the author with the software  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            19. Rename Change  
                - Description: Change the software name to avoid misrepresentation  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            20. Contact Author  
                - Description: Obtain permission or contact the author about the module used  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            21. Include Install Instructions  
                - Description: Include necessary installation information  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            22. Compensate for Damages  
                - Description: Compensate the author for damages caused by your work  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            23. Pay Above Use Threshold  
                - Description: Pay the licensor after a certain amount of use  
                - Possible Labels: CAN, CANNOT, MUST, NO NEED
            ```
            **Note:** If any information regarding a field is not mentioned in the document, label it as "NOT MENTIONED."

        ### Examples:
        **Input:**
            ### Input License text -
            Board minutes SPDX short identifier: BlueOak-1.0.0 Link to license steward's version Version 1.0.0 Purpose This license gives everyone as much permission to work with this software as possible, while protecting contributors from liability. Acceptance In order to receive this license, you must agree to its rules.  The rules of this license are both obligations under that agreement and conditions to your license. You must not do anything with this software that triggers a rule that you cannot or will not follow. Copyright Each contributor licenses you to do everything with this software that would otherwise infringe that contributor’s copyright in it. Notices You must ensure that everyone who gets a copy of any part of this software from you, with or without changes, also gets the text of this license or a link to https://blueoakcouncil.org/license/1.0.0. Excuse If anyone notifies you in writing that you have not complied with [Notices](#notices), you can keep your license by taking all practical steps to comply within 30 days after the notice.  If you do not do so, your license ends immediately. Patent Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license. Reliability No contributor can revoke this license. No Liability As far as the law allows, this software comes as is, without any warranty or condition, and no contributor will be liable to anyone for any damages related to this software or this license, under any kind of legal claim.
        **Output:**
        ``` 
            {
                "Distribute": {
                    "label": "CAN",
                    "reasoning": "The license gives everyone permission to work with the software, which implies that distribution is allowed."
                },
                "Modify": {
                    "label": "CAN",
                    "reasoning": "The license states that each contributor licenses users to do everything with the software, including modifications."
                },
                "Commercial Use": {
                    "label": "CAN",
                    "reasoning": "The purpose of the license indicates that it grants maximum permission, which includes commercial use."
                },
                "Relicense": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The text does not specify whether re-licensing is permitted."
                },
                "Hold Liable": {
                    "label": "CANNOT",
                    "reasoning": "The license explicitly states that no contributor will be liable for damages related to the software."
                },
                "Use Patent": {
                    "label": "CAN",
                    "reasoning": "Each contributor licenses the use of any patent claims they can license, allowing this action."
                },
                "Sublicense": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The license does not address sublicensing."
                },
                "Statically Link": {
                    "label": "NOT MENTIONED",
                    "reasoning": "There is no mention of static linking in the license text."
                },
                "Private Use": {
                    "label": "CAN",
                    "reasoning": "The license allows users to work with the software freely, implying private use is permitted."
                },
                "Use Trademark": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The text does not mention any rights related to trademarks."
                },
                "Place Warranty": {
                    "label": "CANNOT",
                    "reasoning": "The license states that the software comes 'as is,' indicating no warranties can be placed."
                },
                "Include Copyright": {
                    "label": "MUST",
                    "reasoning": "The license requires that everyone who gets a copy also receives the license text, which implies retaining copyright notices."
                },
                "Include License": {
                    "label": "MUST",
                    "reasoning": "The text explicitly requires including the license text or a link when distributing the software."
                },
                "Include Notice": {
                    "label": "MUST",
                    "reasoning": "Notices must be included when distributing the software if they are present."
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
                    "label": "CANNOT",
                    "reasoning": "The license states no obligation to compensate contributors for damages."
                },
                "Pay Above Use Threshold": {
                    "label": "NOT MENTIONED",
                    "reasoning": "The document does not specify any payment requirements after a certain amount of use."
                }
            }
            
            ```
        
            **Input:**
            ### Input License text -
            f'{query_license}' 
            
            **Output:**
    '''
    
    return messages


def get_conflict_prompt(license1_json, license2_json):
  messages = [
      {
          "role": "system",
          "content": '''
          As a software licensing expert, analyze two sets of license permissions to identify conflicts in their rights and obligations. For each right and obligation, compare labels and descriptions to detect conflicts, providing a clear, step-by-step analysis. Present the results in JSON format, with each key representing a specific conflict and each value containing the detailed analysis. Base your analysis strictly on the information provided, avoiding assumptions or external interpretations.

          ### Instructions for Conflict Detection:
          1. **Identify Conflicts:**
              - For each right/obligation, compare the labels ("CAN", "CANNOT", "MUST", etc.) from both licenses.
              - If both licenses agree on the label (e.g., both say "CAN"), there’s no conflict.
              - If one license permits an action (e.g., "CAN") and the other prohibits it (e.g., "CANNOT"), this indicates a conflict.
              - If one license permits/prohibits an action while the other is "NOT MENTIONED", assess how this absence might affect interpretation. Consider whether "NOT MENTIONED" implies permission or prohibition depending upon that right/obligation and decide if its conflicting or not.
              - If both licenses gives "NOT MENTIONED" as its label, then consider whether it implies permission or prohibition depending upon that right/obligation and decide if its conflicting or not.

          ### Rights and Obligations that needs to be considered for the conflict detection:
          ```
          1. Distribute  
              - Description: Distribute original or modified derivative works  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          2. Modify  
              - Description: Modify the software and create derivatives  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          3. Commercial Use  
              - Description: Use the software for commercial purposes  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          4. Relicense  
              - Description: Add other licenses to the software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          5. Hold Liable  
              - Description: Hold the author responsible for subsequent impacts  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          6. Use Patent  
              - Description: Practice patent claims of contributors  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          7. Sublicense  
              - Description: Incorporate the work into something with a more restrictive license  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          8. Statically Link  
              - Description: Compile the library into the program linked at compile time  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          9. Private Use  
              - Description: Use or modify software freely without distribution  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          10. Use Trademark  
              - Description: Use contributors’ names, trademarks, or logos  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          11. Place Warranty  
              - Description: Place a warranty on the licensed software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          12. Include Copyright  
              - Description: Retain the copyright notice in copies or substantial uses  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          13. Include License  
              - Description: Include the full text of the license in modified software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          14. Include Notice  
              - Description: Include a NOTICE when distributing if present  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          15. Disclose Source  
              - Description: Disclose your source code when distributing the software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          16. State Changes  
              - Description: State significant changes made to the software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          17. Include Original  
              - Description: Distribute copies of the original software or provide instructions to obtain copies  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          18. Give Credit  
              - Description: Give explicit credit to the author with the software  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          19. Rename Change  
              - Description: Change the software name to avoid misrepresentation  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          20. Contact Author  
              - Description: Obtain permission or contact the author about the module used  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          21. Include Install Instructions  
              - Description: Include necessary installation information  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          22. Compensate for Damages  
              - Description: Compensate the author for damages caused by your work  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          23. Pay Above Use Threshold  
              - Description: Pay the licensor after a certain amount of use  
              - Possible Labels: CAN, CANNOT, MUST, NO NEED
          ```
          **Note:** Label will be given as "NOT MENTIONED" if any information regarding that field is not given in the license text.
          '''
      },
      {
          "role": "user",
          "content": '''Permissions JSON for License 1: "{
                ""Distribute"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license explicitly grants permission to distribute the software.""
                },
                ""Modify"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants the right to modify the software.""
                },
                ""Commercial Use"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license allows for commercial use, as it grants the right to sell copies of the software.""
                },
                ""Relicense"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to sublicense the software.""
                },
                ""Hold Liable"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license explicitly states that the authors and copyright holders are not liable for any claims, damages, or other liability.""
                },
                ""Use Patent"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license does not restrict the use of patent claims, implying that it is allowed.""
                },
                ""Sublicense"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license explicitly grants permission to sublicense the software.""
                },
                ""Statically Link"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""There is no mention of static linking in the license text.""
                },
                ""Private Use"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants the right to use the software without restriction.""
                },
                ""Use Trademark"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The text does not mention any rights related to trademarks.""
                },
                ""Place Warranty"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license explicitly states that the software is provided 'as is,' without any warranty.""
                },
                ""Include Copyright"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the copyright notice be included in all copies or substantial portions of the software.""
                },
                ""Include License"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the permission notice be included in all copies or substantial portions of the software.""
                },
                ""Include Notice"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the permission notice be included in all copies or substantial portions of the software.""
                },
                ""Disclose Source"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""There is no mention of a requirement to disclose source code.""
                },
                ""State Changes"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The license does not specify any obligation to state changes made to the software.""
                },
                ""Include Original"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require including the original software.""
                },
                ""Give Credit"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software, which implies giving credit to the author.""
                },
                ""Rename Change"": {
                    ""label"": ""YES"",
                    ""reasoning"": ""The license does not restrict renaming the software.""
                },
                ""Contact Author"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require contacting the author.""
                },
                ""Include Install Instructions"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require including installation instructions.""
                },
                ""Compensate for Damages"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license explicitly states that the authors and copyright holders are not liable for any claims, damages, or other liability.""
                },
                ""Pay Above Use Threshold"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not specify any payment requirements after a certain amount of use.""
                }
            }"
            Permissions JSON for License 2"{
                ""Distribute"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license explicitly grants permission to distribute the software.""
                },
                ""Modify"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to modify the software.""
                },
                ""Commercial Use"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to use the software for any purpose, including commercial use.""
                },
                ""Relicense"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to distribute the software under this license, implying that re-licensing is also allowed.""
                },
                ""Hold Liable"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license includes a warranty disclaimer and liability protection for the author.""
                },
                ""Use Patent"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The text does not address patent claims.""
                },
                ""Sublicense"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to distribute the software, implying that sublicensing is also allowed.""
                },
                ""Statically Link"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""There is no mention of static linking in the license text.""
                },
                ""Private Use"": {
                    ""label"": ""CAN"",
                    ""reasoning"": ""The license grants permission to use the software for any purpose, including private use.""
                },
                ""Use Trademark"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require permission to use the author's name in advertising or publicity.""
                },
                ""Place Warranty"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license includes a warranty disclaimer, indicating that no warranties can be placed.""
                },
                ""Include Copyright"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the copyright notice appear in all copies.""
                },
                ""Include License"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the permission notice and warranty disclaimer appear in supporting documentation.""
                },
                ""Include Notice"": {
                    ""label"": ""MUST"",
                    ""reasoning"": ""The license requires that the permission notice and warranty disclaimer appear in supporting documentation.""
                },
                ""Disclose Source"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""There is no mention of a requirement to disclose source code.""
                },
                ""State Changes"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The license does not specify any obligation to state changes made to the software.""
                },
                ""Include Original"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The text does not address whether the original software must be included.""
                },
                ""Give Credit"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require explicit credit to the author.""
                },
                ""Rename Change"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require changing the software name to avoid misrepresentation.""
                },
                ""Contact Author"": {
                    ""label"": ""NO NEED"",
                    ""reasoning"": ""The license does not require permission to use the author's name in advertising or publicity.""
                },
                ""Include Install Instructions"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""There is no mention of including installation instructions.""
                },
                ""Compensate for Damages"": {
                    ""label"": ""CANNOT"",
                    ""reasoning"": ""The license includes a liability protection for the author.""
                },
                ""Pay Above Use Threshold"": {
                    ""label"": ""NOT MENTIONED"",
                    ""reasoning"": ""The document does not specify any payment requirements after a certain amount of use.""
                }
            }"          
           '''
      },
      {
          "role": "assistant",
          "content": '''{
            "Distribute": "Both licenses allow distribution, so there is no conflict.",
            "Modify": "Both licenses allow modification, so there is no conflict.",
            "Commercial Use": "Both licenses permit commercial use, so there is no conflict.",
            "Relicense": "Both licenses allow relicensing, so there is no conflict.",
            "Hold Liable": "Both licenses state that the authors cannot be held liable, so there is no conflict.",
            "Use Patent": "License 1 allows the use of patents, while License 2 does not mention it. This could lead to confusion about patent usage rights.",
            "Sublicense": "Both licenses allow sublicensing, so there is no conflict.",
            "Statically Link": "Both licenses do not mention static linking, leading to ambiguity in interpretation about whether it is allowed.",
            "Private Use": "Both licenses allow private use, so there is no conflict.",
            "Use Trademark": "License 1 does not address trademark use, while License 2 implies it is allowed. This creates potential confusion about trademark usage rights.",
            "Place Warranty": "Both licenses state that no warranties can be placed, so there is no conflict.",
            "Include Copyright": "Both licenses require including the copyright notice, so there is no conflict.",
            "Include License": "Both licenses require including the license text, so there is no conflict.",
            "Include Notice": "Both licenses require including a notice, so there is no conflict.",
            "Disclose Source": "Both licenses do not mention source code disclosure, leading to ambiguity about whether disclosure is required.",
            "State Changes": "Both licenses do not mention stating changes, creating ambiguity regarding any obligation to do so.",
            "Include Original": "License 1 implies that including the original software is not required, while License 2's omission leads to confusion about whether it is required.",
            "Give Credit": "License 1 requires giving explicit credit to the author, while License 2 does not require explicit credit. This creates confusion regarding the obligation to credit the author.",
            "Rename Change": "Both licenses allow renaming, so there is no conflict.",
            "Contact Author": "Both licenses do not require contacting the author, so there is no conflict.",
            "Include Install Instructions": "License 1 implies that including installation instructions is not required, while License 2's omission leads to confusion regarding any requirement.",
            "Compensate for Damages": "Both licenses state that authors cannot be compensated for damages, so there is no conflict.",
            "Pay Above Use Threshold": "License 1 implies that paying above a use threshold is not required, while License 2's omission creates ambiguity about any potential requirement."
            }
            '''
      },
      {
          "role": "user",
          "content": f'''Permissions JSON for License 1: {license1_json}
                         Permissions JSON for License 2: {license2_json}'''
      }
  ]
  
  return messages


def get_conclusion_prompt(text):
    messages = [
        {
            "role": "system",
            "content": '''You are a legal analysis assistant tasked with providing a very **brief overall summary** of license comparison results based on a JSON structure. 
            Focus on capturing the **key points** of alignment, conflict, and ambiguity in **no more than 4 lines**. Be accurate in your summary and do not twist the facts.
            
            Your summary should:
            1. Mention if the licenses **align** or have **conflicts** in key areas.
            2. Point out any **ambiguities** or unclear aspects.
            3. Be **short and concise**—not more than 6 lines total.
            4. Avoid listing specific rights/obligations, instead focus on the **general picture** of how the two licenses compare.

            **Important distinctions:**
            - **Conflicts** occur only when one license **explicitly contradicts** the other (e.g., one license permits something while the other prohibits it).
            - **Ambiguities** arise when one license is **silent** or **unclear** about a particular obligation or right, or when it's unclear how both licenses address the issue (e.g., one mentions it, the other doesn't or both doesn't mention it).
            - If a license is silent about an obligation or right, it should be categorized as an **ambiguity**, not a **conflict**.

            The goal is to give the user a **quick, digestible overview** of the most important aspects of the license comparison.
            '''
        },
        {
            "role": "user",
            "content": f'''
            Input JSON:\n{text}
            '''
        }
    ]
    return messages
