# "Sparkify" ETL Process
 - The purpose of this project is to load songs and log data from json files into a Postgres database that is suitable for analysis on user and songplay activity (i.e most played songs, most active user on "sparkify, etc)
 
## Requirements 
- Postgres database: dbname: sparkifly, user: student
- Python3 to run scripts

# Content
## Data Source
 - /data/song_data: songs data
 - /data/log_data: log data of users songplay
 
## Scripts
- sql_queries.py: contains SQL script to create tables and insert data into the sparkify database (songs, artists, users, time, songplays)
    -- songplays: fact table containing logs of songplay sessions from users
    -- artists: dimension table containing list of artists
    -- songs: dimension table containing list of songs (with key to artists_id in artist table)
    -- users: dimension table containing list of users
    -- time: dimension table breaking up timestamp info about dates and times
- create_tables.py: drops and recreates sparkify database and tables defined in sql_queries.py 
- etl.py: main script to extract all song and log data in json files from /data, transform their data values into appropriate format, and load into the tables on sparkify database.

## Notebooks
- etl.ipynb: workbook planning the etl process
- test.ipynb: workbook containing select scripts to view data from tables in the sparkify database
- run_scripts.ipynb: workbook with scripts to run for creating and populating hte sparkify database