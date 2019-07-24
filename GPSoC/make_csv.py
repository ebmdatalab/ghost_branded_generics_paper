import glob
import re
import pandas as pd
import string
import dateparser
import os
from tqdm import tqdm_notebook


cwd = os.getcwd()
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)


dates = []
df = pd.DataFrame()
for name in tqdm_notebook(glob.glob("*xls*")):
    d = re.match(r".*hare (?:- )?(.*)\.x", name).groups()[0]
    if d[-1] not in string.digits:
        d = d[:-1]  # remove the version letter
    d = d.replace(" 20", " ").replace(" v2", "")
    d = d[:-2] + "20" + d[-2:]
    dt = dateparser.parse(d, locales=['en-GB'], settings={'PREFER_DAY_OF_MONTH': 'first'})
    this_df = pd.read_excel(name)
    this_df['Date'] = dt
    #print(this_df.columns)
    this_df = this_df.rename(index=str, columns={"Principal Supplier": "Principal_Supplier",
                                                 "Principal System": "Principal_System"})
    #this_df['Principal Supplier'] = .rstrip(' (GPSoC)')

    df = df.append(this_df[['Date', 'ODS', 'Principal_Supplier', 'Principal_System']])
#df.to_csv("complete.csv")
df.to_gbq('alex.vendors', project_id='ebmdatalab',if_exists='replace')
os.chdir(cwd)


# feb 2018 is missing