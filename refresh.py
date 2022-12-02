import os
import os.path
import datetime
import config

#############################################################################################

# ENTER NAME OF DATALAKE DATABASE
config.db_name = 'colonoscopy_registry' 

# Files in the '/table' firectory contain sql that are used to create tables in the database.
# Table names in the database are the file names.

# ENTER NAMES OF FILES THAT DEFINE TEMP TABLES THAT ARE DELETED AT THE END OF THE REFRESH
temp_tables = [ ] 

# ENTER NAMES OF TABLES IN ORDER THAT WILL BE DONE FIRST
# ANY TABLES NOT LISTED HERE WILL BE REFRESHED IN RANDOM ORDER
base_tables = [ 
  'exam', 'patient'
]

#############################################################################################

def main():
  if not config.refresh_log_exists():
    config.initialize_refresh_log()

  if os.path.exists('refreshing'):
    return 'ERROR: Refresh file already exists'

  with open('refreshing', 'w') as f:
    f.write(str(datetime.datetime.now()))
  
  # create base tables
  # create the rest of the tables
  for table in base_tables + [x for x in config.tables if x not in base_tables]:
    config.drop_and_create(table)
    
  # delete temp tables
  for table in temp_tables:
    config.drop_table(table)

  os.remove('refreshing')

if __name__ == '__main__':
    main()
