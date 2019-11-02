import pandas as pd
import numpy as np
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf


# clean and normalize city demographics (Race and Count are columns 10-11)
#df_citydemo = pd.read_csv('us-cities-demographics.csv', delimiter=';')
#df_citydemo_filt = df_citydemo.iloc[:,:10].drop_duplicates()
#df_citydemo_race = df_citydemo.iloc[:,10:].drop_duplicates()
#df_citydemo_filt.to_csv("city_demo.csv", index=False)
#df_citydemo_race.to_csv("city_race.csv", index=False)

# clean city temperature data 
df_temp = pd.read_csv('../../data2/GlobalLandTemperaturesByCity.csv')
df_temp_filt = df_temp[(df_temp['Country']=='United States') & (pd.notna(df_temp['AverageTemperature'])) 
                       & (df_temp['dt'] > '2010-01-01') & (df_temp['dt'] < '2017-01-01')].drop_duplicates()
df_temp_filt.to_csv("temperature_US.csv", index=False)


# clean immigration data

# create a spack session
from pyspark.sql import SparkSession
spark = SparkSession.builder.\
config("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11")\
.enableHiveSupport().getOrCreate()

df = pd.DataFrame()
# skip june dataset due to mismatch in column count found during exploration of the raw dataset
month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
for m in month_list:  
    filepath = '../../data/18-83510-I94-Data-2016/i94_'+m+'16_sub.sas7bdat' 
    
    # Read data into Spark
    df_i94 = spark.read.format('com.github.saurfang.sas.spark').load(filepath)

    # Filter for entires where i94cit is 203 (LAOS)
    df_i94_filt = df_i94.filter(df_i94.i94cit.isin(203))
    print(m, (df_i94_filt.count(), len(df_i94_filt.columns)))
        
    if m == 'jan':
        df = df_i94_filt.toPandas()
    else:
        df.append(df_i94_filt.toPandas(), ignore_index=True)

df.to_csv("i94_laos.csv", index=False)