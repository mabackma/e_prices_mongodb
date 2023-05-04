import pymongo


def make_all_queries():
    client = None

    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client.prices

        user_date = input("\nAnna päivämäärä YYYY-MM-DD: ")
        user_year = int(user_date[:4])
        user_month = int(user_date[5:7])
        user_day = int(user_date[8:10])

        # Haetaan tuntikohtaiset hinnat valitulta päivältä.
        query = {'year': user_year, 'month': user_month, 'day': user_day}
        todays_prices = db.prices.find(query)

        print(f"\nTuntikohtaiset hinnat päivälle {user_day}.{user_month}.{user_year}:")
        for price in todays_prices:
            print(f"{price['hour']}:00:   {round(price['value'], 3)} ¢")

        # Haetaan päiväkohtaiset keskiarvohinnat valitulta kuukaudelta.
        this_months_prices = db.prices.aggregate([
            {
                '$project': {
                    '_id': 0
                }
            }, {
                '$match': {
                    'year': user_year,
                    'month': user_month
                }
            }, {
                '$group': {
                    '_id': {
                        'day': '$day'
                    },
                    'value': {
                        '$avg': '$value'
                    }
                }
            }, {
                '$sort': {
                    '_id.day': 1
                }
            }
        ])

        print(f"\nPäiväkohtaiset keskiarvohinnat kuukaudelle {user_month}:")
        for item in this_months_prices:
            print(f"{item['_id']['day']}.{user_month}    {round(item['value'], 3)} ¢")

        # Haetaan kuukausikohtaiset keskiarvohinnat valitulle vuodelle.
        this_years_prices = db.prices.aggregate([
            {
                '$project': {
                    '_id': 0
                }
            }, {
                '$match': {
                    'year': user_year
                }
            }, {
                '$group': {
                    '_id': {
                        'month': '$month'
                    },
                    'value': {
                        '$avg': '$value'
                    }
                }
            }, {
                '$sort': {
                    '_id.month': 1
                }
            }
        ])

        print(f"\nKuukausikohtaiset keskiarvohinnat vuodelle {user_year}:")
        for item in this_years_prices:
            print(f"{user_year}-{item['_id']['month']}    {round(item['value'], 3)} ¢")

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()