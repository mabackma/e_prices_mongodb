import pymongo
import requests
from datetime import datetime


def import_values():
    client = None

    try:
        client = pymongo.MongoClient(host='mongodb://localhost:27017/prices')
        db = client.prices

        res = requests.get('http://spotprices.energyecs.frostbit.fi/api/v1/prices')
        prices_list = res.json()

        for p in prices_list:
            time_str = p['_time']
            time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
            day = time_obj.day
            month = time_obj.month
            year = time_obj.year
            hour = time_obj.time().hour
            price = {'day': day, 'month': month, 'year': year, 'hour': hour, 'value': p['value']}
            db.prices.insert_one(price)

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()