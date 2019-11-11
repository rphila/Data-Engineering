# Laotian Immigration Patterns
- This project will investigate trends of Laotian immigration to the US in 2016. Raw datasets on immigration, city temperature and city demographics will be collected, cleaned and uploaded into S3. Then Python and Spark will be used to transform the raw data from S3 into a database schema suitable for analysis in a Redshift data warehouse. 

## Raw Dataset
- The I94 Immigration Data is in SAS7BDAT format and comes from the US National Tourism and Trade Office: https://travel.trade.gov/research/reports/i94/historical/2016.html 
    - _The data dictionary is in the I94_SAS_Labels_Descriptions.SAS file._
- The World Temperature Data is in csv format and comes from Kaggle: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
- The U.S. City Demographic Data is in csv format and comes from OpenSoft: https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/
- The Airport Code Table is a simple csv table of airport codes and corresponding cities. It comes from here: https://datahub.io/core/airport-codes#data

### Data Model

 ![star schema](https://github.com/rphila/Data-Engineering/blob/master/Capstone_Project/img/star_schema.png)
  
  - Table description:
    - `city_demo`: dimension table containing list of US cities and their demographics information
    - `city_race`: dimension table containing list US cities and information about race counts
    - `temperature`: fact table containing temperature data for a city at a certain date
    - `i94`: fact table containing records of immigration information
    

## Repo Content      
### Python Scripts
_Note: These scripts reference values for resources from a config file: dwh.cfg_

- `data_cleaning.py`: cleans the raw dataset (i.e. remove NaN, duplicates)
- `upload_to_S3.py`: uploads cleaned dataset to S3
- `sqlqueries.py`: contains SQL scripts to create redshift tables and insert data into them (used by `etl.py`)
- `etl.py`: main script to __extract__ data from S3 and stage on redshift, __transform__ them into required formats for the data model, and then __load__ them into their final star shema on redshift.

### Jupyter Notebooks
- `AWS_setup.ipynb`: workbook setting up the resources that will be used (redshift cluster, IAM role) - which need to be added to the `dwh.cfg` file
- `Capstone_Project.ipynb`: workbook containing exploratory analysis to document the purpose of the project and prepare the data pipeline

### Cleaned Dataset
- `temperature_US.csv`: Cleaned and filtered temperature data
- `i94_laos.csv`: Cleaned and filtered immigration data
- `us-cities-demographics.csv`: raw us cities demographics data (dataset will be normalized during transformation into redshift tables)
- `airport-codes_csv.csv`: raw airport codes (will be used to join local_code with i94port to get municipality as city)

## Running the pipeline
### Prerequisite
 - Redshift cluster and IAM role for readonly access to S3 should be setup (see `AWS_setup.ipynb`)
 - Python3 to run .py scripts

### Instruction
 - Run `data_cleaning.py`
 - Run `upload_to_S3.py`
 - Run `etl.py` _(Requires going through AWS_Setup.ipynb to setup Redshift cluster first)_
 - Run through commands in `test.ipynb` to verify all tables in redshift has been populated with the json data
 

## Example Analysis:
#### Query

```# Top city destination for Laotion immigrants in 2016

%%sql SELECT city, state, count(i.*) AS cnt
FROM i94 i 
LEFT JOIN city_demo c ON i.citydemo_id=c.citydemo_id
GROUP by city, state
ORDER BY cnt DESC;
```

#### Results
```
city, state: cnt
Seattle, Washington:7
Houston, Texas:2
Detroit, Michigan:2
Atlanta, Georgia:2
Dallas, Texas:2
```
### Findings

3 of the top 5 cities for Laotian immigrants are to destinations with a large Laotion populatian: https://en.wikipedia.org/wiki/Laotian_Americans#Demographics

These include Seattle, Washington and Houston/Dallas, Texas. This may indicate that Laotian immigrants seek US destinations where they can  find an existing Laotiancommunity.

