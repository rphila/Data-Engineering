# "Sparkify" Data Lake
- This project is a continuation of the data engineering efforts started previously using:

    -- [Postgres Database](https://github.com/rphila/Data-Engineering/tree/master/data_modeling_Postgres) 
    
    -- [Redshift Data warehouse](https://github.com/rphila/Data-Engineering/tree/master/data_warehouse_Redshift)
- As the user and song database grows even more, the data warehouse will now be moved into a data lake, and Spark will be used for data processing. 
    -- The data source will continue to reside in S3 as json files, and the transformed data will now be written to parquet files that are partitioned in table directories on S3. Futher analytics can be done using tools such as AWS Athena.

- The ETL process will be adjusted as follows:
   - __Extract__ json data from files in S3 after reading it into Spark
   - __Transform__ the data using Spark
   - __Load__ the data back into S3 as parquet files containing the set of dimensional tables it will transform into
 

## Repo Content      
### Python Scripts
_Note: These scripts reference values for resources from a config file: dl.cfg_
- `etl.py`: main script to __extract__ json data from S3, __transform__ them into dimention tables using Spark, and then __load__ them back into S3 as parquet files.

### Jupyter Notebooks
- `etl.ipynb`: experimental workbook exploring the etl scripts

## Running the pipeline
### Instructions
 - Python3 to run .py scripts
 - AWS keys to connect to S3 
 
    -- Fill in AWS access and secret keys into _dl.cfg_ file
    
    -- Replace *output_data* with path to desired S3 output location in the main() function of _etl.py_
 - Run `etl.py`
