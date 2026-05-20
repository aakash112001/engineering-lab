# JobSpy Reverse Engineering Notes

## Project Goal

Build a Python project that collects job postings using JobSpy, inspects the returned data, and saves the results for later processing.

## Current Milestone

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

