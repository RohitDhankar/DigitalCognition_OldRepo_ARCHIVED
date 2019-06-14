import re , io , os
from .models import *
from django.db.models import Count , Max
from django.conf import settings
import pandas as pd
import json 
from django.shortcuts import redirect

#from settings import * ## Wont Work -- Code below has chained Imports === user = settings.DATABASES['default']['USER']

def returnFunc(request):
    return redirect('dc/call_merged_table_view/')    

def psql_liveConn_Status():
    """
    FOO_## Needs REWORKING @80% Code 
    Trigger a SQL Query in PSQL from Python
    Check status of PSQL conns - LIVE etc.
    """
    from sqlalchemy import create_engine
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )
    engine = create_engine(database_url, echo=False)
    schema_default_public = "public"
    #sql_command = "SELECT count(*) from pg_stat_activity ;" ## Only COUNT of CONNECTIONS / SESSIONS 
    # SOURCE -- SO -- https://stackoverflow.com/questions/54284939/how-to-check-postgresql-session-count
    sql_command = "SELECT * from pg_stat_activity ;" ## All Status of CONNECTIONS / SESSIONS 
    df_for_pg_stat_activity = pd.read_sql(sql_command,engine)
    #df_for_pg_stat_activity.to_csv("pg_stat_activity.csv")
    df_for_pg_stat_activity.to_csv('pg_stat_activity.csv', mode='a', header=False) #
    # FOO_ERROR --- get this into a SQL Table and Persist ---
    # ERROR in getting this to -- front_end HTML JavaScript is --- 
    # the Postgres returned TimeStamp with TIMEZONE -- doesnt get Converted to DataTables.js DATETIME
    
    return df_for_pg_stat_activity



def psql_drop_delete_tables(db_table_name):
    """
    psql_drop_delete_tables
    FOO _## Needs REWORKING @80% Code 
    """
    from sqlalchemy import create_engine
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )
    engine = create_engine(database_url, echo=False)
    #
    import psycopg2
    schema_default_public = "public"
    psql_user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    conn = psycopg2.connect("dbname="+str(database_name)+" "+"user="+str(psql_user)+" "+"password="+str(password)+"")
    conn_cursor = conn.cursor()
    conn_cursor.execute("DROP TABLE"+" "+str(db_table_name)+ ";")
    #
    conn.commit() # <--WE Need COMMIT to actually EXECUTE in DB
    # BELOW-- deletes Record from the DJANGO table / model == csv_document
    #DONE ABOVE == from .models import *
    csv_document.objects.filter(dataset_name=str(db_table_name)).delete()

    return db_table_name


import traceback

