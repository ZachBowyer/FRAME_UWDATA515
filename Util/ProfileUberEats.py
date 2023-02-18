"""
Test file to get some information about the uber eats kaggle dataset.
Information located on the top level readme.md file also used excel. 
This dataset is located at: 
https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus?resource=download
"""
import pylint
import pandas as pd

df = pd.read_csv('../data/UberEats/restaurants.csv')
print(df.head())

#Get percent of dataset with null values for each column:
for columnName in df.columns.values:
    null_list = (df[columnName].isnull())
    countnull = 0
    countnotnull = 0
    for isratingnull in null_list:
        if(isratingnull == True):
            countnull += 1
        else:
            countnotnull += 1
    print("For", columnName, countnull, "/", countnull+countnotnull, countnull/(countnull+countnotnull))