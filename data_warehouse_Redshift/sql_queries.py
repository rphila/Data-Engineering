import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

'''Data in staging tables are temporary and will be futher transformed into their correct data formats downstream'''
staging_events_table_create= ("CREATE TABLE IF NOT EXISTS staging_events ("
                    "artistname text,"
                    "auth text,"
                    "firstName text,"
                    "gender text,"
                    "itemInSession int,"
                    "lastName text,"
                    "length text,"
                    "level text,"
                    "location text,"
                    "method text,"
                    "page text,"
                    "registration text,"
                    "sessionId int,"
                    "song text,"
                    "status int,"
                    "ts bigint,"
                    "userAgent text,"
                    "userId int)")

staging_songs_table_create = ("CREATE TABLE IF NOT EXISTS staging_songs ("
                     "artist_id text,"
                     "artist_latitude float,"
                     "artist_longitude float,"
                     "artist_location text,"
                     "artist_name text,"
                     "duration float,"
                     "num_songs int,"
                     "song_id text,"
                     "title text,"
                     "year int)")

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplay ("
                         "songplay_id BIGINT IDENTITY(0,1) NOT NULL, "
                         "start_time BIGINT NOT NULL sortkey, "
                         "user_id INTEGER NOT NULL, "
                         "level VARCHAR(255) NOT NULL, "
                         "song_id VARCHAR(255) NOT NULL distkey, "
                         "artist_id VARCHAR(255), "
                         "session_id INTEGER NOT NULL, "
                         "location VARCHAR(255) NOT NULL, "
                         "user_agent VARCHAR(255) NOT NULL"
                         ");")

user_table_create = ("CREATE TABLE IF NOT EXISTS users ("
                     "user_id INTEGER NOT NULL sortkey, "
                     "first_name VARCHAR(255) NOT NULL, "
                     "last_name VARCHAR(255) NOT NULL, "
                     "gender VARCHAR(4) NOT NULL, "
                     "level VARCHAR(255) NOT NULL"
                     ");")

song_table_create = ("CREATE TABLE IF NOT EXISTS song ("
                     "song_id VARCHAR(255) NOT NULL sortkey, "
                     "title VARCHAR(255) NOT NULL, "
                     "artist_id VARCHAR(255) NOT NULL, "
                     "year INTEGER NOT NULL, "
                     "duration FLOAT NOT NULL);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artist ("
                       "artist_id VARCHAR(255) NOT NULL sortkey, "
                       "name VARCHAR(255) NOT NULL, "
                       "location VARCHAR(255), "
                       "latitude FLOAT, "
                       "longitude FLOAT);")

time_table_create = ("CREATE TABLE IF NOT EXISTS time ("
                     "start_time BIGINT NOT NULL sortkey, "
                     "hour INTEGER NOT NULL, "
                     "day INTEGER NOT NULL, "
                     "week INTEGER NOT NULL, "
                     "month INTEGER NOT NULL, "
                     "year INTEGER NOT NULL, "
                     "weekday INTEGER NOT NULL);")

# STAGING TABLES

staging_events_copy = ("COPY staging_events FROM {} " +
                       "CREDENTIALS 'aws_iam_role={}' " +
                       "REGION 'us-west-2' COMPUPDATE OFF " +
                       "JSON {}").format(config.get('S3', 'LOG_DATA'), 
                                config.get('IAM_ROLE','ARN'), 
                                config.get('S3', 'LOG_JSONPATH'),)

staging_songs_copy = ("COPY staging_songs FROM {} " +
                      "CREDENTIALS 'aws_iam_role={}' "+
                      "REGION 'us-west-2' COMPUPDATE OFF "+
                      "JSON 'auto' ").format(config.get('S3', 'SONG_DATA'), 
                                config.get('IAM_ROLE','ARN'))

    
# FINAL TABLES
'''Select unique user record, keeping user data from latest timestamp'''
user_table_insert = ("INSERT INTO users ("
                         "user_id, "
                         "first_name, "
                         "last_name, "
                         "gender, "
                         "level) "
                     "SELECT se.userId, "
                         "firstname, "
                         "lastname, "
                         "gender, "
                         "level "
                    "FROM staging_events se "
                    "INNER JOIN ("
                        "SELECT userId, MAX(ts) as MaxDate "
                        "FROM staging_events "
                        "GROUP BY userId "
                        ") se2 on se.userId = se2.userId and se.ts = se2.MaxDate")

song_table_insert = ("INSERT INTO song ("
                         "song_id, "
                         "title, "
                         "artist_id, "
                         "year, "
                         "duration) "
                    "SELECT DISTINCT song_id, "
                             "title, "
                             "artist_id, "
                             "year, "
                             "duration "
                    "FROM staging_songs")

artist_table_insert = ("INSERT INTO artist ("
                          "artist_id, "
                           "name, "
                           "location, "
                           "latitude, "
                           "longitude) "
                    "SELECT DISTINCT artist_id, "
                             "artist_name, "
                             "artist_location, "
                             "artist_latitude, "
                             "artist_longitude "
                    "FROM staging_songs")

time_table_insert = ("INSERT INTO time ("
                          "start_time, "
                         "hour, "
                         "day, "
                         "week, "
                         "month, "
                         "year, "
                         "weekday)"
                  "SELECT DISTINCT ts"
                    ",EXTRACT(HOUR FROM ts_start_time) As ts_hour "
                    ",EXTRACT(DAY FROM ts_start_time) As ts_day "
                    ",EXTRACT(WEEK FROM ts_start_time) As ts_week "
                    ",EXTRACT(MONTH FROM ts_start_time) As ts_month "
                    ",EXTRACT(YEAR FROM ts_start_time) As ts_year "
                    ",EXTRACT(DOW FROM ts_start_time) As ts_weekday "
                "FROM ("
                "SELECT DISTINCT ts,'1970-01-01'::date + ts/1000 * interval '1 second' as ts_start_time "
                "FROM staging_events)")

songplay_table_insert = ("INSERT INTO songplay ("
                             "start_time, "
                             "user_id, "
                             "level, "
                             "song_id, "
                             "artist_id, "
                             "session_id, "
                             "location, "
                             "user_agent)"
                        "SELECT "
                             "se.ts, "
                             "se.userId, "
                             "se.level, "
                             "sa.song_id, "
                             "sa.artist_id, "
                             "se.sessionId, "
                             "se.location, "
                             "se.userAgent "
                        "FROM staging_events se "
                        "JOIN (SELECT "
                                 "s.song_id, "
                                 "a.artist_id, "
                                 "s.title, "
                                 "a.name, "
                                 "s.duration "
                            "FROM song s JOIN artist a ON s.artist_id = a.artist_id) AS sa "
                        "ON (sa.title = se.song AND sa.name = se.artistname AND sa.duration = se.length) "
                        "WHERE se.page = 'NextSong'")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert,song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