def psql_merge_basic(data_table1,data_table2,new_table_name): ## Original 
#def psql_merge_basic(data_table1,data_table2): ## TESTING 
    """
    psql_merge_basic
    FOO_ ## Needs REWORKING @80% Code 
    """
    try:
        from sqlalchemy import create_engine
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']
        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )
        engine = create_engine(database_url, echo=False)
        #
        # schema_default_public = "public"
        # #sql_command = "CREATE TABLE"+" "+str(new_table_name)+" "+"AS (SELECT * FROM"+" "+str(data_table1)+" "+"UNION SELECT * FROM" +str(data_table2)+");"
        #
        import psycopg2
        schema_default_public = "public"
        psql_user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']
        conn = psycopg2.connect("dbname="+str(database_name)+" "+"user="+str(psql_user)+" "+"password="+str(password)+"")
        conn_cursor = conn.cursor()
        #FOO_NOTE______ORIGINAL_QUERY_below_OK                
        conn_cursor.execute("CREATE TABLE"+" "+str(new_table_name)+" "+"AS (SELECT * FROM"+" "+str(data_table1)+" "+"UNION SELECT * FROM"+" "+str(data_table2)+");")
        conn.commit() # <--WE Need COMMIT to actually EXECUTE in DB

        # Actual merge happening above --- 
        # Below just getting a DF from Merged PSQL Table and sending JSON to AJAX in frontend---
        # Now read SQL table int0 Python DF >> DF to JSON >> DataTables.js 
        #sql_command = "SELECT * FROM {}.{} limit {};".format(str(schema_default_public), str(dataset_name),str(limit_records))

        #### Testing OK below --- Uncomment 
    
        sql_command = "SELECT * FROM {}.{};".format(str(schema_default_public), str(new_table_name))
        df_new_table_name = pd.read_sql(sql_command,engine)
        df_new_table_name.to_csv("df_new_table_name.csv")
        #df_new_table_name.to_csv('df_new_table_name.csv', mode='a', header=False) #
        print("-------df_new_table_name.shape-------------",df_new_table_name.shape)
        
        return df_new_table_name #
        # EARLIER TESTING ---- here above - New Table with name == new_table_name , is created but we dont pass anything NEW from here in-- return-- below, we dont need to . 
        # Utily.py funcs  already know the name of the == new_table_name.
        # Just passing it to Populate this - return. 
    except Exception as ex:
        exception_str = "dummy_str"
        exception_str = str(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
    return str(exception_str) 
    
    #
        #EXPLAIN ANALYZE --- Testing 
        #conn_cursor.mogrify("SELECT * FROM"+" "+str(data_table1)+" "+"UNION SELECT * FROM"+" "+str(data_table2)+";")
        #conn_cursor.execute("EXPLAIN ANALYZE SELECT * FROM"+" "+str(data_table1)+" "+"UNION SELECT * FROM"+" "+str(data_table2)+";")
        #Below Hardcoded for Testing ==>>
        #conn_cursor.execute("CREATE TABLE csv_new_table_merge3 AS SELECT * FROM csv_1a UNION SELECT * FROM csv_1abv;")

        #
    # Now read SQL table int0 Python DF >> DF to JSON >> DataTables.js 
    #sql_command = "SELECT * FROM {}.{} limit {};".format(str(schema_default_public), str(dataset_name),str(limit_records))

    #### Testing OK below --- Uncomment 
    """
    sql_command = "SELECT * FROM {}.{};".format(str(schema_default_public), str(new_table_name))
    df_new_table_name = pd.read_sql(sql_command,engine)
    df_new_table_name.to_csv("df_new_table_name.csv")
    #df_new_table_name.to_csv('df_new_table_name.csv', mode='a', header=False) #
    print("-------df_new_table_name.shape-------------",df_new_table_name.shape)
    """
    #return df_new_table_name










"""
## Update -- 16-MARCH-19 -- Not sure if these two lines below are now relevant -- after using PSQL , SqlAlchemy etc etc 
Option -1 - Use Django ORM -- django_queryset next line syntax 'DOT + BACK_SLASH'
Option -2 - Pure SQL Queries --- model_name.objects.raw("SQL QUERY")
"""


def dedupDataORM(model_name,col_name):
    """
    ## Needs REWORKING @80% Code 
    Keep pressing DeDup Button on Template - till RECORDS count stabilizes - doesnt reduce anymore. 
    DeDup use ORM + Regex- not deleting more than 20 Id's or Pk 
    """
    # model_name = news_startup_1 # OK - getting passed in from Views
    # col_name = ORG_Name # OK - getting passed in from Views

    len_ls_all_objects = len(list(model_name.objects.all()))
    print("------------len_ls_all_objects--------------------",len_ls_all_objects)
    dups = model_name.objects.values('ORG_Name').\
    annotate(Count('ORG_Name')).\
    order_by().\
    filter(ORG_Name__count__gt=1)
    #
    dups1 = model_name.objects.filter(ORG_Name__in=[item['ORG_Name'] for item in dups])
    dups_str_for_extract_id = str(dups1)
    #print(dups_str_for_extract_id)
    ls_ids_del = []

    ls_ids_delete = re.findall(r'object (.*?)>,',dups_str_for_extract_id,re.M|re.S)
    for k in range(len(ls_ids_delete)):
        str_pk_id = re.sub(r'\(','',str(ls_ids_delete[k]))
        str_pk_id = re.sub(r'\)','',str(str_pk_id))
        ls_ids_del.append(str_pk_id)
    #dups2 = model_name.objects.filter(id__in=[item['id'] for item in dups]) ## NOthing Called id ??
    for k in range(len(ls_ids_del)):
        model_name.objects.filter(id=ls_ids_del[k]).delete() ## Deletes the PK == ID 
        print("------------DELETED------------",ls_ids_del[k])
    
    len_ls_all_objects1 = len(list(model_name.objects.all()))
    print("------------len_ls_all_objects1--------------------",len_ls_all_objects1)
    return dups #dedupData_DF_to_beSavedBack_In_Model


## FOO_ERROR--- if we create a --- dedupDataSQL --- SQL dependent Function in place of SQL Inde[endent and ORM Dependent 
# We may have to change the FUNC if we Change from SQLITE to PostGreSQL etc 

# def dedupDataSQL(SQL_Query):
#     return dedupDataSQL_return



