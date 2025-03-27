#!/usr/bin/env python
"""
Example script for searching KAKEN projects.
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
    parser = argparse.ArgumentParser(description="Search KAKEN projects")
    parser.add_argument("--app-id", help="Application ID for the KAKEN API")
    parser.add_argument("--keyword", help="Keyword to search for")
    parser.add_argument("--title", help="Project title to search for")
    parser.add_argument("--number", help="Project number to search for")
    parser.add_argument("--researcher", help="Researcher name to search for")
    parser.add_argument("--institution", help="Institution to search for")
    parser.add_argument("--category", help="Research category to search for")
    parser.add_argument("--year-from", type=int, help="Grant period from (year)")
    parser.add_argument("--year-to", type=int, help="Grant period to (year)")
    parser.add_argument("--limit", type=int, default=5, help="Number of results to return")
    parser.add_argument("--language", default="ja", choices=["ja", "en"], help="Response language")
    args = parser.parse_args()

    # Initialize the client
    client = KakenApiClient(app_id=args.app_id)

    try:
        # Search for projects
        projects = client.projects.search(
            keyword=args.keyword,
            project_title=args.title,
            project_number=args.number,
            researcher_name=args.researcher,
            institution=args.institution,
            research_category=args.category,
            grant_period_from=args.year_from,
            grant_period_to=args.year_to,
            results_per_page=args.limit,
            language=args.language,
        )

        # Print the results
        print(f"検索結果: {projects.total_results}件")
        print(f"表示件数: {len(projects.projects)}件")
        print()

        for i, project in enumerate(projects.projects, 1):
            print(f"[{i}] 課題番号: {project.award_number}")
            print(f"    課題名: {project.title}")
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
