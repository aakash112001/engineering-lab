from jobspy import scrape_jobs


def main():
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term="Python Developer",
        location="Dallas, TX",
        results_wanted=10,
        country_indeed="USA",
    )

    print("Jobs collected successfully")
    print(f"Total jobs collected: {len(jobs)}")

    print("\nColumns returned by JobSpy:")
    print(jobs.columns)

    print("\nFirst few jobs:")
    print(jobs.head())

    jobs.to_csv("data/processed/jobs.csv", index=False)
    print("\nSaved jobs to data/processed/jobs.csv")


if __name__ == "__main__":
    main()
