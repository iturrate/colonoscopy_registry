# RegistryDB
Create and refresh a standard base registry for a custom cohort of patients.

**Registry creation steps:**

1. request creation of a new database and of a database_wksp database in the datalake 
    * https://collibraprod.nyumc.org/dashboard
2. define the list of users who need access to read/write and users who need read-only for both and request:
    * https://nyu-amc.ivanticloud.com/Modules/SelfService/#serviceCatalog/request/039CCFC23D484150B69DEF76F48EF0D5
3. clone this repo, modify refesh_db.py:
    * edit 'db_name' to be the name of the new database
    * identify any temp_tables and the base_tables in the table directory
    * modify the sql in the table files in the table directory
7. run refresh.py
8. review the table called refresh_log in the database for timestamps of events
9. if the registry needs regular updating, set up a cron job to run refresh.py

**Registry Customization:**
1. customize existing tables by editing files in the 'table' directory
2. add new tables to the registry by creating new files in the table directory 
    * name the file the name of the new table
    * the new file contains sql that defines the new table
    * refer to this registry's database name as DATABASE in the sql files 
