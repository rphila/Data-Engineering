import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_i94_table_drop = "DROP TABLE IF EXISTS staging_i94;"
staging_temperature_table_drop = "DROP TABLE IF EXISTS staging_temperature;"
staging_citydemo_table_drop = "DROP TABLE IF EXISTS staging_citydemo;"
i94_table_drop = "DROP TABLE IF EXISTS i94;"
temperature_table_drop = "DROP TABLE IF EXISTS temperature;"
citydemo_table_drop = "DROP TABLE IF EXISTS city_demo;"
cityrace_table_drop = "DROP TABLE IF EXISTS city_race;"


# CREATE TABLES
staging_i94_table_create = ("CREATE TABLE IF NOT EXISTS staging_i94 ("
                    "cicid  FLOAT NOT NULL,"
                    "i94yr FLOAT NOT NULL,"
                    "i94mon FLOAT NOT NULL,"
                    "i94cit FLOAT NOT NULL,"
                    "i94res FLOAT NULL,"
                    "i94port VARCHAR(4) NOT NULL, "
                     "arrdate FLOAT NULL,"
                    "i94mode FLOAT NULL,"
                    "i94addr VARCHAR(4) NULL, "
                     "depdate FLOAT NULL,"
                    "i94bir FLOAT NULL,"
                    "i94visa  FLOAT NULL,"
                    "count FLOAT NULL,"
                    "dtadfile INTEGER NULL,"
                    "visapost VARCHAR(4) NULL, "
                     "occup VARCHAR(4) NULL, "
                     "entdepa VARCHAR(4) NULL, "
                     "entdepd VARCHAR(4) NULL, "
                     "entdepu VARCHAR(4) NULL, "
                     "matflag VARCHAR(4) NULL, "
                     "biryear FLOAT NULL,"
                    "dtaddto VARCHAR(255) NULL,"
                    "gender VARCHAR(4) NULL, "
                     "insnum INTEGER NULL,"
                    "airline VARCHAR(4) NULL, "
                     "admnum FLOAT NULL,"
                    "fltno VARCHAR(255) NULL,"
                    "visatype VARCHAR(4) NULL);")

staging_temperature_table_create = ("CREATE TABLE IF NOT EXISTS staging_temperature ("
                    "dt VARCHAR(255) NOT NULL, "
                     "avg_temperature FLOAT NULL,"
                    "avg_temperature_uncertainty FLOAT NULL,"
                    "City VARCHAR(255) NOT NULL, "
                     "country VARCHAR(255) NOT NULL, "
                     "latitude VARCHAR(255) NULL,"
                    "longitude VARCHAR(255) NULL);")

staging_citydemo_table_create = ("CREATE TABLE IF NOT EXISTS staging_citydemo ("
                    "City VARCHAR(255) NOT NULL, "
                     "State VARCHAR(255) NOT NULL, "
                     "median_age FLOAT NULL,"
                    "male_population FLOAT NULL,"
                    "female_population  FLOAT NULL,"
                    "total_population FLOAT NULL,"
                    "num_veterans FLOAT NULL,"
                    "foreign_born  FLOAT NULL,"
                    "avg_household_size FLOAT NULL,"
                    "state_code VARCHAR(4) NULL,"
                    "race VARCHAR(255) NULL, "
                     "count FLOAT NULL);")


citydemo_table_create = ("CREATE TABLE IF NOT EXISTS city_demo ("
                     "citydemo_id BIGINT IDENTITY(0,1)  NOT NULL, "
                    "City VARCHAR(255) NOT NULL, "
                     "State VARCHAR(255) NOT NULL, "
                     "median_age FLOAT NULL,"
                    "male_population FLOAT NULL,"
                    "female_population  FLOAT NULL,"
                    "total_population FLOAT NULL,"
                    "num_veterans FLOAT NULL,"
                    "foreign_born  FLOAT NULL,"
                    "avg_household_size FLOAT NULL,"
                    "state_code VARCHAR(4) NULL);")
                     
cityrace_table_create = ("CREATE TABLE IF NOT EXISTS city_race ("
                       "cityrace_id BIGINT IDENTITY(0,1)  NOT NULL, "
                        "citydemo_id BIGINT NOT NULL, "
                       "race VARCHAR(255) NULL, "
                       "count FLOAT NULL);")

i94_table_create = ("CREATE TABLE IF NOT EXISTS i94 ("
                    "i94_id BIGINT IDENTITY(0,1) NOT NULL, "
                    "i94yr FLOAT NOT NULL,"
                    "i94mon FLOAT NOT NULL,"
                    "i94cit FLOAT NOT NULL,"
                    "i94port VARCHAR(4) NOT NULL, "
                    "citydemo_id BIGINT NOT NULL, "
                     "arrdate FLOAT NULL,"
                    "i94mode FLOAT NULL,"
                     "depdate FLOAT NULL,"
                    "i94bir FLOAT NULL,"
                    "i94visa  FLOAT NULL,"
                    "dtadfile INTEGER NULL,"
                     "occup VARCHAR(4) NULL, "
                     "biryear FLOAT NULL,"
                    "gender VARCHAR(4) NULL);")


