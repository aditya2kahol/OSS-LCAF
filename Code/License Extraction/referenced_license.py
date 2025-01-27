"""
    Strategy to extract Referenced licenses:
    1. for Python dependencies: use the pypi package manager.
    2. for Javascript dependencies: use npm registry
    3. for Ruby dependencies: use rubygems api
    4. for Java dependencies: use maven central
    5. for c, c++ and c# dependencies: manually extract from GitHub
"""
import os
import requests
# import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from utils import (extract_python_dependencies,
                   extract_js_dependencies,
                #    extract_java_dependencies,
                   extract_ruby_dependencies,
                   extract_rust_dependencies,
                   extract_csharp_dependencies,
                   extract_c_cplusplus_dependencies)

def extract_dependencies_from_file(file_path: str) -> List[str]:
    # print(file_path.split('/')[-1])
    if file_path.endswith(('requirements.txt', 'Pipfile', 'Pipfile.txt', 'pyproject.toml', 'environment.yaml')):
        print(f"Python file found at {file_path}")
        return extract_python_dependencies(file_path, language="Python")
    elif file_path.endswith('package.json'):
        print(f"Javascript file found at {file_path}")
        return extract_js_dependencies(file_path, language="Js")
    # elif file_path.endswith(('pom.xml', 'build.gradle')):
    #     print(f"Java file found!")
    #     return extract_java_dependencies(file_path, language="Java")
    elif file_path.endswith('Gemfile'):
        print(f"Ruby file found at {file_path}!")
        return extract_ruby_dependencies(file_path, language="Ruby")
    elif file_path.endswith('Cargo.toml'):
        print(f"Rust file found at {file_path}!")
        return extract_rust_dependencies(file_path, language="Rust")
    elif file_path.endswith(('CMakeLists.txt', 'Makefile')):
        print(f"C++ file found at {file_path}")
        return extract_c_cplusplus_dependencies(file_path, language="C++")
    elif file_path.endswith(('.csproj', 'packages.config')):
        print(f"C# file found at {file_path}")
        return extract_csharp_dependencies(file_path, language="C#")
    return []

def find_all_files(directory: str) -> List[str]:
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def get_pypi_license(package_name: str) -> str:
    """
        Fetch license information from PyPI registry.
        :param package_name: The name of the PyPI package
        :return: License information or a message if not found
    """
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            license_info = data.get('info', {}).get('license', 'No license information found')
            return license_info
        except:
            return 'Package not found'
    else:
        return 'Package not found'

def get_npm_license(package_name: str) -> str:
    """
        Fetch license information from npm registry.
        :param package_name: The name of the npm package
        :return: License information or a message if not found
    """
    api_url = f'https://registry.npmjs.org/{package_name}'
    web_url = f'https://www.npmjs.com/package/{package_name}'
    try:
        """First Try to extract the license using the api"""
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            license_info = data.get('license', 'No license information found')
            return license_info
        else:
            return 'Package not found'
    except:
        """If max retry limit exceeds, try to scraping the web for license"""
        try:
            # Send a GET request to the URL
            response = requests.get(web_url)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the content of the page with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the <div> containing the <h3> with the text "License"
            license_div = soup.find('h3', string='License')

            if license_div:
                # Get the parent <div> of the found <h3>
                parent_div = license_div.find_parent('div')
                if parent_div:
                    p_tag = parent_div.find('p')
                    license_identifier = p_tag.get_text().strip()
                    return license_identifier
                else:
                    return "Package not found"
            else:
                return "Package not found"
        except:
            return 'Package not found'

def get_ruby_gem_license(package: str)->str:
    """Useful to extract Ruby dependency license identifier."""
    url=f'https://rubygems.org/gems/{package}'
    try:
        # Send a GET request to the URL
        response=requests.get(url)
        response.raise_for_status() #Raise an error for bad response

        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the span with class 'gem__ruby-version'
        span_tag = soup.find('span',class_='gem__ruby-version')
        if span_tag:
            license_identifier=span_tag.get_text().strip()
            return license_identifier
    except:
        return "Package not found."

def get_rust_license(package:str):
    """Useful to extract rust dependency license identifier"""
    url = f'https://crates.io/api/v1/crates/{package}'
    try:
        # Send a GET request to the URL
        response=requests.get(url)
        response_dict = response.json()
        versions = response_dict['versions']
        versions_dict = versions[0]
        license_identifier = versions_dict['license']
        return license_identifier
    except:
        return "Package not found"

def get_vcpkg_license_identifier(package_name):
    """Useful to extract C++ dependency license identifiers"""
    url = f"https://vcpkg.io/en/package/{package_name}"
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Navigate to the div with the class sidebar-container
        sidebar_container = soup.find('div', class_='sidebar-container')
        if sidebar_container:
            # Locate the sidebar-section
            sidebar_section = sidebar_container.find('div', class_='sidebar-section')
            if sidebar_section:
                final_div = sidebar_section.find('div')
                license_identifier = final_div.get_text(strip=True)
            return license_identifier if license_identifier else "Package not found"
        
        return "Package not found"
    except Exception as e:
        return "Package not found"

def get_nuget_license_identifier(package_name):
    """Useful to extract C# dependency license identifiers."""
    # URL for the NuGet package
    url = f'https://www.nuget.org/packages/{package_name}'
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the <i> with specified class
        i_tag = soup.find('i', class_='ms-Icon ms-Icon--Certificate')
        if i_tag:
            #Find the parent <li> for i-tag
            parent_li = i_tag.find_parent('li')
            if parent_li:
                #Extract the license text
                a_tag = parent_li.find('a')
                license_identifier=a_tag.get_text().strip()
                return license_identifier
        else:
            return "Package not found"
    except requests.exceptions.RequestException as e:
        return "Package not found"

def ref_licenses(path:str):
    all_files = find_all_files(path)
    all_dependencies = {"Python":[], "Js":[],
                        # "Java":[],
                        "Ruby":[], "Rust":[],
                        "C++":[], "C#":[]
                        }
    for file in all_files:
        dependencies = extract_dependencies_from_file(file)
        if dependencies:
            all_dependencies[dependencies[1]].extend(dependencies[0])
            #dependencied[1]->language, dependencies[0]->dependency
    # removing duplicate dependencies
    all_dependencies = {language: list(set(all_dependencies[language])) for language in all_dependencies}
    return all_dependencies

def get_referenced_license_dict(paths):
    all_functions = {"Python":get_pypi_license,
                     "Js":get_npm_license,
                    #  "Java":get_maven_license,
                     "Ruby":get_ruby_gem_license,
                     "Rust":get_rust_license,
                     "C++":get_vcpkg_license_identifier,
                     "C#":get_nuget_license_identifier
                     }
    license_dict = {
        "Repository name":[],
        "Repository path":[],
        "License text":[],
        "License type":[]
    }
    for path in paths:
        # print(path)
        all_dependencies = ref_licenses(path)
        
        for language in all_dependencies:
            for dependency in all_dependencies[language]:
                license = all_functions[language](dependency)
                if license in ['SEE LICENSE IN LICENSE','No license information found','Package not found', 'N/A']:
                    continue
                license_dict['Repository name'].append(path.split('/')[-1])
                license_dict['Repository path'].append(path)
                license_dict['License text'].append(license)
                license_dict['License type'].append("Referenced")
    return license_dict

if __name__ == '__main__':
    print("Nothing to see here!")
