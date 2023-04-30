# %%
import csv
import math
import pandas as pd
import numpy as np
import datetime

# %%
file_path1 = r'C:\Users\Maaba\Desktop\Tests\Test009\iMotions_test009.csv'
file_path3 = r'C:\Users\Maaba\Desktop\Tests\Test009\eSense_Skin_Response_data_from_20.04.23_14_43_43_5Hz.csv'

# %%
SHIFT_IN_SEC = 0

# Open the CSV file
with open(file_path1, 'r', encoding='utf-8') as file:
    

    # Create a CSV reader object, on the file that we have opened
  
    csv_reader = csv.reader(file)

    # Read the 25 first rows because they are not interesting
    for i in range(24):
        current_row = next(csv_reader)

    header_row = next(csv_reader) #take row 26, as the header row

    fear_column = header_row.index('Fear') #find the index of the 'Fear' column
    timestamp_column = header_row.index('Timestamp') #find the index of the 'timestamp' column

    # define empty lists to hold all the data we'te going to read
    all_timestamps = []
    all_fears = []
    
    for row in csv_reader:
        try:
            all_timestamps.append(float(row[timestamp_column]) / 1000 - SHIFT_IN_SEC * 1000) #add to the timestamps the value from each row, after convertion to int
            all_fears.append(float(row[fear_column])) #add to the fears the value from each row, after convertion to float
        except:
            print('I failed at: {}'.format(row)) #for problematic rows, print the rows

    first_timestamp = int(all_timestamps[0]) #this is the first timestamp
    last_timestamp = int(all_timestamps[-1]) #this is the last timestamp
    print('\nFirst timestamp is: {}, last is: {}'.format(first_timestamp, last_timestamp))

    all_fears = np.array(all_fears) / 100 #max(all_fears)*0.6#normalize all the feats (our 'Y' axis) by the largest value, for them to be from 0 to 1



# %%
NUMBER_OF_ROWS_TO_SKIP = 27
TIME_TO_SHIFT_IN_SEC = 0
TIME_TO_CUT_FROM_THE_END_SEC = 100  #if needed
     
with open(file_path3, 'r', encoding='utf-8') as file1:

    # Create a CSV reader object
    csv_reader = csv.reader(file1,delimiter=';')
    for i in range(NUMBER_OF_ROWS_TO_SKIP):
        current_row = next(csv_reader) #skip 26 rows

    header_row = next(csv_reader) #take row 26, as the header row
    
    second_column = header_row.index('SECOND') #find the index of the 'timestamp' column
    microsiemens_column = header_row.index('MICROSIEMENS') #find the index of the 'Fear' column

    # define empty lists to hold all the data we'te going to read
    all_seconds = []
    all_microsiemens = []
    
    for row in csv_reader:
        # try:
        all_seconds.append(float(row[second_column].replace(',', '.')) - TIME_TO_SHIFT_IN_SEC*1000) #add to the timestamps the value from each row, after convertion to int
        all_microsiemens.append(float(row[microsiemens_column].replace(',', '.'))) #add to the microsimens data the value from each row, after convertion to float
        # except Exception as e:
        #     print(e)
        #     print('I failed at: {}'.format(row)) #for problematic rows, print the rows
    
    print(f'First timestamp is: {all_seconds[0]}, last is: {all_seconds[-1]}')
    print(len(all_microsiemens))
    
   
    all_seconds = all_seconds[:-TIME_TO_CUT_FROM_THE_END_SEC*5]              #cutting time from the end if needed
    all_microsiemens = all_microsiemens [:-TIME_TO_CUT_FROM_THE_END_SEC*5]    #cutting time from the end if needed (can be used for normalization exluding specific time)
    
 #NORMALIZATION
    min_val = np.min(all_microsiemens)
    max_val = np.max(all_microsiemens)

# Apply min-max normalization to each data point
normalized_microsimens = ((all_microsiemens - min_val) / (max_val - min_val))

# %%
all_timestamps = all_timestamps[1:]
print(all_timestamps)

data = {'time': [all_seconds], 'name': [all_microsiemens]}
df = pd.DataFrame(data)
print(df)

all_seconds = list(zip(*[all_seconds]))

# Print the vertical list
print(all_seconds)



# %%
data = {'time': [all_seconds], 'name': [all_microsiemens]}
df = pd.DataFrame(data)
print(df)

# %%

all_seconds = list(zip(*[all_seconds]))

# Print the vertical list
print(all_seconds)


# %%


# %%
df = pd.DataFrame(all_seconds, columns = ["Time"])
df

# %%
list(zip(all_seconds, all_microsiemens))

# %%
GSR = pd.DataFrame(list(zip(all_seconds, all_microsiemens)))
resampled_GSR = GSR.resample('30ms').mean().ffill()
GSR

# %%
gsr = GSR.rename(columns={0: 'Timestamp', 1: 'Microsiemens'})
gsr

# %%
gsr['Timestamp'] = gsr['Timestamp'].str[0].str[0]
gsr

# %%
iMotions = pd.DataFrame(list(zip(all_timestamps, all_fears * 100)))
iMotions

# %%
iMotions = iMotions.rename(columns={0: 'Timestamp', 1: 'Fear'})
iMotions

# %%
# Convert the 'Duration' column to a timedelta column
iMotions['Timestamp'] = pd.to_timedelta(iMotions['Timestamp'], unit='S')

# Print the updated dataframe
print(iMotions)


# %%
iMotions['Timestamp'] = iMotions['Timestamp'].astype(str)

# remove the "days" substring from the duration column
iMotions['Timestamp'] = iMotions['Timestamp'].apply(lambda x: x.replace('days ', ''))
iMotions

# %%
iMotions['Timestamp'] = iMotions['Timestamp'].apply(lambda x: x[1:])
iMotions


# %%
gsr

# %%
iMotions

# %%



