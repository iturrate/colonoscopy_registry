import datetime
import re

##########################################################################  

from os import listdir
from os.path import isfile, join
from pathlib import Path
table_path = 'table/'
tables = [f for f in listdir(table_path) if isfile(join(table_path, f))]

def get_sql_from_file(table):
  sql = Path(table_path+table).read_text()
  sql = re.sub('DATABASE',db_name,sql)
  return sql

##########################################################################  

from impala.dbapi import connect

connection = connect(
  host='cdhprod.nyumc.org',
  port=21050,
  auth_mechanism='GSSAPI',
  kerberos_service_name='impala',
  use_ssl=True,
  database='cogito'
)

def connect():
  return connection.cursor()

##########################################################################  

datalake = connect()
db_name = ''

def drop_and_create(table):
  drop_table(table)
  create_table(table)
  
def drop_table(table):
  try:
    datalake.execute('drop table '+db_name+'.'+table)
  except:
    log_event('Drop Error',table,0)

def create_table(table):
  sql = get_sql_from_file(table)
  datalake.execute('create table '+db_name+'.'+table+' as '+sql)
  log_event('Table Refresh',table,str(row_count(table)))

def row_count(table):
  datalake.execute("select count(*) counter from "+db_name+'.'+table)
  result = datalake.fetchone()
  return result[0]

##########################################################################  

def refresh_log_exists():
  try:
    datalake.execute('select * from '+db_name+'.refresh_log')
  except:
    return False
  return True
  
def initialize_refresh_log():
  datalake.execute("create table "+db_name+""".refresh_log ( 
                   event_timestamp varchar, 
                   event_description varchar,
                   table_name varchar,
                   row_count bigint
                  )""")
  log_event('Create Log','refresh_log',0)
  
def log_event(description,table,count):
  datalake.execute(
    'insert into '+db_name+".refresh_log values ( '"+str(datetime.datetime.now())+"', '"+description+"', '"+table+"', "+str(count)+" )"            
  )

##########################################################################  

