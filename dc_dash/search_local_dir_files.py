import os
import datetime
import pandas as pd

now = datetime.datetime.now()
#print(now.year, now.month, now.day, now.hour, now.minute, now.second)
#
own_dir_path = "/media/dhankar/Dhankar_1/a3_19/eBrary_Books_Gits_MARCH19"
ls_path_lowestDir = own_dir_path.split('/') # Split on /
len_lowestDir = len(ls_path_lowestDir)
#
str_1 = str(ls_path_lowestDir[len_lowestDir-1])
str_2 = str(ls_path_lowestDir[len_lowestDir-2])
#

file_extension = ".pdf"
file_names_ls = []
path_ls = []
file_extn_ls = [] 
for (paths, dirs, files) in os.walk(own_dir_path):
    for own_file in files:
        if own_file.endswith(file_extension):
            file_names_ls.append(own_file)
            path_ls.append(os.path.join(paths, own_file))
            file_extn_ls.append(file_extension)

df_own_files = pd.DataFrame({'Paths':path_ls,'File Names':file_names_ls,'File Extension':file_extn_ls})
df_own_files.to_csv("Table_of_" + str(file_extension) + "_Files_from_DIR=="+str(str_2)+"_|_"+str(str_1)+"_|_SearchedOn_"+str(now.day)+"-"+str(now.month)+"-"+str(now.year)+"_.csv")
"""
#ERROR# Giving a -- / -- [fwd slash] anywhere in the CSV File name - breaks the code...
Traceback (most recent call last):
  File "dc_dash/search_local_dir_files.py", line 33, in <module>
    df_own_files.to_csv("Table_of_" + str(file_extension) + "_Files_from_DIR__"+str(str_2)+"_/_"+str(str_1)+"__SearchedOn_"+str(now.day)+"-"+str(now.month)+"-"+str(now.year)+"_.csv")
  File "/home/dhankar/anaconda2/envs/dc_info_venv/lib/python3.5/site-packages/pandas/core/frame.py", line 1745, in to_csv
    formatter.save()
  File "/home/dhankar/anaconda2/envs/dc_info_venv/lib/python3.5/site-packages/pandas/io/formats/csvs.py", line 136, in save
    compression=None)
  File "/home/dhankar/anaconda2/envs/dc_info_venv/lib/python3.5/site-packages/pandas/io/common.py", line 400, in _get_handle
    f = open(path_or_buf, mode, encoding=encoding)
FileNotFoundError: [Errno 2] No such file or directory: 'Table_of_.pdf_Files_from_DIR__dhankar_/_Downloads__SearchedOn_10-6-2019_.csv'

"""
