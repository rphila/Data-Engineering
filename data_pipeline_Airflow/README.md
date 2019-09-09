# "Sparkify" Data Pipeline
- This project is a continuation of the data engineering efforts started previously using:

    -- [Postgres Database](https://github.com/rphila/Data-Engineering/tree/master/data_modeling_Postgres) 
    
    -- [Redshift Data warehouse](https://github.com/rphila/Data-Engineering/tree/master/data_warehouse_Redshift)

    -- [Spark Data processing](https://github.com/rphila/Data-Engineering/tree/master/data_lake_Spark)

- Thus far, the current ETL process utlizes aws cloud services, and transforms json data from S3 to Redshift when running a python script. The next step is to utilize Apache Airflow to automate this pipeline and intoduce tools to monitor it.
 
- The Airflow Data Pipeline will consist of custom operators to perform ETL tasks that:
   - Extract the json data from S3 into staging
   - Transform and load the data into a data warehouse
   - Run data quality checks against the transformed data
 
 ![Airflow Pipeline](https://github.com/rphila/Data-Engineering/blob/master/data_pipeline_Airflow/img/example-dag.png)
  
## Prerequisite
 - Python3 
 - Airflow installation `pip3 install apache-airflow`
 - AWS keys to connect to S3/Redshift

### Configure AWS credentials in Airflow UI
 - Connect to airflow UI
 	-- `/opt/airflow/shart.sh`
 	--  http://localhost:8080
 - Goto Admin -> Connections -> Create:
 - AWS Connection:
 	-- Conn Id = aws_credentials
 	-- Conn Type = Amazon Web Services
 	-- Login = <AWS Access Key ID>
 	-- Password = <AWS Secret Access Key>
  - Redshift Connection:
 	-- Conn Id = redshift
 	-- Conn Type = Postgres
 	-- Host = <endpoint of Redshift cluster>
 	-- Schema = dev
 	-- Login = awsuser
 	-- Password = <Password created when launching redshift cluster>
    -- Port = 5439


## Repo Content      
- airflow
	-- dags: contains all the imports and tasks to run
	-- plugins/operators: resuable, custom defined airflow operators 
		-- stage_redshift.py: operator to load json data from S3 into redshift staging tables
		-- load_dimension.py: operator that utilizes the SQL helper queries to transform the staged data into dimension tables via truncate-insert (due to small size)
		-- load_fact.py: operator that utilizes the SQL helper queries to transform the staged data into fact tables via appending (due to massive size)
		-- data_quality.py: operatpr that runs checks on data quality with test cases 

	-- plugins/helpers: python script with sql queries for the data transformations
	-- create_tables.sql: SQL to create fact and dimension tables in Redshift

## Running the pipeline
 - Prepare tables in redshift
 	-- Run `create_tables.sql` to create tables in redshift
 - Connect to airflow UI
 	-- `/opt/airflow/shart.sh`
 	--  http://localhost:8080
 - Turn dag on and trigger run

