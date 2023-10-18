"""
Module with a functions to read a CSV file containing student term line items 
(STLIs), convert the data to a Python list, then identify instances where an 
initial faciliation was negative and there was a subsequent positive net TA 
line item. The results are then written to a CSV file.

Currently, this only includes MLB data because the Invoice Management data in 
Snowflake does not contain Payment Reason or the initial v recon determination, 
so it would be overly time-consuming to attempt to determine which lines were 
negative on primary versus negative on recon or spend = $0. 

Author: Emily Ciarabellini
Date: 6/16/2023
"""

import csv

def createListfromCSV(csvFileName):
    """
    Takes a csv file as an argument and returns a list.
    File name argument is formatted as a string with .csv. Example: 'overrides.csv'
    """ 
    file=open(csvFileName)
    new_list = list(csv.reader(file))
    return new_list


def writeToCSV(list,filename):
    """
    Takes a list and a CSV file name as parameters and writes the contents of the 
    list to the csv file. File name is a string in quotes ''.
    """
    file = open(filename,'w',newline='')
    wrapper = csv.writer(file, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
    for i in list:
        wrapper.writerow(i)
    file.close()


allSTLIs = createListfromCSV('MLB_STLIs.csv')
resolvedItems = createListfromCSV('Resolved_items.csv')

#add termcode_studentID key to last column of the STLI table
for line in allSTLIs:
    key = line[5] + "_" + line[7]
    line.append(key)

#create lists of positive STLIs and negative initial facilitation STLIs
negativeSTLIs = []
positiveSTLIs = []
for line in allSTLIs:
    if 'NET_TA' in line[0]: #add the header to the list of results
        negativeSTLIs.append(line)
        positiveSTLIs.append(line) 
    elif line[4] == "Initial Facilitation Can't be Negative":
        negativeSTLIs.append(line)
    elif float(line[0]) > 0 and line[4] != "Outside of reconciliation window":
        positiveSTLIs.append(line)

#compare negative and postiive STLI lists 
results1 = []
for n in negativeSTLIs:
    for p in positiveSTLIs:
        if p[-1] == n[-1]:
            results1.append(p)
            results1.append(n)

#remove Bellevue, PG, UMass Global (likely all model A. Verify as needed.)
results2 = []
for r in results1:
    if (r[8] != "Bellevue University") & (r[8] != "Purdue Global") & (r[8] !="University of Massachusetts Global"):
        results2.append(r)

#remove line items already resolved
results = []
count = 0 
for r in results2:
    if [r[11]] not in resolvedItems:
        results.append(r)
        count = count + 1

print(f"There are {count} results.")
writeToCSV(results,'results.csv')
