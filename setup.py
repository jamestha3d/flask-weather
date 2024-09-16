"""

Data Source:
- City data is retrieved from [latlong.net](https://www.latlong.net/place/calgary-ab-canada-29104.html#:~:text=Calgary%2C%20AB%2C%20Canada%20Lat%20Long,%C2%B0%203'%2059.9976''%20W.)

"""

import csv
from api.models import City
from sqlalchemy.exc import IntegrityError


def load_cities():
    with open("cities.csv", 'r') as file:
        reader = csv.reader(file)

        next(reader)
        try:
            for name, country, latitude, longitude in reader:
                City.create(name=name, latitude=latitude, longitude=longitude)
                print(".", end='')

        except IntegrityError:
            return
    

if __name__ == "__main__":
	load_cities()
     