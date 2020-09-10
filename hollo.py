import ephem
import datetime


date = datetime.date.today()

a = ephem.Mars(date)
print(ephem.constellation(a))


#print(real_planet(planeta, date))
