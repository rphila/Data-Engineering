# "Sparkify" ETL Process in the Cloud
- This project is a continuation of the [initial data engineering project started for 'Sparkify'](https://github.com/rphila/Data-Engineering/tree/master/data_modeling_Postgres). 
- As the user base and song database grows at Sparkify, the json data has been moved to AWS S3 to handle the increase in volume, and a new cloud database hosted on AWS Redshift will be needed for analytics.
- The purpose of this project is to adjust the ETL and analytics process to fit into the new cloud infastructure. This includes:
   - __Extract__ json data from files in S3 and stage them in Redshift
   - __Transform__ the data from the staging tables into new data formats and structures that will fit into the star schema model, removing duplicate values
   - __Load__ the transformed data into fact and dimension tables in Redshift, that is suitable for analtyics
 

### Redshift Data Warehouse 
  - The same star schema will be created as the final tables in Redshift -- with the songplay session data as the main fact table and supporting dimension tables containing information about song, artist, user and time.   

 ![star schema](https://github.com/rphila/Data-Engineering/blob/master/data_modeling_Postgres/img/star_schema.png)
  
  - However, with increased data volume the analytics process will also require optimization. Redshift was choosen because it provides efficient columnar data storage and offers optimized query performance with their massively parallel processing architecture. 
  - To optimize query performance, a table in Redshift is partitioned and distributed across different nodes in the cluster.
  - Based on knowledge about the content distribution of the dataset and access patterns, a strategy can be devised to optimize the table design by defining the distribution style and sorting keys.
  - Table description:
    - `artists`: dimension table containing list of song artists (duplicates removed): __artist_id - sortkey __
    - `songs`: dimension table containing list of songs (duplicates removed): __song_id - sortkey, distkey__
    - `users`: dimension table containing list of users (duplicates removed, with the latest subscription "level" used during insert): __user_id - sortkey__
    - `time`: dimension table breaking up timestamp info about dates and times of user sessions: __start_time - sortkey__
    - `songplays`: fact table containing logs of "NextSong" songplay sessions from users: __song_id - distkey, start_time - sortkey__
    
 - Also, before being transformed into the final star schema, the data has to first be loaded from S3 onto staging stages on Redshift. From the staging tables, SQL queries can then be created to transform then into the final structure for analytics. 

## Repo Content      
### Python Scripts
_Note: These scripts reference values for resources from a config file: dwh.cfg_

- `sql_queries.py`: contains SQL scripts to create redshift tables and insert data into them
- `create_tables.py`: drops and recreates redshift tables defined in sql_queries.py (run this script to reset the database)
- `etl.py`: main script to __extract__ json data from S3 and stage on redshift, __transform__ them into required formats for the data model, and then __load__ them into their final star shema on redshift.

### Jupyter Notebooks
- `setup.ipynb`: workbook setting up the resources that will be used (redshift cluster, IAM role) - which need to be added to the `dwh.cfg` file
- `test.ipynb`: workbook containing SQL select scripts to view data from tables in redshift and run analytic queries
- `run_scripts.ipynb`: workbook with scripts to run for creating and populating the redshift tables

## Running the pipeline
### Prerequisite
 - Redshift cluster and IAM role for readonly access to S3 should be setup (see `setup.ipynb`)
 - Python3 to run .py scripts

### Instruction
 - Run `create_tables.py`
 - Run `etl.py`
 - Run through commands in `test.ipynb` to verify all tables in redshift has been populated with the json data
 
## Example Analysis:
### Queries and Results
- See `test.ipynb`
  
- Songplay session by gender:
> SELECT u.gender, count(s.songplay_id) AS cnt FROM songplay s JOIN users u ON s.user_id=u.user_id GROUP BY u.gender

    - F:	84
    - M:	35

 - Songplay session by subscription level:
 > SELECT u.level, count(s.songplay_id) AS cnt FROM songplay s JOIN users u ON s.user_id=u.user_id GROUP BY u.level
 
    - paid:	93
    - free:	26
  
  - Most played song
  > %sql SELECT s.title, a.name, count(sp.songplay_id) AS cnt FROM songplay sp LEFT JOIN song s ON sp.song_id=s.song_id LEFT JOIN artist a ON s.artist_id=s.artist_id GROUP BY s.title, a.name ORDER BY count(sp.songplay_id) DESC LIMIT 5;
  
     - "You're The One"	by Alison Krauss / Union Station	(111 songplays)
   
### Findings
 - Most active users listening to music on sparkfy music streaming app continues to be female, those with paid subscipions, and on Friday.


