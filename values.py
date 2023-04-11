import pymongo
import requests
from datetime import datetime
from pymongo import ASCENDING


def import_values():
    client = None

    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client.prices

        res = requests.get('http://spotprices.energyecs.frostbit.fi/api/v1/prices')
        prices_list = res.json()

        # Indeksoidaan kokoelma.
        prices_collection = db.prices
        prices_collection.create_index(
            [("year", ASCENDING), ("month", ASCENDING), ("day", ASCENDING),
             ("hour", ASCENDING)], unique=True)

        for p in prices_list:
            time_str = p['_time']
            time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
            day = time_obj.day
            month = time_obj.month
            year = time_obj.year
            hour = time_obj.time().hour
            price = {'year': year, 'month': month, 'day': day, 'hour': hour, 'value': p['value']}

            # Lisätään arvot tietokantaan jos päivää ei löydy jo kokoelmasta.
            db.prices.insert_one(price, {'upsert': True})

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()