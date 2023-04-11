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

        query = {'year': user_year, 'month': user_month, 'day': user_day}
        todays_prices = db.prices.find(query)

        # Haetaan tuntikohtaiset hinnat valitulta päivältä.
        print(f"\nTuntikohtaiset hinnat päivälle {user_day}.{user_month}.{user_year}:")
        for price in todays_prices:
            print(f"{price['hour']}:00:   {round(price['value'], 3)} ¢")

        query = {'year': user_year, 'month': user_month}
        this_months_prices = list(db.prices.find(query))

        sum = 0
        count = 0
        index = 0
        current_day = None

        print(f"\nPäiväkohtaiset keskiarvohinnat kuukaudelle {user_year}-{user_month}:")
        for item in this_months_prices:

            # Jos on kyseessä kuukauden viimeinen päivä niin lasketaan viimeisen päivän keskiarvo.
            if index == len(this_months_prices) - 1:
                sum += item['value']
                count += 1
                avg_price = round((sum / count), 3)
                print(f"{item['day']}.{item['month']}:    {avg_price} ¢")

            # Lasketaan aina edellisen päivän keskiarvo kun päivä vaihtuu.
            if item['day'] != current_day:
                if current_day is not None:
                    avg_price = round((sum / count), 3)
                    print(f"{item['day'] - 1}.{item['month']}:    {avg_price} ¢")
                current_day = item['day']
                sum = 0
                count = 0
            sum += item['value']
            count += 1
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
                sum += item['value']
                count += 1
                avg_price = round((sum / count), 3)
                print(f"{item['year']}-{item['month']}:    {avg_price} ¢")

            # Lasketaan aina edellisen kuukauden keskiarvo kun kuukausi vaihtuu.
            if item['month'] != current_month:
                if current_month is not None:
                    avg_price = round((sum / count), 3)
                    print(f"{item['year']}-{item['month'] - 1}:    {avg_price} ¢")
                current_month = item['month']
                sum = 0
                count = 0
            sum += item['value']
            count += 1
            index += 1


    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()