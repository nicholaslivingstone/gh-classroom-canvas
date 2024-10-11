import pandas as pd
import argparse

def get_parser():
    parser = argparse.ArgumentParser(
            description="Merge GitHub grades with Canvas roster.",
            add_help=False
        )
    parser.add_argument('-g', '--github_grades', required=True, help="Path to the GitHub assignment grades CSV file.")
    parser.add_argument('-r', '--canvas_roster', required=True, help="Path to the Canvas roster CSV file.")
    parser.add_argument('-o', '--output', default="merged_roster.csv", help="Output file path for the merged CSV file. (Default: merged_roster.csv)")

    return parser

def merge_roster_and_grades(github_grades_fpath, canvas_roster_fpath, output_fpath):
    # Load the CSV files
    assignment_grades = pd.read_csv(github_grades_fpath)
    roster = pd.read_csv(canvas_roster_fpath)

    # Get the roster identifier from the email for merging
    roster["roster_identifier"] = roster["Email"].str.split("@").str[0]

    # Acquire student first and last name for ordering purposes
    roster["Last Name"] = roster["Student Name"].str.split(" ").str[1:].str.join(" ")
    roster["First Name"] = roster["Student Name"].str.split(" ").str[0]

    # Select only the columns we need from assignment grades
    assignment_grades = assignment_grades[["roster_identifier", "github_username", "student_repository_url"]]

    merged_df = pd.merge(roster, assignment_grades, on="roster_identifier", how="left")

    # Save the merged dataframe to a CSV file
    merged_df.to_csv(output_fpath, index=False)

def main(args):
    merge_roster_and_grades(args.github_grades, args.canvas_roster, args.output)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)