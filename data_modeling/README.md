# "Sparkify" ETL Process
 - The purpose of this data modeling project is to architect a database schema and ETL pipeline that would optimize the analytics team ability to query information about songplay activity data being collected from "sparikfy's" music streaming app (i.e most played songs, most active user on "sparkify", etc).
 - This ETL pipeline uses python and SQL scripts to:
   - __Extract__ data about user songplay session activity and song metadata from json files in local directories
   - __Transform__ the extracted json datasets into new data formats and structures that will fit into a relational data model
   - __Load__ the transformed data into relational tables in Postgres database for analytic focus
 
## Repo Content
### Datasets
 - `/data/song_data`: songs and artist metadata partitioned into directories according to first 3 letters of track ID 
   - This dataset is subset of http://millionsongdataset.com/
 - `/data/log_data`: data of user session activity logs on the sparkify music streaming app, partitioned into directories by year and month
 
### Postgres Database (dbname: sparkify) 
  - Tables:
    - `songplays`: fact table containing logs of songplay sessions from users
    - `artists`: dimension table containing list of song artists
    - `songs`: dimension table containing list of songs (with key to artists_id from artist table)
    - `users`: dimension table containing list of users
    - `time`: dimension table breaking up timestamp info about dates and times of user sessions
    
### Python Scripts
- `sql_queries.py`: contains SQL scripts to create database tables and insert data into them
- `create_tables.py`: drops and recreates sparkify database and tables defined in sql_queries.py (run this script to reset the database)
- `etl.py`: main script to __extract__ song and log data from json files in `/data`, __transform__ them into required formats for the data model, and then __load__ them into relational tables in the sparkify database.

### Jupyter Notebooks
- `etl.ipynb`: workbook planning the etl process
- `test.ipynb`: workbook containing SQL select scripts to view data from tables in the sparkify database and run analytic queries
- `run_scripts.ipynb`: workbook with scripts to run for creating and populating the sparkify database

## Running the pipeline
### Prerequisite
 - Postgres installed on local host with default database `(host=127.0.0.1 dbname=studentdb user=student password=student)`
 - Python3 to run .py scripts
 - Contents of `/data.zip` file extracted into `/data`

### Instruction
 - Run `create_tables.py`
 - Run `etl.py`
 - Run through commands in `test.ipynb` to verify all tables in sparkify database has been populated with the json data
