#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sqlalchemy import create_engine

pg_user = 'root'
pg_pass = 'root'
pg_host = 'localhost'
pg_port = 5432
pg_db = 'ny_taxi'


year = 2021
month = 1


# In[3]:



# In[4]:


# In[17]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'


engine = create_engine('postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates
)


# In[10]:


df.head()


# In[11]:


get_ipython().system('uv add sqlalchemy')


# In[13]:


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')


# In[14]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[15]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[18]:


len(df)


# In[27]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[23]:


from tqdm.auto import tqdm


# In[20]:


for df_chunk in df_iter:
    print(len(df_chunk))


# In[21]:


df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[28]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




