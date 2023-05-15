import os
import sys
import shutil
import subprocess
from urllib.parse import urlparse
from distutils.dir_util import copy_tree

def clone_repo(repo_ssh, dir_name):
    if os.path.exists(dir_name):
        raise Exception(f"Directory '{dir_name}' already exists.")
    subprocess.run(['git', 'clone', repo_ssh, dir_name], check=True)

def check_if_repo_empty(dir_name):
    return len(os.listdir(dir_name)) <= 1

def clone_repo_without_git(repo_ssh, dir_name):
    clone_repo(repo_ssh, dir_name)
    shutil.rmtree(os.path.join(dir_name, '.git'))

def move_files(source_dir, dest_dir):
    copy_tree(source_dir, dest_dir)

def manage_repo(repo_ssh, repo_name):
    # Clone the repo
    try:
        clone_repo(repo_ssh, repo_name)
    except Exception as e:
        print(f"Error during cloning: {e}")
        return

    # Check if the repo is empty
    if not check_if_repo_empty(repo_name):
        print("Warning: The repository is not empty!")
        user_input = input("Do you want to continue? (y/n) ")
        if user_input.lower() != 'y':
            print("Process terminated by user.")
            return

    # If warning is accepted, clone the other repo into a temporary directory
    try:
        clone_repo_without_git('git@github.com:S0ly/EpiTemplate.git', 'temp_repo')
    except Exception as e:
        print(f"Error during cloning: {e}")
        return

    # Move everything from temp_repo to the user provided repo
    move_files('temp_repo/', repo_name)

    # Remove temp_repo
    shutil.rmtree('temp_repo')

    print(f"Contents of the repo 'git@github.com:S0ly/EpiTemplate.git' have been cloned to '{repo_name}' excluding '.git' directory.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python script_name.py ssh_repo_link [repo_name]')
        sys.exit(1)

    repo_ssh = sys.argv[1]
    if len(sys.argv) > 2:
        repo_name = sys.argv[2]
    else:
        repo_name = os.path.basename(urlparse(repo_ssh).path).replace('.git', '')

    manage_repo(repo_ssh, repo_name)
