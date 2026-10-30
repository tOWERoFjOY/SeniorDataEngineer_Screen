# WPRDC Data Pipeline Exercise

## Excercise goal: 
Build a small, reproducible pipeline that ingests it from the WPRDC CKAN API, producing a clean analytical table that shares something useful about the data. Completed script and markdown document should be available in a public GitHub or GitLab repository.

## Requirements

* [ ] Ingest the data programmatically (CKAN API or resource URL). No manual downloads.
* [ ] Land raw data unchanged, then transform into a cleaned/modeled layer. Use any local stack you like (Python, SQL, DuckDB, SQLite, Postgres via Docker, dbt, etc). No cloud accounts required.
  * Employing Python pandas library
* [ ] Make it re-runnable. Running it twice must not duplicate or corrupt data. Explain how you’d handle the dataset being updated.
* [ ] Add data quality checks that would actually fail on bad data. Include at least one check you wrote because of something you found in this dataset.
* [ ] Produce one output table that could be used to answer a question you chose (state the question).
* [ ] Write a README.md covering decision you made in the process: the three most important design decisions and the alternatives you rejected, what surprised you in the data, what you’d do differently at 100x scale or with daily refreshes, and what you didn’t do and why.
* [ ] AI disclosure: AI tools are allowed. Tell us which you used and for what purpose. We will ask you to walk through your code live should you progress to an interview round.

## Data Sets
- [X] Allegheny County Property Sale Transactions
- [ ] Allegheny County Weights and Measures Inspections 
- [ ] Allegheny County Air Quality
- [ ] Allegheny County Jail Census

## Project Design
