from myhttp import MyHttp
from create_db import MyDB
import time
import mysql.connector


sleep_time = 5


"""
    Returns list of the data of the requested month(ex 1) year(ex 2020)
"""
def get_daily_generation_data(month, year, user_id):
    url = "/graph/Graph/cumulative_month_graph"
    payload = {"month":month,"year":year,"user_id":user_id}
    response = http.send_request(url, payload)
    return response.get('resultObject')


"""
    Returns error data between start_date(ex-"2020-01-01") end_date (ex - "2020-02-29")
"""
def get_error_data(start_date, end_date, limit, offset):
    url = "/normal/Alarms/getClearedNormalAlarms"
    error_data = []
    count = offset + limit + 1
    while count > offset:
        payload = {"user_id":"90","start_date":start_date,"end_date":end_date,"limit":limit,"offset":offset}
        response = http.send_request(url, payload)
        time.sleep(sleep_time)
        if not response.get('resultObject'):
            break
        error_data.extend(response.get('resultObject'))
        offset += limit
        count = response['count']

    return error_data


BASE_URL = "http://3.6.0.2/inject-solar-angular/inject_solar_server"
login_id = "triose"
password = "triose123"

http = MyHttp(BASE_URL, login_id, password)

# getting daily generation data of january
print("Getting jan generation data")
month_jan = 1
year = 2020
jan_daily_generation_data = get_daily_generation_data(month_jan, year, login_id)
time.sleep(sleep_time)

# getting daily generation data of february
print("Getting feb generation data")
month_feb = 2
feb_daily_generation_data = get_daily_generation_data(month_feb, year, login_id)
time.sleep(sleep_time)

# getting error data of january and february
start_date = "2020-01-01"
end_date = "2020-02-29"
limit = 50
offset = 0
print("Getting jan feb error data")
error_data = get_error_data(start_date, end_date, limit, offset)

# Preparing database
print("Preparing database")
myDB = MyDB()
mydb = myDB.get_instance()
cursor = mydb.cursor()

# Saving data in database
print("Saving data")
daily_generation_data = jan_daily_generation_data + feb_daily_generation_data
cursor.executemany("""
    INSERT INTO dailygeneration (date, power_generation)
    VALUES (%(date)s, %(power_generation)s)""", daily_generation_data)
cursor.executemany("""
    INSERT INTO dailyerror (dev_name, name, inv_name, alarm_id, date_time, clear_time, alarm_msg)
    VALUES (%(dev_name)s, %(name)s, %(inv_name)s, %(alarm_id)s, %(date_time)s, %(clear_time)s, %(alarm_msg)s)""", error_data)
mydb.commit()

print("Data scraping task finished !")
