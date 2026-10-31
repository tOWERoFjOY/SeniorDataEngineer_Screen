# WPRDC ACJ Daily Census Excersize

## Excercise goal: 
Build a small, reproducible pipeline that ingests data from the WPRDC CKAN API, producing a clean analytical table that shares something useful about the data. Completed script and markdown document should be available in a public GitHub or GitLab repository.

## Requirements

* [ ] Ingest the data programmatically (CKAN API or resource URL). No manual downloads.
* [ ] Land raw data unchanged, then transform into a cleaned/modeled layer. Use any local stack you like (Python, SQL, DuckDB, SQLite, Postgres via Docker, dbt, etc). No cloud accounts required.
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

Attempted to use the ckan python library/wrapper suggested by the WPRDC, but the package had download conflicts due to a defunct dependency. Opted to use python requests library to interact with the REST api. 

To ensure regular, programmatic access to the resource, I opted to employ SQL payloads to send to the API. This provides the easiest method for controlling the return from this dataset using simple SQL filters and select statements. Otherwise, API calls will pull the entirety of the dataset and its 500 thousand rows. 

While 500 thousand rows is not an unwieldly dataset in modern contexts, data engineering best practices encourage pipelines with idempotent operations. Idempotency should be able to run multiple times without changing the result beyond the initial application. With a property sales dataset, we expect two types of property transactions: the sale of new property or the resale of property. So we should only expect   

 that the The dataset has a date field (Sale Date) that facilitates idempotency. This method also allows for easier transformation of this script into a scheduled python that pulls data in reproducible date ranges. 

Since I wanted to use the datastore_search_sql endpoint of the CKAN REST API, I had to resolve an issue with the 
