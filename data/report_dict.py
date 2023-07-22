import openpyxl

file_path = "app reference/reports.xlsx"
sheet_name = "all_reports"

workbook = openpyxl.load_workbook(file_path)
sheet = workbook[sheet_name]

main_report_filename_dict = {}
for row in sheet.iter_rows(min_row=2, values_only=True):
    cell_value = row[0]
    if cell_value is not None:
        key = cell_value
        value = row[1] if row[1] is not None else ""
        main_report_filename_dict[key] = value
workbook.close()


report_dictionary = {"SP_AP_D":
                        {"report_name": "SP_AP_D",
                        "report_body": {
                            "name": '',
                            "startDate": '',
                            "endDate": '',
                            "configuration": {
                                "adProduct": "SPONSORED_PRODUCTS",
                                "groupBy": ["advertiser"],
                                "columns": ["date", "portfolioId", "campaignBudgetCurrencyCode", "campaignName", "adGroupName",
                                            "advertisedAsin",
                                            "impressions", "clicks", "clickThroughRate", "costPerClick", "spend", "sales14d",
                                            "purchases14d", "unitsSoldClicks14d"],
                                "reportTypeId": "spAdvertisedProduct",
                                "timeUnit": "DAILY",
                                "format": "GZIP_JSON"
                            }
                        },
                        "processor": [{'parser': 'parse_SP_AP_D',
                                      'updater': 'update_SP_AP_D',
                                      'name_suffix': main_report_filename_dict["SP_AP_D"],
                                      'secondary_table_name_suffix':''}]
                        },
                        "SB_CM_D":
                        {"report_name": "SB_CM_D",
                        "report_body": {
                            "reportDate": '',
                            "metrics": "campaignName,impressions,clicks,cost,attributedConversions14d,attributedSales14d,unitsSold14d",
                            "creativeType": "all"
                            },
                        "processor": [{'parser': 'parse_SB_CM_D',
                                      'updater': 'update_SB_CM_D',
                                      'name_suffix': main_report_filename_dict["SB_CM_D"],
                                      'secondary_table_name_suffix':''}]
                        }
                     }
