#!/usr/bin/env python3
# Copyright 2024 Stichting Health-RI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
from pathlib import Path

def get_python_files(directory: str) -> list[str]:
    """Get all Python files in a directory recursively."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                full_path = os.path.join(root, file)
                python_files.append(full_path)
    return python_files

def main():
    # Get the root directory of the project
    root_dir = Path(__file__).parent
    sempyro_dir = root_dir / "sempyro"
    
    # Get all Python files in the sempyro directory
    python_files = get_python_files(str(sempyro_dir))
    
    # Process each file
    for file_path in python_files:
        try:
            print(f"Running {file_path}...")
            result = subprocess.run(['python', file_path], 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                print(f"Successfully processed {file_path}")
                if result.stdout:
                    print("Output:", result.stdout.strip())
            else:
                print(f"Error processing {file_path}:")
                print("Error output:", result.stderr.strip())
                
        except Exception as e:
            print(f"Error running {file_path}: {e}")

if __name__ == "__main__":
    main() 