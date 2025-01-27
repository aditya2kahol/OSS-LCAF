# Utility file for creating benchmark dataset for OSS-LCAT

# import os
import re
import json
import yaml
import toml
import requests
import subprocess
from typing import List, Tuple
# from dotenv import load_dotenv

# load_dotenv()

BASE_FILE_PATH = '<path_to_store_repositories>'

# Fetch the top repos.
def fetch_top_repositories(num_links:int=5, page_num:int=1, run:bool=True, languages:List[str]=None)->List[str]:
    # num_links: number of top repository links you want to download
    # page_num: from which page you want to download the repo links
    # run: boolean value, indicating whether you want to fetch the repos or not
    if run:
        if languages is None:
            languages = ['Python','Javascript','Java','HTML','C++','c#','C','Rust','Ruby']
        url = "https://api.github.com/search/repositories"
        repositories = []
        for language in languages:
            page = page_num
            params = {
                "q": "language:{language} stars:100..3000", # previously 100..30000
                "sort": "stars",
                "order": "asc", #"desc",
                "per_page": 100 #max allowed value
            }
            while len(repositories) < num_links:
                params["page"] = page
                response = requests.get(url, params=params)
                
                if response.status_code != 200:
                    print(f"Failed to fetch data: {response.status_code}")
                    break
                data = response.json()
                items = data.get('items',[])

                if not items:
                    break # No more results
                repositories.extend(items)
                page+=1

                if len(repositories) >= num_links:
                    repositories = repositories[:num_links]
                    break
        # Extract the repository urls
        repo_urls = [repo['clone_url'] for repo in repositories]
        return repo_urls

# Clone the repos in your disk
def clone_repos(repos:List, run:bool=True)->None:
    PATH = f'{BASE_FILE_PATH}/Repositories'
    if run:
        # repository_names = []
        for repo in repos:
            repo_name = repo.split('/')[-1].replace('.git', '')
            print(f"Cloning {repo_name}...")
            try:
                print("Running the try block...")
                subprocess.run(['git', 'clone', repo, PATH+'/'+repo_name])
            except:
                print("Running the except block...")
                subprocess.run(['git', 'clone', repo, PATH])

# Remove extra spaces from the license text (if exists)
def remove_spaces(full_text:str)->str:
    text = ''
    for idx, char in enumerate(full_text):
        try:
            if (ord(char)==32 and ord(full_text[idx-1])==32):
                continue
            else:
                text += char
        except:
            if idx==0:
                if ord(char)==32:
                    continue
                else:
                    text += char
    return text

def extract_python_dependencies(file_path: str, language: str = 'Python') -> Tuple[List[str], str]:
    dependencies = []
    
    if file_path.endswith('requirements.txt'):
        with open(file_path, 'r') as f:
            dependencies = f.read().splitlines()
    elif file_path.endswith('Pipfile') or file_path.endswith('Pipfile.txt'):
        try:
            # Load the Pipfile using toml
            pipfile = toml.load(file_path)
            # Extract dependencies
            dependencies = list(pipfile.get('packages',{}).keys())
        except:
            print(f"Couldn't extract dependencies from {file_path}")
    elif file_path.endswith('pyproject.toml'):
        try:
            with open(file_path, 'r') as f:
                toml_content = f.read()
                parsed_content = toml.loads(toml_content) # Parse the TOML content
                dependencies = parsed_content.get('build-system', {}).get('requires', []) # Extract the dependencies from the 'requires' list
        except:
            print(f"Couldn't extract dependencies from {file_path}")
    elif file_path.endswith('environment.yaml'):
        try:
            with open(file_path, 'r') as f:
                environment = yaml.safe_load(f)
                deps = environment.get('dependencies', [])
                for dep in deps:
                    if isinstance(dep, dict) and 'pip' in dep:
                        dependencies.extend(dep['pip'])
                    else:
                        dependencies.append(dep)
        except:
            print(f"Couldn't extract dependencies from {file_path}")
    # Extracting names using regex
    try:
        names = [re.split('[=<>]', dep)[0] for dep in dependencies]
        # Removing duplicates and sorting (if needed)
        unique_names = sorted(set(names))
    except:
        print(f"Dependencies could not be loaded for {file_path}")
        unique_names = []
    return (unique_names, language)

