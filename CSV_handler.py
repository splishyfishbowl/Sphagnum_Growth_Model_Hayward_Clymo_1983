import numpy as np
import pandas as pd
import os
from pathlib import Path

class CSV_handler:
    def __init__(self):
        print(f'CSV_handler.init(): Initiated CSV_handler.')

    ########## CSV Handling #####################################
    def get_data_frame_from_csv(self, path_to_csv:str):
        '''
        The dataframe will look like this:
                Time Abstich GOK
        0    2025-11-08 21:00:00   -75.15 mm
        1    2025-11-09 01:00:00   -75.71 mm
        2    2025-11-09 05:00:00   -76.20 mm
        3    2025-11-09 09:00:00   -76.12 mm
        4    2025-11-09 13:00:00   -75.82 mm
        ..                   ...         ...
        168  2025-12-07 21:00:00     9.68 mm
        169  2025-12-08 01:00:00    19.57 mm
        '''

        path = Path(path_to_csv)
        # expanduser if possible
        path_to_csv = os.path.expanduser(path_to_csv)

        # Check path
        if not os.path.exists(path_to_csv):
            print(f'Statistics.get_data_frame_from_csv(): path did not exist. Maybe check for spelling.')
        
        # Get csv
        water_table_data = pd.read_csv(path_to_csv)

        print(f'\nStatistics.get_data_frame_from_csv(): Succesfully loaded csv table. path: {path_to_csv}\n')

        # return
        return water_table_data
    
    def get_daily_dataframe_and_array_from_mm_csv(self, path_to_csv, timeidentifier:str='Time', valueidentifier: str ='Abstich GOK'):
        '''
        ## RETURN + DESCRIPTION
        Will return a array with values of water-table-depth in mm and a numpy array with all the water_tables in cm.
        If there are multiple values for one day, the average is used for the day.
        Missing days will be approximated by linear interpolation.

        The dataframe will look like this:
                Time Abstich GOK
        0    2025-11-08 21:00:00   -75.15 mm
        1    2025-11-09 01:00:00   -75.71 mm
        2    2025-11-09 05:00:00   -76.20 mm
        3    2025-11-09 09:00:00   -76.12 mm
        4    2025-11-09 13:00:00   -75.82 mm
        ..                   ...         ...
        168  2025-12-07 21:00:00     9.68 mm
        169  2025-12-08 01:00:00    19.57 mm
        '''
        # load Dataframe
        dataframe = self.get_data_frame_from_csv(path_to_csv=path_to_csv)

        # make time formats in the first column
        dataframe[timeidentifier] = pd.to_datetime(dataframe[timeidentifier])

        # ensure string
        col = dataframe[valueidentifier].astype(str)

        print(f'col before string casting and unit deletion \n {col}')

        # remove units (mm, µm, m) and put spaceholder
        # save in a copy
        col = col.str.replace(' mm', '', regex=False)
        col = col.str.replace(' µm', '', regex=False)
        col = col.str.replace(' m', '', regex=False)

        # convert to float
        col = col.astype(float)
        

        # say, where which unit was saved
        col_mm  = dataframe[valueidentifier].str.contains(' mm', regex=False)
        col_um  = dataframe[valueidentifier].str.contains(' µm', regex=False)
        col_m   = dataframe[valueidentifier].str.contains(' m ',  regex=False) # if no blank after the m, then it also matches the mm case
        
        print(f'col_mm:\n{col_mm}')
        print(f'type(col): {type(col)}')

        # convert to cm
        col[col_mm] /= 10          # mm → cm
        col[col_um] /= 10000       # µm → cm
        col[col_m]  *= 100         # m → cm

        # finally save the calculations
        print(f'dataframe before: {dataframe}')
        dataframe[valueidentifier] = col

        print(f'dataframe after: {dataframe}')

        # make all values that were measured the same day to one (take the average)
        df_daily = (
            dataframe.groupby(dataframe[timeidentifier].dt.normalize())[valueidentifier]
                        .mean()
                        .reset_index()
                    )
        
        # check if there are days that were not covered
        df_daily = df_daily.set_index(timeidentifier)

        full_index = pd.date_range(df_daily.index.min(),
                                df_daily.index.max(),
                                freq="D")

        df_reindexed = df_daily.reindex(full_index)

        # Here we get all the dates that are missing
        missing_days = df_reindexed[df_reindexed.isna().any(axis=1)]

        if len(missing_days.keys()) != 0:
            print(f'CSV_handler.get_daily_dataframe_and_array_from_mm_csv(): missing dates\n{missing_days}')

            # fill missing dates by averages
            df_daily = df_reindexed.interpolate(method='time')

            # make numpy array from the daily water-table depths
            # As they are in mm we convert them to cm
            wtd_in_cm_np_array = df_daily[valueidentifier].to_numpy() 

            # return filled array
            return df_daily, wtd_in_cm_np_array
        
        else:
            # print that no interpolation was neccessary
            print(f'CSV_handler.get_daily_dataframe_and_array_from_mm_csv(): SUCCESS No interpolation was neccessary because no dates were missing')

            # make numpy array from the daily water-table depths
            # As they are in mm we convert them to cm
            wtd_in_cm_np_array = df_daily[valueidentifier].to_numpy()

            # return
            return df_daily, wtd_in_cm_np_array




       