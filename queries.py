import pymongo
import requests
from datetime import datetime


def make_all_queries():
    client = None

    try:
        client = pymongo.MongoClient(host='mongodb://localhost:27017/prices')
        db = client.prices

        #query = {'day': datetime.today().day, 'month': datetime.today().month, 'year': datetime.today().year}
        query = {'day': 3, 'month': 4, 'year': 2023}

        todays_prices = db.prices.find(query)

        # Haetaan tuntikohtaiset hinnat valitulta päivältä.
        for price in todays_prices:
            print(f"{price['hour']}:00:   {round(price['value'], 3)} ¢")

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()