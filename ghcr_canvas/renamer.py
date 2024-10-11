import pandas as pd
from pathlib import Path
import argparse
from pandas import DataFrame

def get_parser():
    parser = argparse.ArgumentParser(
            description="Rename repositories based on roster and GitHub username to match the Canvas gradebook ordering.",
            add_help=False
        )
    
    parser.add_argument('-r', '--roster', required=True, help="Path to the roster CSV file.")
    parser.add_argument('-s', '--submissions', required=True, help="Path to the submissions directory.")
    parser.add_argument('-p', '--project_name', default=None, help="Project name (optional). If not provided, it will be derived from the submissions directory name.")
    parser.add_argument('-d', '--dry_run', action='store_true', help="If set, perform a dry run without actually renaming directories.")
    return parser

def parse_project_name(submissions_directory):
    project_name = Path(submissions_directory).name
    project_name = project_name.split("-submissions")[0]
    return project_name

def extract_github_username(repo_directory : Path, project_name : str):
    github_username = repo_directory.name.replace(f"{project_name}-", "")
    return github_username

def get_student_row(roster : DataFrame, github_username : str):
    student_row = roster[roster["github_username"] == github_username]

    # Try again by removing the number suffix from the GitHub username
    if student_row.empty:
        github_username = "-".join(github_username.split("-")[:-1])
        print("Trying again with", github_username)
        student_row = roster[roster["github_username"] == github_username]
        
    if student_row.empty:
        return None
    
    return student_row.squeeze()

def rename_repo(repo_directory : Path, student_row, project_name, dry_run=False):
    last_name = student_row["Last Name"]
    first_name = student_row["First Name"]
    github_username = student_row["github_username"]

    new_directory_name = f"{project_name}-{last_name}-{first_name}-{github_username}"
    new_directory_path = repo_directory.parent / new_directory_name

    print("Renaming to", new_directory_path)

    if not dry_run:
        repo_directory.rename(new_directory_path)

def rename_repositories(roster_fpath, submissions_directory, project_name : str = None, dry_run : bool = False):

    roster = pd.read_csv(roster_fpath)

    if project_name is None:
        project_name = parse_project_name(submissions_directory)

    # Iterate over each student's repository
    for repo_directory in Path(submissions_directory).glob("*"):
        print("\nProcessing", repo_directory)

        github_username = extract_github_username(repo_directory, project_name)

        # Find the student's row in the roster
        student_row = get_student_row(roster, github_username)

        # If the student is not in the roster, skip this repository
        if student_row is None:
            print(f"Student with GitHub username '{github_username}' not found in the roster. Skipping...")
            continue

        rename_repo(repo_directory, student_row, project_name, dry_run)
        

def main(args):
    rename_repositories(args.roster, args.submissions, args.project_name, args.dry_run)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)