def extract_js_dependencies(file_path: str, language:str="Js") -> List[str]:
    dependencies = []
    if file_path.endswith('package.json'):
        with open(file_path, 'r') as f:
            file_str = f.read()
            try:
                package_json = json.loads(file_str)
                dependencies = list(package_json.get('dependencies', {}).keys())
                dev_dependencies = list(package_json.get('devDependencies', {}).keys())
                dependencies.extend(dev_dependencies)
            except:
                pass
    if not dependencies:
        with open(file_path, 'r') as f:
            file_str = f.read()
            try:
                file_dict = json.loads(file_str)
                dependencies.append(file_dict['name'])
            except:
                pass
    return (dependencies, language)

def extract_java_dependencies(file_path: str, language:str="Java") -> List[str]:
    dependencies = []
    if file_path.endswith('pom.xml'):
        with open(file_path, 'r') as f:
            pom_content = f.read()
            dependencies = re.findall(r'<artifactId>(.*?)</artifactId>', pom_content)
    elif file_path.endswith('build.gradle'):
        with open(file_path, 'r') as f:
            gradle_content = f.read()
            dependencies = re.findall(r'''implementation\s*["\''](.*?)["\'']''', gradle_content)
    return (dependencies, language)

def extract_ruby_dependencies(file_path: str, language:str="Ruby") -> List[str]:
    dependencies = []
    if file_path.endswith('Gemfile'):
        with open(file_path, 'r') as f:
            gemfile_content = f.read()
            dependencies = re.findall(r'''gem\s*["\''](.*?)["\'']''', gemfile_content)
    return (dependencies, language)

def extract_rust_dependencies(file_path:str, language:str="Rust") -> List[str]:
    """Extracts dependencies from a Rust project directory."""
    dependencies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            in_dependencies_section=False
            for line in f:
                line = line.strip()
                if line.startswith('[dependencies]'):
                    in_dependencies_section=True
                elif line.startswith('['):
                    # Stop parsing once another section is encountered
                    break
                elif in_dependencies_section and line:
                    dep_name = line.split('=')[0].strip()
                    dependencies.append(dep_name)
        return (dependencies, language)
    except:
        return (dependencies, language)

def extract_c_cplusplus_dependencies(file_path: str, language: str = "C++") -> Tuple[List[str], str]:
    dependencies = []
    
    def read_file_with_encoding(path: str) -> str:
        encodings = ['utf-8', 'iso-8859-1', 'cp1252']  # List of encodings to try
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                # Try the next encoding if there's an error
                continue
        raise UnicodeDecodeError(f"Failed to decode {path} with the given encodings.")
    
    try:
        if file_path.endswith('CMakeLists.txt'):
            cmake_content = read_file_with_encoding(file_path)
            # Extract dependencies using the regex for CMakeLists.txt
            dependencies = re.findall(r'find_package\((.*?)\)', cmake_content)
        elif file_path.endswith('Makefile'):
            makefile_content = read_file_with_encoding(file_path)
            # Extract dependencies using the regex for Makefile
            dependencies = re.findall(r'-l([a-zA-Z0-9_]+)', makefile_content)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
    
    return (dependencies, language)

def extract_csharp_dependencies(file_path: str, language:str="C#") -> List[str]:
    dependencies = []
    if file_path.endswith('.csproj'):
        with open(file_path, 'r') as f:
            csproj_content = f.read()
            dependencies = re.findall(r'<PackageReference Include="(.*?)"', csproj_content)
    elif file_path.endswith('packages.config'):
        with open(file_path, 'r') as f:
            packages_config_content = f.read()
            dependencies = re.findall(r'<package id="(.*?)"', packages_config_content)
    return (dependencies, language)

if __name__ == '__main__':
    pass
