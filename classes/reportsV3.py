import openpyxl
import requests
from datetime import datetime
import json
import urllib.request
import logging


from data.report_dict import report_dictionary
from data.default_dates import date_dictionary
from classes.authenticator import Authenticator


logging.basicConfig(
    level=logging.WARNING,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    filename='app reference/app.log',  # Specify the log file name
    filemode='a'  # Set the file mode (w: write, a: append)
)

# TODO 1: Set variables saved from credentials.csv
file_path = "./app reference/reference.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
pathGz = reference["paths"]["B2"].value
pathJson = reference["paths"]["B3"].value
mainFilePath = reference["paths"]["B4"].value
reference.close()
amzDate = datetime.now().strftime("%Y%m%dT%H%M%SZ")

today = datetime.now()

class Report:
    def __init__(self):
        self.authenticator = Authenticator()
        self.path_json_base = pathJson
        self.path_gzip_base = pathGz
        self.report_id = ""
        self.doc_id = ""
        self.report_status = ""
        self.report_url = ""
        self.comp_algo = ""
        self.header = {"Content-Type": "application/vnd.createasyncreportrequest.v3+json",
                        "Amazon-Advertising-API-ClientID": self.authenticator.clientId,
                        "Amazon-Advertising-API-Scope": self.authenticator.profileId,
                        "Authorization": f"Bearer {self.authenticator.accessToken}"}


class newReport(Report):
    def __init__(self, report_key):
        super().__init__()
        self.report_type_options = report_dictionary[report_key]
        self.report_key = report_key
        self.report_name = self.report_type_options["report_name"]
        self.report_body = self.report_type_options["report_body"]
        self.processors = self.report_type_options["processor"]
        self.json = ""
        self.update_report_body()
        self.requested_report_end_date = ""
        self.requested_report_start_date = ""
        self.filename_string = ""
        self.gz_file = ""

    def update_report_body(self, custom_start=None, custom_end=None):
        """Updates request report body by referring into default_dates.py
        accepts custom_start and custom_end dates following this format YYYY-MM-DD"""

        if (custom_start and custom_end) is None:
            self.default_start = date_dictionary[self.report_key]["defaultStart"]
            self.default_end = date_dictionary[self.report_key]["defaultEnd"]
            self.report_body.update({'name': self.report_name, 'startDate': self.default_start, 'endDate': self.default_end})
        else:
            self.report_body.update({'name': self.report_name, 'startDate': custom_start, 'endDate': custom_end})


    def request_report(self):
        """requests for a report, retrieves report_id"""
        try:
            # params = {"marketplaceIds": [self.mp_id]}
            response = requests.post(url="https://advertising-api.amazon.com/reporting/reports",
                                     data=json.dumps(self.report_body), headers=self.header)
            # print(f"request_report method status code {response.status_code}")
            # print(f"request_report method text {response.text}")
            if response.status_code == 200:
                response_data = response.json()
                self.report_id = response_data['reportId']
                print(response_data)
                return response.status_code
            else:
                error_message = f"Report request failed with status code: {response.status_code}"
                logging.error(error_message)
                print(response.text)
                print(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred during the report request: {str(e)}"
            logging.exception(error_message)
            print(error_message)

        except (ValueError, KeyError) as e:
            error_message = f"Invalid response data: {str(e)}"
            logging.exception(error_message)
            print(error_message)

        except Exception as e:
            error_message = f"An unknown error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)


    def get_report(self):
        """Gets the report document ID to be used in downloading the report"""
        try:
            response = requests.get(url=f"https://advertising-api.amazon.com/reporting/reports/{self.report_id}",
                                    headers=self.header)
            # print(f"get_report method status code {response.status_code}")
            # print(f"get_report method text {response.text}")
            if response.status_code == 200:
                response_data = response.json()
                self.report_status = response_data["status"]

                if self.report_status == 'COMPLETED':
                    self.report_url = response_data["url"]
                    self.requested_report_end_date = response_data["endDate"]
                    self.requested_report_start_date = response_data["startDate"]
                    # self.failure_reason = response_data["failureReason"]
                    print(response_data)
                    return response.status_code
                else:
                    print(response_data)
                    return self.report_status
            else:
                error_message = f"Request failed with status code: {response.status_code}"
                logging.error(error_message)
                print(error_message)


        except (ValueError, KeyError) as e:
            error_message = f"Invalid response data: {str(e)}"
            logging.exception(error_message)
            print(error_message)


        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred during the request: {str(e)}"
            logging.exception(error_message)
            print(error_message)


        except Exception as e:
            error_message = f"An unknown error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)


    def download_report(self):
        try:
            self.filename_string = f"{self.report_name}_{self.requested_report_start_date}_{self.requested_report_end_date}"
            self.gz_file = self.path_gzip_base + self.filename_string + ".json.gz"
            # Download the compressed JSON file
            urllib.request.urlretrieve(self.report_url, self.gz_file)

        except FileNotFoundError as e:
            error_message = f"File not found: {str(e)}"
            logging.exception(error_message)
            print(error_message)

        except IOError as e:
            error_message = f"IO error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)

        except Exception as e:
            error_message = f"An error occurred while requesting a report: {str(e)}"
            logging.exception(error_message)
            print(error_message)

    def parse_and_update_report(self):
        from classes.report_parser import Parser
        from classes.report_updater import Updater
        for processor in self.processors: #list
            self.parser = processor['parser']
            self.updater = processor['updater']
            self.main_file = f"{mainFilePath}\{processor['name_suffix']}.csv"
            self.secondary_file = f"{mainFilePath}\{processor['secondary_table_name_suffix']}.csv"
            report_parser_obj = Parser(self)
            parser_method = getattr(report_parser_obj, self.parser)
            parser_method()
            report_parser_obj = Updater(self)
            update_method = getattr(report_parser_obj, self.updater)
            update_method()
