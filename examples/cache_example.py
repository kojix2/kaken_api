"""
Example of using the cache functionality in the KAKEN API client.
"""

import os
import time
from kaken_api import KakenApiClient


def main():
    """
    Example of using the cache functionality.
    """
    # Get the application ID from the environment variable
    app_id = os.environ.get("KAKEN_APP_ID")
    if not app_id:
        print("KAKEN_APP_ID environment variable is not set.")
        print("Please set it to your KAKEN API application ID.")
        return

    # Create a client with cache enabled (default)
    client = KakenApiClient(app_id=app_id)
    
    # First request (not cached)
    print("Making first request (not cached)...")
    start_time = time.time()
    projects = client.projects.search(keyword="人工知能", results_per_page=5)
    end_time = time.time()
    print(f"First request took {end_time - start_time:.2f} seconds.")
    print(f"Found {projects.total_results} projects.")
    
    # Second request (should be cached)
    print("\nMaking second request (should be cached)...")
    start_time = time.time()
    projects = client.projects.search(keyword="人工知能", results_per_page=5)
    end_time = time.time()
    print(f"Second request took {end_time - start_time:.2f} seconds.")
    print(f"Found {projects.total_results} projects.")
    
    # Different request (not cached)
    print("\nMaking different request (not cached)...")
    start_time = time.time()
    projects = client.projects.search(keyword="深層学習", results_per_page=5)
    end_time = time.time()
    print(f"Different request took {end_time - start_time:.2f} seconds.")
    print(f"Found {projects.total_results} projects.")
    
    # Clear the cache
    print("\nClearing the cache...")
    client.cache.clear()
    
    # Request after clearing the cache (not cached)
    print("\nMaking request after clearing the cache (not cached)...")
    start_time = time.time()
    projects = client.projects.search(keyword="人工知能", results_per_page=5)
    end_time = time.time()
    print(f"Request after clearing the cache took {end_time - start_time:.2f} seconds.")
    print(f"Found {projects.total_results} projects.")
    
    # Create a client with cache disabled
    print("\nCreating a client with cache disabled...")
    client_no_cache = KakenApiClient(app_id=app_id, use_cache=False)
    
    # Request with cache disabled
    print("\nMaking request with cache disabled...")
    start_time = time.time()
    projects = client_no_cache.projects.search(keyword="人工知能", results_per_page=5)
    end_time = time.time()
    print(f"Request with cache disabled took {end_time - start_time:.2f} seconds.")
    print(f"Found {projects.total_results} projects.")


if __name__ == "__main__":
    main()
