import openpyxl
import pandas as pd
from dateutil import parser

# TODO 1: Set variables saved from credentials.csv
file_path = "./app reference/reference.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
pathParsed = reference["paths"]["B5"].value
pathMainFile = reference["paths"]["B4"].value

reference.close()

# did not inherit from Report due to a chance of cyclical dependency


class Updater:
    def __init__(self, reportobj):
        self.report_name = reportobj.report_name
        # self.start_date = reportobj.requested_report_start_date
        # self.end_date = reportobj.requested_report_end_date
        self.path_parsed = pathParsed
        self.csv_file = pathParsed + reportobj.filename_string + ".csv"
        self.main_file = reportobj.main_file

    def update_SP_AP_D(self):
        main_df = pd.read_csv(self.main_file, encoding='UTF-8')
        # print(main_df)
        new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
        new_dates = new_df['Date'].unique()

        main_df_filtered = main_df[~main_df['Date'].isin(new_dates)].dropna(how='all')
        updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

        print("success updating main file")
        updated_df.to_csv(self.main_file, encoding='utf-8', index=False)

    def update_SB_CM_D(self):
        print("reached update")






