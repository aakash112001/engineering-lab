# Job Search Automation Lab Notes

## Project Identity

This project started as a Python learning exercise using JobSpy, but it is now evolving into a broader job search automation system.

The project name is:

Job Search Automation Lab

The current first module focuses on collecting job postings using JobSpy.

## Project Goal

Build a Python project that collects job postings using JobSpy, inspects the returned data, and saves the results for later processing.

## Current Milestone 1

We created the first working script in src/main.py.

The script does the following:

1. Imports scrape_jobs from JobSpy.
2. Searches Indeed for Python Developer jobs in Dallas, TX.
3. Requests 10 results.
4. Receives the result as a Pandas DataFrame.
5. Prints total job count.
6. Prints all returned columns.
7. Prints the first few rows.
8. Saves the results to data/processed/jobs.csv.

## Important Columns Returned

Useful columns returned by JobSpy:

- id
- site
- job_url
- title
- company
- location
- date_posted
- job_type
- is_remote
- description
- skills
- experience_range

## First Observation

JobSpy successfully returned job postings from Indeed.

The date_posted column exists, which means we can later build filters like jobs posted today, jobs posted in the last 24 hours, or jobs posted in the last 7 days.

However, the current date_posted values are date-based, not exact timestamp-based.

## Milestone 2: Raw and Clean Job Output Pipeline

In Milestone 2, we improved the original single-output script into a small data pipeline.

The pipeline flow is:

Collect jobs
→ Save raw jobs
→ Select useful columns
→ Save cleaned jobs
→ Print summary

### Raw Data

Raw data means the original data collected from the source before changing or reducing it.

In this project, raw data is saved to:

data/raw/jobs_raw.csv

This file contains the full JobSpy output with all available columns.

Keeping raw data is important because it allows us to reprocess the original data later if our cleaning logic changes.

### Processed Data

Processed data means data that has been cleaned, reduced, or transformed for easier use.

In this project, processed data is saved to:

data/processed/jobs_clean.csv

This file keeps only the columns we currently need:

- site
- title
- company
- location
- date_posted
- job_type
- is_remote
- job_url

### Why We Used Functions

We split the script into functions so each function has one clear responsibility.

Current functions:

- collect_jobs()
- save_raw_jobs()
- clean_jobs()
- save_clean_jobs()
- print_summary()
- main()

This makes the code easier to read, debug, test, and improve.

### Why We Used pathlib.Path

We used pathlib.Path to handle file paths in a clean Python way.

Example:

RAW_OUTPUT_PATH = Path("data/raw/jobs_raw.csv")

This makes file path handling more readable and gives useful methods like:

RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

That line makes sure the output folder exists before saving the CSV file.

### What clean_jobs() Does

The clean_jobs() function takes the full raw JobSpy DataFrame and selects only the useful columns.

The raw data had 34 columns.

The cleaned data keeps 8 columns.

This is our first transformation step.

### Why Generated CSV Files Are Ignored by Git

The CSV files are generated outputs.

They can be recreated by running the script again.

So we do not commit them to Git.

We commit the code that creates them, not the generated files themselves.

## Milestone 3: Search Configuration File

In Milestone 3, we moved the search settings out of Python code and into a JSON configuration file.

Before this milestone, the search values were hardcoded inside `src/main.py`.

Example:

```python
search_term="Python Developer"
location="Dallas, TX"
results_wanted=10
