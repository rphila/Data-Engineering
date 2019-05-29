# "Sparkify" ETL Process
 - The purpose of this data modeling project is to architect a database schema and ETL pipeline that would optimize the analytic team's ability to query information about songplay activity data being collected from "sparikfy's" music streaming app (i.e most played songs, most active user on "sparkify", etc).
 - The ETL pipeline created uses python and SQL scripts to:
   - __Extract__ data about user songplay session activity and song metadata from json files within local directories
   - __Transform__ the extracted json datasets into new data formats and structures that will fit into a relational data model
   - __Load__ the transformed data into relational tables in Postgres database, removing duplicate values
 
## Repo Content
### Datasets (data.zip)
 - `/data/song_data`: songs and artist metadata partitioned into directories according to first 3 letters of track ID 
   - This dataset is subset of http://millionsongdataset.com/
 - `/data/log_data`: data of user session activity logs on the sparkify music streaming app, partitioned into directories by year and month
 
### Postgres Database (dbname: sparkifydb) 
  - The sparkify database is a star schema with the songplay session data as the main fact table and supporting dimension tables containing information about song, artist, user and time. This structure (pictured below) allows optimized querying on any of the dimension table fields to join with data in the songplay table. 
  
 ![star schema](https://github.com/rphila/Data-Engineering/blob/master/data_modeling_Postgres/img/star_schema.png)
  
  (_Primary Key fields are in bold while foreign key (FK) relationships between tables are identified with lines linking them;_
  
  _NOTE: FK relationships between songs and artists tables are disabled due to their dataset being incomplete, resulting in missing values when joined_)
  
  - Table description:
    - `artists`: dimension table containing list of song artists (duplicates removed)
    - `songs`: dimension table containing list of songs (duplicates removed)
    - `users`: dimension table containing list of users (duplicates removed, with the latest subscription "level" used during insert)
    - `time`: dimension table breaking up timestamp info about dates and times of user sessions
    - `songplays`: fact table containing logs of "NextSong" songplay sessions from users
    
  - Preview of songplays table:
   ![songplays](https://github.com/rphila/Data-Engineering/blob/master/data_modeling_Postgres/img/songplays.PNG)
      
### Python Scripts
- `sql_queries.py`: contains SQL scripts to create database tables and insert data into them
- `create_tables.py`: drops and recreates sparkify database and tables defined in sql_queries.py (run this script to reset the database)
- `etl.py`: main script to __extract__ song and log data from json files in `/data`, __transform__ them into required formats for the data model, and then __load__ them into relational tables in the sparkify database, removing duplicate values.

### Jupyter Notebooks
- `etl.ipynb`: workbook planning the etl process
- `test.ipynb`: workbook containing SQL select scripts to view data from tables in the sparkify database and run analytic queries
- `run_scripts.ipynb`: workbook with scripts to run for creating and populating the sparkify database

## Running the pipeline
### Prerequisite
 - Postgres is installed on local host with default database `(host=127.0.0.1 dbname=studentdb user=student password=student)`
 - Python3 to run .py scripts
 - Contents of `/data.zip` file extracted into `/data`

### Instruction
 - Run `create_tables.py`
 - Run `etl.py`
 - Run through commands in `test.ipynb` to verify all tables in sparkify database has been populated with the json data
 
## Example Analysis:
### Queries and Results
- Songplay session by weekday:

 ![query1](https://github.com/rphila/Data-Engineering/blob/master/data_modeling_Postgres/img/query1.PNG)
  
- Songplay session by gender:
> SELECT u.gender, count(s.songplay_id) AS cnt FROM songplays s JOIN users u ON s.user_id=u.user_id GROUP BY u.gender

    - F:	4895
    - M:	1936

 - Songplay session by subscription level:
 > SELECT u.level, count(s.songplay_id) AS cnt FROM songplays s JOIN users u ON s.user_id=u.user_id GROUP BY u.level
 
    - paid:	4547
    - free:	2284
  
  - Songs played in sessions
  > SELECT s.title, count(sp.songplay_id) AS cnt FROM songplays sp LEFT JOIN songs s ON sp.song_id=s.song_id GROUP BY s.title
  
     - None:	6830
     - Setanta matins:	1
   
### Findings
 - Most active users listening to music on sparkfy music streaming app are female, those with paid subscipions, and on Friday.
 - Only 1 record from the songplay logs were matched with the song/artist metadata

### Next Steps:
 - Import the complete set of song/artist metadata from the `millionssongdataset` so more informative analysis on the songs/artists being played in sparkify can be queried
