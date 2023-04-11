import pymongo
import requests
from datetime import datetime

'''
def make_all_queries():
    client = None

    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client.prices

        #query = {'day': datetime.today().day, 'month': datetime.today().month, 'year': datetime.today().year}
        query = {'day': 3, 'month': 3, 'year': 2023}

        todays_prices = db.prices.find(query)

        # Haetaan tuntikohtaiset hinnat valitulta päivältä.
        print("\nTuntikohtaiset hinnat valitulta päivältä:")
        for price in todays_prices:
            print(f"{price['hour']}:00:   {round(price['value'], 3)} ¢")

        #query = { 'month': datetime.today().month, 'year': datetime.today().year}
        query = {'month': 3, 'year': 2023}

        this_months_prices = db.prices.find(query)

        index = 0
        sum = 0

        print("\nPäiväkohtaiset keskiarvohinnat valitulta kuukaudelta:")
        for price in this_months_prices:
            index += 1
            sum += price['value']
            if index % 24 == 0:
                print(f"{price['day']}.{price['month']}:   {round((sum / 24), 3)} ¢")
                sum = 0

        # query = {'year': datetime.today().year}
        query = {'year': 2023}

        this_years_prices = db.prices.find(query)

        index = 0
        sum = 0

        print("\nKuukausikohtaiset keskiarvohinnat valitulta vuodelta:")
        for price in this_months_prices:
            month = price['month']
            index += 1
            sum += price['value']
            if index % 24 == 0:
                print(f"{price['day']}.{price['month']}:   {round((sum / 24), 3)} ¢")
                sum = 0

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()
'''

def make_all_queries():
    client = None

    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client.prices

        user_date = input("\nAnna päivämäärä YYYY-MM-DD: ")
        user_year = int(user_date[:4])
        user_month = int(user_date[5:7])
        user_day = int(user_date[8:10])

        query = {'year': user_year, 'months.month': user_month, 'months.days.day': user_day}
        todays_prices = db.prices.find(query)

        # Haetaan tuntikohtaiset hinnat valitulta päivältä.
        print(f"\nTuntikohtaiset hinnat päivälle {user_day}.{user_month}.{user_year}:")
        for price in todays_prices:
            print(f"{price['months']['days']['hours']['hour']}:00:   {round(price['months']['days']['hours']['value'], 3)} ¢")

        query = {'year': user_year, 'months.month': user_month}
        this_months_prices = list(db.prices.find(query))

        sum = 0
        count = 0
        index = 0
        current_day = None

        print(f"\nPäiväkohtaiset keskiarvohinnat kuukaudelle {user_year}-{user_month}:")
        for item in this_months_prices:

            # Jos on kyseessä kuukauden viimeinen päivä niin lasketaan viimeisen päivän keskiarvo.
            if index == len(this_months_prices) - 1:
                sum += item['months']['days']['hours']['value']
                count += 1
                avg_price = round((sum / count), 3)
                print(f"{item['months']['days']['day']}.{item['months']['month']}:    {avg_price} ¢")

            # Lasketaan aina edellisen päivän keskiarvo kun päivä vaihtuu.
            if item['months']['days']['day'] != current_day:
                if current_day is not None:
                    avg_price = round((sum / count), 3)
                    print(f"{item['months']['days']['day'] - 1}.{item['months']['month']}:    {avg_price} ¢")
                current_day = item['months']['days']['day']
                sum = 0
                count = 0
            sum += item['months']['days']['hours']['value']
            count+=1
            index += 1

        query = {'year': user_year}
        this_years_prices = list(db.prices.find(query))

        sum = 0
        count = 0
        index = 0
        current_month = None

        print(f"\nKuukausikohtaiset keskiarvohinnat vuodelle {user_year}:")
        for item in this_years_prices:

            # Jos on kyseessä vuoden viimeinen päivä niin lasketaan viimeisen kuukauden keskiarvo.
            if index == len(this_years_prices) - 1:
                sum += item['months']['days']['hours']['value']
                count += 1
                avg_price = round((sum / count), 3)
                print(f"{item['year']}-{item['months']['month']}:    {avg_price} ¢")

            # Lasketaan aina edellisen kuukauden keskiarvo kun kuukausi vaihtuu.
            if item['months']['month'] != current_month:
                if current_month is not None:
                    avg_price = round((sum / count), 3)
                    print(f"{item['year']}-{item['months']['month'] - 1}:    {avg_price} ¢")
                current_month = item['months']['month']
                sum = 0
                count = 0
            sum += item['months']['days']['hours']['value']
            count+=1
            index += 1


    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()