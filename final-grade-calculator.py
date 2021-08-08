#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 00:00:00 2020

@author: Usman Naz
"""


import pandas as pd

pd.set_option('mode.chained_assignment', 'raise')


def apply_scheme(filenam,  # filename
                 num_stu,  # number of students
                 num_HWs,  # number of homeworks
                 HW_tots,  # list of homework totals
                 mid_tot,  # midterm total
                 fin_tot,  # final total
                 scheme1 = {'HW': 35, 'Midterm': 30, 'Final': 35},
                 scheme2 = {'HW': 35, 'Midterm':  0, 'Final': 65}
                 ):

    assert num_HWs == len(HW_tots)

    # create initial DF with top 5 rows deleted, 
    # extra rows at the bottom deleted,
    # section colomn deleted,
    # accounted for all missing values (na_values)
    df = pd.read_excel(filenam, skiprows = [0,1,2,3,4,5], nrows = num_stu, usecols = deleteDueDateCol, 
                      na_values = ['', ' ', '  ']) 
    
    # convert data types 
    df = df.convert_dtypes()
    
    # only enrolled students included 
    df = df[df['Status'] == 'Enrolled'] 
    
    # delete enrolled status colomn
    df = df.iloc[:, 1:]
    
    # use UID to index rows
    df = df.set_index("UID")

    # leave index col name blank
    df.index.name = None
    
    # change column names before adding HWA, SM, SF, Scheme 1, Scheme 2 cols
    col_names = ['Name']
    for i in range(1, num_HWs+1):
        hw_name = 'HW' + f'{i}'
        col_names.append(hw_name)
    col_names.append('Midterm')
    col_names.append('Final')
    col_names.append('Best')
    df.columns = pd.Index(col_names)
    
    # replace na values with 0
    df = df.fillna(0)
    
    # add HWA column
    df.insert(num_HWs+1, column = 'HWA', value = 0)
    
    # add SM column
    df.insert(num_HWs+1+2, column = 'SM', value = 0)
    
    # add SF column
    df.insert(len(df.columns)-1, column = 'SF', value = 0)
    
    # add Scheme 1 col
    df.insert(len(df.columns)-1, column = 'Scheme 1', value = 0)
    
    # add Scheme 2 col
    df.insert(len(df.columns)-1, column = 'Scheme 2', value = 0)
    
    # change type of numbers to float
    df.iloc[:, 1:] = df.iloc[:, 1:].astype('float64')
    
    # add up total percentage of hws and store in HWA col
    # and take the average with num_HWs
    for i in range(1, num_HWs+1):
        df['HWA'] += (df.iloc[:, i]/HW_tots[i-1])*100.0
    df['HWA'] = df['HWA']/num_HWs
    
    # store midterm percentages in SM col
    df['SM'] = (df['Midterm']/mid_tot)*100.0
    
    # store final percentages in SF col
    df['SF'] = (df['Final']/fin_tot)*100.0
    
    # calculate Scheme 1 grade 
    df['Scheme 1'] = ((scheme1['HW']*df['HWA']) + (scheme1['Midterm']*df['SM']) + (scheme1['Final']*df['SF']))/100.0
    
    # calculate Scheme 2 grade 
    df['Scheme 2'] = ((scheme2['HW']*df['HWA']) + (scheme2['Midterm']*df['SM']) + (scheme2['Final']*df['SF']))/100.0

    # store better grade of the 2 schemes in Best col
    df['Best'] = df.iloc[:, (len(df.columns)-3):(len(df.columns)-1)].max(axis = 1)
    
    # sort values in Best in descending order
    df = df.sort_values(by=['Best'], ascending = False)
    

    # gr = pd.read_excel(io = filenam)
    return df


# helper function for usecols parameter to delete Section col
def deleteDueDateCol(col_name):
    if col_name == "Due Date:":
        return False
    else:
        return True



gr = apply_scheme(filenam = 'sample-grades.xlsx',
                  num_stu = 18,
                  num_HWs = 4,
                  HW_tots = [10, 10, 12, 14],
                  mid_tot = 40,
                  fin_tot = 50,
                  scheme1 = {'HW': 0, 'Midterm': 0, 'Final': 100},
                  scheme2 = {'HW': 0, 'Midterm':  50, 'Final': 50})

print(gr)


# Best to work in Jupyter Notebook
# where typing gr and pressing "shift, enter"
# displays the dataframe in a pretty format.
