import datetime
class Menu():
  def __init__(self, name, item, start_time, end_time):
    self.name = name
    self.items = item
    self.start_time = start_time
    self.end_time = end_time

  def calculate_bill(self, purchased_itmes):
    total = 0
    for item in purchased_itmes:
      total += self.items.get(item)
    print(total)


  def __repr__(self):
    return f"{self.name} menu available form {self.start_time} to {self.end_time}"

brunch = Menu("brunch",{
  'pancakes': 7.50, 'waffles': 9.00, 'burger': 11.00, 'home fries': 4.50, 'coffee': 1.50, 'espresso': 3.00, 'tea': 1.00, 'mimosa': 10.50, 'orange juice': 3.50
},datetime.time(hour = 11,minute = 00),datetime.time(hour = 16,minute = 00))

early_bird = Menu("early_bird",{
  'salumeria plate': 8.00, 'salad and breadsticks (serves 2, no refills)': 14.00, 'pizza with quattro formaggi': 9.00, 'duck ragu': 17.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 1.50, 'espresso': 3.00,
},datetime.time(hour = 15,minute = 00),datetime.time(hour = 18,minute = 00))

dinner = Menu("dinner",{
  'crostini with eggplant caponata': 13.00, 'ceaser salad': 16.00, 'pizza with quattro formaggi': 11.00, 'duck ragu': 19.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 2.00, 'espresso': 3.00,
},datetime.time(hour = 17,minute = 00),datetime.time(hour = 23,minute = 00))

kids = Menu("kids", {
  'chicken nuggets': 6.50, 'fusilli with wild mushrooms': 12.00, 'apple juice': 3.00
},datetime.time(hour = 11,minute = 00),datetime.time(hour = 23,minute = 59))

arepas_menu = Menu("Take a’ Arepa", {
  'arepa pabellon': 7.00, 'pernil arepa': 8.50, 'guayanes arepa': 8.00, 'jamon arepa': 7.50
  },datetime.time(hour = 10,minute = 00),datetime.time(hour = 20,minute = 00))

#brunch.calculate_bill(['pancakes', 'home fries', 'coffee'])
#early_bird.calculate_bill(["salumeria plate","mushroom ravioli (vegan)"])

class Franchise():
  def __init__(self, address, menus):
    self.address = address
    self.menus = menus

  def available_menus(self, time):
    for item in self.menus:
      if datetime.time(hour = time) >= item.start_time and datetime.time(hour = time) <= item.end_time:
        print(item)

  def __repr__(self):
    return self.address

flagship_store = Franchise("1232 West End Road", [brunch, early_bird, dinner, kids]) 

new_installment = Franchise("12 East Mulberry Street", [brunch, early_bird, dinner, kids])

arepas_place = Franchise("189 Fitzgerald Avenue", [ arepas_menu])


class Buisness():
  def __init__(self, name, franchises):
    self.name = name
    self.franchises = franchises

arepas = Buisness("Take a' Arepa",[arepas_place])

print(arepas.franchises[0].menus[0])