temperature_table_create = ("CREATE TABLE IF NOT EXISTS temperature ("
                                "temperature_id BIGINT IDENTITY(0,1) NOT NULL, "
                    "dt VARCHAR(255) NOT NULL, "
                     "avg_temperature FLOAT NULL,"
                    "avg_temperature_uncertainty FLOAT NULL,"
                    "City VARCHAR(255) NOT NULL, "
                     "citydemo_id BIGINT NOT NULL, "
                     "country VARCHAR(255) NOT NULL, "
                     "latitude VARCHAR(255) NULL,"
                    "longitude VARCHAR(255) NULL);")


# STAGING TABLES

bucket_name = 'udacity-deng-capstone-project'

staging_i94_copy = ("COPY staging_i94 FROM 's3://{}' " +
                       "CREDENTIALS 'aws_iam_role={}' " +
                       "CSV "
                       "IGNOREHEADER 1").format(bucket_name+"/i94_laos.csv", 
                                config.get('IAM_ROLE','ARN'),)


staging_temperature_copy = ("COPY staging_temperature FROM 's3://{}' " +
                       "CREDENTIALS 'aws_iam_role={}' " +
                       "CSV "
                       "IGNOREHEADER 1").format(bucket_name+"/temperature_US.csv", 
                                config.get('IAM_ROLE','ARN'),)


staging_citydemo_copy = ("COPY staging_citydemo FROM 's3://{}' " +
                       "CREDENTIALS 'aws_iam_role={}' " +
                       "CSV " +
                       "DELIMITER ';' "
                       "IGNOREHEADER 1").format(bucket_name+"/us-cities-demographics.csv", 
                                config.get('IAM_ROLE','ARN'),)

# FINAL TABLES

citydemo_table_insert = ("INSERT INTO city_demo ("
                         "City, "
                     "State, "
                     "median_age,"
                    "male_population,"
                    "female_population,"
                    "total_population,"
                    "num_veterans,"
                    "foreign_born,"
                    "avg_household_size,"
                    "state_code) "
                    "SELECT DISTINCT City , "
                     "State, "
                     "median_age,"
                    "male_population,"
                    "female_population,"
                    "total_population,"
                    "num_veterans,"
                    "foreign_born,"
                    "avg_household_size,"
                    "state_code "
                    "FROM staging_citydemo;")

cityrace_table_insert = ("INSERT INTO city_race ("
                         "citydemo_id, "
                     "race, "
                     "count) "
                    "SELECT DISTINCT c.citydemo_id, "
                     "s.race, "
                     "s.count "
                    "FROM staging_citydemo s LEFT JOIN city_demo c ON c.city=s.city;")

temperature_table_insert = ("INSERT INTO temperature ("
                    "dt, "
                     "avg_temperature ,"
                    "avg_temperature_uncertainty,"
                    "city, "
                     "citydemo_id, "
                     "country, "
                     "latitude,"
                    "longitude) "
          "SELECT DISTINCT dt, "
                     "avg_temperature,"
                    "avg_temperature_uncertainty,"
                    "City, "
                     "c.citydemo_id, "
                     "country, "
                        "latitude,"
                    "longitude "
                    "FROM staging_temperature s LEFT JOIN city_demo c ON c.city=s.city;")

i94_table_insert = ("INSERT INTO i94 ("
                    "i94yr,"
                    "i94mon,"
                    "i94cit,"
                    "i94port, "
                      "citydemo_id, "
                     "arrdate,"
                    "i94mode,"
                     "depdate,"
                    "i94bir,"
                    "i94visa,"
                    "dtadfile,"
                     "occup, "
                     "biryear,"
                    "gender) "
          "SELECT DISTINCT "
                    "i94yr,"
                    "i94mon,"
                    "i94cit,"
                    "i94port, "
                      "c.citydemo_id, "
                     "arrdate,"
                    "i94mode,"
                     "depdate,"
                    "i94bir,"
                    "i94visa,"
                    "dtadfile,"
                     "occup, "
                     "biryear,"
                    "gender
                    "FROM staging_i94 s LEFT JOIN city_demo c ON c.city=s.i94port;")

# QUERY LISTS

create_table_queries = [staging_i94_table_create, staging_temperature_table_create, staging_citydemo_table_create, i94_table_create, temperature_table_create, citydemo_table_create,cityrace_table_create]
drop_table_queries = [staging_i94_table_drop, staging_temperature_table_drop, staging_citydemo_table_drop, i94_table_drop, temperature_table_drop, citydemo_table_drop,cityrace_table_drop]
copy_table_queries = [staging_i94_copy, staging_temperature_copy, staging_citydemo_copy]
insert_table_queries = [citydemo_table_insert,cityrace_table_insert, i94_table_insert, temperature_table_insert]