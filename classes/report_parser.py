import openpyxl
import pandas as pd
import gzip
import json
import numpy as np
from datetime import datetime, timedelta
from dateutil import parser


# TODO 1: Set variables saved from credentials.csv
file_path = "./app reference/reference.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
pathGz = reference["paths"]["B2"].value
pathJson = reference["paths"]["B3"].value
pathParsed = reference["paths"]["B5"].value
pathASIN = reference["paths"]["B6"].value
pathInv = reference["paths"]["B7"].value
pathPrio = reference["paths"]["B8"].value
reference.close()




#TODO just inherit from Report, remove unnecessary attribute init
class Parser:
    def __init__(self, reportobj):
        self.path_gzip_base = reportobj.path_gzip_base
        self.path_parsed = pathParsed
        self.report_name = reportobj.report_name
        self.report_date_obj = datetime.strptime(reportobj.report_date, "%Y%m%d")
        self.report_date = f'{self.report_date_obj.month}/{self.report_date_obj.day}/{self.report_date_obj.year}'
        # self.end_date = reportobj.requested_report_end_date
        self.gz_file = reportobj.gz_file
        self.csv_file = pathParsed + reportobj.filename_string + ".csv"
        self.secondary_file = reportobj.secondary_file

    def parse_SP_AP_D(self):
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))
            df = pd.DataFrame(jsondata)
            pd.set_option('display.max_columns', None)

            df = df.rename(
                columns={"date": "Date", "portfolioId": "Portfolio Id", "campaignBudgetCurrencyCode": "Currency",
                         "campaignName": "Campaign Name", "adGroupName": "Ad Group Name",
                         "advertisedAsin": "Advertised ASIN", "impressions": "Impressions", "clicks": "Clicks",
                         "clickThroughRate": "Click-Thru Rate (CTR)", "costPerClick": "Cost Per Click (CPC)",
                         "spend": "Spend", "sales14d": "14 Day Total Sales ",
                         "purchases14d": "14 Day Total Orders (#)", "unitsSoldClicks14d": "14 Day Total Units (#)", })
            df['Total Advertising Cost of Sales (ACOS) '] = df['Spend'] / df['14 Day Total Sales ']
            df['Total Advertising Cost of Sales (ACOS) '].replace([np.inf, -np.inf], np.nan, inplace=True)
            df['Total Return on Advertising Spend (ROAS)'] = df['14 Day Total Sales '] / df['Spend']
            df['Total Return on Advertising Spend (ROAS)'].replace([np.inf, -np.inf], np.nan, inplace=True)
            df['14 Day Conversion Rate'] = df['14 Day Total Orders (#)'] / df['Clicks']
            df['14 Day Conversion Rate'].replace([np.inf, -np.inf], np.nan, inplace=True)
            arrange_cols = ['Date', 'Portfolio Id', 'Currency', "Campaign Name", "Ad Group Name", "Advertised ASIN",
                            "Impressions", "Clicks", "Click-Thru Rate (CTR)", "Cost Per Click (CPC)", "Spend",
                            "14 Day Total Sales ", 'Total Advertising Cost of Sales (ACOS) ',
                            'Total Return on Advertising Spend (ROAS)',
                            "14 Day Total Orders (#)", "14 Day Total Units (#)", "14 Day Conversion Rate"]
            df = df[arrange_cols]
            df.to_csv(self.csv_file, index=False)

    def parse_SB_CM_D(self):
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))
            df = pd.DataFrame(jsondata)
            pd.set_option('display.max_columns', None)

            df = df.rename(
                columns={"campaignName": "Campaign Name", "impressions": "Impressions", "clicks": "Clicks",
                         "cost": "Spend", "attributedSales14d": "14 Day Total Sales ",
                         "attributedConversions14d": "14 Day Total Orders (#)", "unitsSold14d": "14 Day Total Units (#)"})

            df['Portfolio Id'] = None
            df['Currency'] = None
            df['Ad Group Name'] = None
            df['Advertised ASIN'] = None
            df['Date'] = self.report_date
            df['Click-Thru Rate (CTR)'] = df['Clicks'] / df['Impressions']
            df['Cost Per Click (CPC)'] = df['Spend'] / df['Clicks']
            df['Total Advertising Cost of Sales (ACOS) '] = df['Spend'] / df['14 Day Total Sales ']
            df['Total Advertising Cost of Sales (ACOS) '].replace([np.inf, -np.inf], np.nan, inplace=True)
            df['Total Return on Advertising Spend (ROAS)'] = df['14 Day Total Sales '] / df['Spend']
            df['Total Return on Advertising Spend (ROAS)'].replace([np.inf, -np.inf], np.nan, inplace=True)
            df['14 Day Conversion Rate'] = df['14 Day Total Orders (#)'] / df['Clicks']
            df['14 Day Conversion Rate'].replace([np.inf, -np.inf], np.nan, inplace=True)
            arrange_cols = ['Date', 'Portfolio Id', 'Currency', "Campaign Name", "Ad Group Name", "Advertised ASIN",
                            "Impressions", "Clicks", "Click-Thru Rate (CTR)", "Cost Per Click (CPC)", "Spend",
                            "14 Day Total Sales ", 'Total Advertising Cost of Sales (ACOS) ',
                            'Total Return on Advertising Spend (ROAS)',
                            "14 Day Total Orders (#)", "14 Day Total Units (#)", "14 Day Conversion Rate"]
            df = df[arrange_cols]
            df.to_csv(self.csv_file, index=False)
