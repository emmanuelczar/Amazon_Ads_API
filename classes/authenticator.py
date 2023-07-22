import openpyxl
import requests
from datetime import datetime, timedelta

# TODO 1: Set static variables
file_path = "./app reference/reference.xlsx"
authURL = "https://api.amazon.com/auth/o2/token"

# TODO 1: Set variables saved from credentials.csv

amzDate = datetime.now().strftime("%Y%m%dT%H%M%SZ")




class Authenticator:
    def __init__(self):
        # self.mp = mp
        # self.credential_map = credentials_mapping[self.mp]
        self.authURL = authURL
        self.check_reference()

    def check_reference(self):
        """Checks if we need to request a new token"""
        self.reference = openpyxl.load_workbook(file_path)
        self.profileId = self.reference["app_credentials"]["B2"].value.strip('"')
        self.clientId = self.reference["app_credentials"]["B3"].value.strip('"')
        self.clientSecret = self.reference["app_credentials"]["B4"].value.strip('"')
        self.accessTokenSheet = self.reference["token_credentials"]
        self.accessToken = self.accessTokenSheet["B2"].value.strip('"')
        self.refreshToken = self.accessTokenSheet["B3"].value.strip('"')
        self.params = {"grant_type": "refresh_token",
                        "refresh_token": self.refreshToken,
                        "client_id": self.clientId,
                        "client_secret": self.clientSecret
                       }
        self.accessTokenCreated = self.accessTokenSheet["C2"].value
        self.accessTokenExpires = self.accessTokenCreated + timedelta(minutes=60)
        if self.accessTokenExpires < datetime.today():
            self.request_access_token_r()
        else:
            pass
        self.reference.close()


    def update_access_token(self, new_token):
        """Writes new access token in the excel file where we saved our variables"""
        self.accessTokenSheet["B2"] = new_token
        self.accessTokenSheet["C2"] = datetime.today()
        self.reference.save(file_path)
        self.accessToken = new_token


    def request_access_token_r(self):
        """ This function requests for an access token using a refresh token
        Args:
        Returns: access_token (expires in 60 minutes)
        Raises:  status_code
        Example: request_access_token_r(refreshtoken)
        """
        response = requests.post(url=self.authURL, params=self.params)
        if response.status_code == 200:
            response_json = response.json()
            access_token_new = response_json["access_token"]
            self.update_access_token(access_token_new)
            return self.accessToken
        else:
            return f"request_access_token_r(): {response.status_code}"


