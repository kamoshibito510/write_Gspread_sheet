import gspread
import json
import os
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

def get_gspread():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    SECRETS = json.loads(os.environ["GCP_SECRET_JSON"])
    credentials = Credentials.from_service_account_info(
        SECRETS,
        scopes=scopes
    )

    SP_SHEET_KEY = os.environ["SP_SHEET_KEY"]
    SP_SHEET = os.environ["SP_SHEET_TAB_NAME"]

    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SP_SHEET_KEY)
    ws = sh.worksheet(SP_SHEET)
    return ws

def gcp_writer():
    date_today = datetime.today().timetuple()
    date = f'{date_today.tm_year}-{date_today.tm_mon}-{date_today.tm_mday}'
    data_dict = {'Date': f'{date}', 'column1': 'ダンゴ', 'column2': 'ゴディバ', 'column3': 'バルス', 'column4': 'スバル'}

    ws = get_gspread()
    df = pd.DataFrame(ws.get_all_values()[1:], columns=ws.get_all_values()[0])
    df = df.append(data_dict, ignore_index=True)
    set_with_dataframe(ws, df, row=1, col=1)

def main():
    gcp_writer()

if __name__ == "__main__":
    main()