db = sys.argv[1]

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

datalake = connect()

#############################################################################################

# ENTER NAME OF DATALAKE DATABASE
db_name = sys.argv[1]
datalake.execute("select * from "+db_name+"_registry.refresh_log where table_name = 'patient' order by event_timestamp desc")
result = datalake.fetchone()
print('ZZZZZ')
timestamp = result[0]
timestamp, dump = timestamp.split('.')
print(timestamp+' with '+str(result[3])+' total patients')
