from datetime import datetime, timedelta

today = datetime.now()

date_dictionary = {"SP_AP_D":
                        {"defaultStart": (today - timedelta(days=18)).strftime("%Y-%m-%d"),#18
                        "defaultEnd": (today - timedelta(days=18)).strftime("%Y-%m-%d")},#3
                    "SB_CM_D":
                        {"defaultStart": (today - timedelta(days=18)).strftime("%Y%m%d"),#18
                        "defaultEnd": (today - timedelta(days=18)).strftime("%Y%m%d")}#3
                   }

