import time
from classes.reportsV2 import newReport
import logging
import openpyxl
from datetime import datetime

logging.basicConfig(
    level=logging.WARNING,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    filename='app reference/app.log',  # Specify the log file name
    filemode='a'  # Set the file mode (w: write, a: append)
)

file_path = "app reference/reports.xlsx"
report_sheet_name = "V2_reports"

workbook = openpyxl.load_workbook(file_path)
report_sheet = workbook[report_sheet_name]

reports = []
for row in report_sheet.iter_rows(min_row=1, values_only=True):
    cell_value = row[0]
    if cell_value is not None:
        reports.append(cell_value)
workbook.close()

def run_auto(reports):
    report_objects = []
    excluded_report_objects = []
    for report in reports:
        base_report = newReport(f"{report}")
        date_range = base_report.get_date_range()
        del base_report

        for date in date_range:
            new_report = newReport(report, date)
            new_report.update_report_body()
            if new_report.request_report() == 202:
                report_objects.append(new_report)
            else:
                excluded_report_objects.append(new_report)
                error_message = f"Removed {report} from downloads, report Status: {new_report.request_report()}"
                logging.error(error_message)
                print(error_message)
            time.sleep(2)

    done_processing_report_objects = []
    no_of_reports = len(report_objects)

    print(report_objects)
    print(excluded_report_objects)

    while no_of_reports != len(done_processing_report_objects):
        if len(report_objects) >= 10:
            sleep_sec = 3
        elif len(report_objects) >= 5:
            sleep_sec = 7
        else:
            sleep_sec = 15
        for report in report_objects:
            report.get_report()
            if report.report_status == 'SUCCESS':
                done_processing_report_objects.append(report)
                report_objects.remove(report)
                report.download_report()
                print(report.report_date)
                report.parse_and_update_report()
            else:
                pass
            time.sleep(sleep_sec)

run_auto(reports)

# reports = ["SB_CM_D"]
# sbcmd = newReport("SB_CM_D")
# sbcmd.report_id = "amzn1.clicksAPI.v1.p1.64BADF26.b1ea9a9a-04d5-4722-91c2-a88e61be80ba"
# sbcmd.get_report()
# sbcmd.download_report()

# import requests
# import urllib.request
# from classes.reportsV2 import Report
#
# report = newReport("SB_CM_D")
#
# url = "https://advertising-api.amazon.com/v1/reports/amzn1.clicksAPI.v1.p1.64BADF26.b1ea9a9a-04d5-4722-91c2-a88e61be80ba/download"
# headers = report.header
#
#
# response = requests.get(url=url, headers=headers)
# print(response.status_code)
# print(response.text)
#
# if response.status_code == 200:
#     # Assuming you have a variable named `filename` with the desired output filename
#     filename = "C:/Users/emman/PycharmProjects/Amazon_Ads-API/raw_data/US_SB_CM_D_2023-06-28_2023-07-13.json.gz"
#     with open(filename, 'wb') as file:
#         file.write(response.content)
#     print(f"File downloaded and saved as '{filename}' successfully.")
# else:
#     print(f"Failed to download the file. Status Code: {response.status_code}")
