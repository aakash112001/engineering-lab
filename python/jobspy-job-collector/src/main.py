import json
from pathlib import Path

import pandas as pd
from jobspy import scrape_jobs


CONFIG_PATH = Path("config/search_config.json")
RAW_OUTPUT_PATH = Path("data/raw/jobs_raw.csv")
CLEAN_OUTPUT_PATH = Path("data/processed/jobs_clean.csv")


def load_config():
    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)

    return config


def collect_jobs_for_search_term(config, search_term):
    jobs = scrape_jobs(
        site_name=config["site_name"],
        search_term=search_term,
        location=config["location"],
        results_wanted=config["results_wanted"],
        country_indeed=config["country_indeed"],
    )

    jobs["search_term"] = search_term

    return jobs


def collect_jobs(config):
    all_jobs = []

    for search_term in config["search_terms"]:
        print(f"Collecting jobs for search term: {search_term}")

        jobs = collect_jobs_for_search_term(config, search_term)
        all_jobs.append(jobs)

    combined_jobs = pd.concat(all_jobs, ignore_index=True)

    return combined_jobs


def save_raw_jobs(jobs):
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    jobs.to_csv(RAW_OUTPUT_PATH, index=False)

def deduplicate_jobs(jobs):
    deduplicated_jobs = jobs.drop_duplicates(subset=["job_url"]).copy()

    return deduplicated_jobs

def clean_jobs(jobs):
    useful_columns = [
        "search_term",
        "site",
        "title",
        "company",
        "location",
        "date_posted",
        "job_type",
        "is_remote",
        "job_url",
    ]

    cleaned_jobs = jobs[useful_columns].copy()

    return cleaned_jobs


def save_clean_jobs(cleaned_jobs):
    CLEAN_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned_jobs.to_csv(CLEAN_OUTPUT_PATH, index=False)


def print_summary(config, jobs, deduplicated_jobs, cleaned_jobs):
    print("Job collection pipeline completed")
    print(f"Search terms: {config['search_terms']}")
    print(f"Location: {config['location']}")
    print(f"Sites: {config['site_name']}")
    print(f"Raw jobs collected: {len(jobs)}")
    print(f"Unique jobs after deduplication: {len(deduplicated_jobs)}")
    print(f"Clean jobs saved: {len(cleaned_jobs)}")
    print(f"Raw output: {RAW_OUTPUT_PATH}")
    print(f"Clean output: {CLEAN_OUTPUT_PATH}")

    print("\nCleaned job preview:")
    print(cleaned_jobs.head().to_string(index=False))


def main():
    config = load_config()

    jobs = collect_jobs(config)
    save_raw_jobs(jobs)

    deduplicated_jobs = deduplicate_jobs(jobs)

    cleaned_jobs = clean_jobs(deduplicated_jobs)
    save_clean_jobs(cleaned_jobs)

    print_summary(config, jobs, deduplicated_jobs, cleaned_jobs)


if __name__ == "__main__":
    main()