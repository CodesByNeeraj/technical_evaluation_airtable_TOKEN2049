
from pyairtable import Api
from config import settings

API_KEY = settings.AIRTABLE_API_KEY
BASE_ID = settings.AIRTABLE_BASE_ID
TABLE_NAME = settings.AIRTABLE_TABLE_NAME

def test_read_airtable():
    try:
        api = Api(API_KEY)
        table = api.table(BASE_ID, TABLE_NAME)
        records = table.all()
        print(f"Fetched {len(records)} records from Airtable:")
        for rec in records:
            print(rec['fields'])
    except Exception as e:
        print(f"Error reading from Airtable: {e}")

if __name__ == "__main__":
    test_read_airtable()
