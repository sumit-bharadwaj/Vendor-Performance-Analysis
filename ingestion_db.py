import pandas as pd
import os # used to get the list of file names inside a folder
from sqlalchemy import create_engine
import logging
import time
# logging: used to track/record the steps and errors happening in the code
# different from print() because:
#   - print() only shows output in the console (lost once Jupyter is closed)
#   - logging saves permanently to a file, so you can check it later
#   - automatically adds a timestamp and severity level (INFO/WARNING/ERROR)
#   - lets you know which file loaded successfully and which failed — without re-running everything
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a"
)

engine = create_engine('mysql+pymysql://root:password@localhost:3306/DataBaseName') #connect with DataBase(MYSQL WORKBENCH)
def ingest_db(df, table_name, engine):
    ''' this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con=engine, if_exists ='replace', index = False, chunksize=5000, method='multi') # chunksize-inserts in batches of 5000 rows to avoid MemoryError

# read csv file 
def load_raw_data():
    '''this function will load the csv as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)# in this table name is file name but remove .csv so use file[:-4]
    end = time.time()
    total_time = (end-start)/60
    logging.info('-----------------Ingestion Complete--------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')
if __name__ == '__main__':
   load_raw_data()