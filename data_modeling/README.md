# "Sparkify" ETL Process
 - The purpose of this data modeling project is to architect a database schema and ETL pipeline that would allow the analytics team to quickly analyze user songplay activity data being collected by "sparikfy's" music streaming app.
 - This ETL pipeline will extract user session data and song/artist metadata contained in json files, then transform and load them into relational tables in Postgres database, which will be optimized for running analytic queries (i.e most played songs, most active user on "sparkify", etc).
 
## Repo Content
### Data Sources
 - `/data/song_data`: songs and artist metadata
 - `/data/log_data`: log data of user songplay sessions
 
### Postgres Database (dbname: sparkify) 
  - Tables:
    - `songplays`: fact table containing logs of songplay sessions from users
    - `artists`: dimension table containing list of song artists
    - `songs`: dimension table containing list of songs (with key to artists_id from artist table)
    - `users`: dimension table containing list of users
    - `time`: dimension table breaking up timestamp info about dates and times of user sessions
    
### Python3 Scripts
- `sql_queries.py`: contains SQL scripts to create database tables and insert data into them
- `create_tables.py`: drops and recreates sparkify database and tables defined in sql_queries.py (run this script to reset the database)
- `etl.py`: main script to _extract_ all song and log data in json files from `/data`, _transform_ them into required data formats for data model, and then _load_ them into relational tables in the sparkify database.

### Jupyter Notebooks
- `etl.ipynb`: workbook planning the etl process
- `test.ipynb`: workbook containing SQL select scripts to view data from tables in the sparkify database
- `run_scripts.ipynb`: workbook with scripts to run for creating and populating the sparkify database

## Instructions
 - Run `create_tables.py`
 - Run `etl.py`
 - Run through commands in `test.ipynb` to verify all tables in sparkify database has been populated with the json data
