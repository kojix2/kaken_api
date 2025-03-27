#!/usr/bin/env python
"""
Example script for searching KAKEN researchers.
"""

import os
import sys
import argparse
from pprint import pprint

# Add the parent directory to the path so we can import the kaken_api package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kaken_api import KakenApiClient


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="Search KAKEN researchers")
    parser.add_argument("--app-id", help="Application ID for the KAKEN API")
    parser.add_argument("--keyword", help="Keyword to search for")
    parser.add_argument("--name", help="Researcher name to search for")
    parser.add_argument("--number", help="Researcher number to search for")
    parser.add_argument("--institution", help="Institution to search for")
    parser.add_argument("--department", help="Department to search for")
    parser.add_argument("--job-title", help="Job title to search for")
    parser.add_argument("--project-title", help="Project title to search for")
    parser.add_argument("--project-number", help="Project number to search for")
    parser.add_argument("--limit", type=int, default=5, help="Number of results to return")
    parser.add_argument("--language", default="ja", choices=["ja", "en"], help="Response language")
    args = parser.parse_args()

    # Initialize the client
    client = KakenApiClient(app_id=args.app_id)

    try:
        # Search for researchers
        researchers = client.researchers.search(
            keyword=args.keyword,
            researcher_name=args.name,
            researcher_number=args.number,
            researcher_institution=args.institution,
            researcher_department=args.department,
            researcher_job_title=args.job_title,
            project_title=args.project_title,
            project_number=args.project_number,
            results_per_page=args.limit,
            language=args.language,
        )

        # Print the results
        print(f"検索結果: {researchers.total_results}件")
        print(f"表示件数: {len(researchers.researchers)}件")
        print()

        for i, researcher in enumerate(researchers.researchers, 1):
            print(f"[{i}] 研究者ID: {researcher.id}")
            if researcher.name:
                print(f"    氏名: {researcher.name.full_name}")
            
            # Print affiliations
            if researcher.affiliations:
                print("    所属:")
                for affiliation in researcher.affiliations:
                    if affiliation.institution:
                        print(f"      機関: {affiliation.institution.name}")
                    if affiliation.department:
                        print(f"      部局: {affiliation.department.name}")
                    if affiliation.job_title:
                        print(f"      職名: {affiliation.job_title.name}")
            print()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1

    finally:
        # Close the client
        client.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
