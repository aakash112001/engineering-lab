from pathlib import Path

from jobspy import scrape_jobs


RAW_OUTPUT_PATH = Path("data/raw/jobs_raw.csv")
CLEAN_OUTPUT_PATH = Path("data/processed/jobs_clean.csv")


def collect_jobs():
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term="Python Developer",
        location="Dallas, TX",
        results_wanted=10,
        country_indeed="USA",
    )

    return jobs


def save_raw_jobs(jobs):
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    jobs.to_csv(RAW_OUTPUT_PATH, index=False)


def clean_jobs(jobs):
    useful_columns = [
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


def print_summary(jobs, cleaned_jobs):
    print("Job collection pipeline completed")
    print(f"Raw jobs collected: {len(jobs)}")
    print(f"Clean jobs saved: {len(cleaned_jobs)}")
    print(f"Raw output: {RAW_OUTPUT_PATH}")
    print(f"Clean output: {CLEAN_OUTPUT_PATH}")

    print("\nCleaned job preview:")
    print(cleaned_jobs.head().to_string(index=False))


def main():
    jobs = collect_jobs()
    save_raw_jobs(jobs)

    cleaned_jobs = clean_jobs(jobs)
    save_clean_jobs(cleaned_jobs)

    print_summary(jobs, cleaned_jobs)


if __name__ == "__main__":
    main()