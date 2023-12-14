import xml.etree.ElementTree as ET

class Car:
    
    def __init__(self, dol, vin, modyear, erange, cafv, utility, city):
        Car.counter += 1
        self._id = Car.counter
        self._dol = dol
        self._vin = vin
        self._modyear = modyear
        self._erange = erange
        self._cafv = cafv
        self._utility = utility
        self._city = city

    def to_xml(self):
        el = ET.Element("Car")  
        el.set("id", str(self._id))  
        el.set("DOL", self._dol)
        el.set("VIN", self._vin)
        el.set("year", self._modyear)
        el.set("range", self._erange)
        el.set("cafv_ref", str(self._cafv.get_id())) 
        el.set("utility_ref", str(self._utility.get_id()))
        el.set("city_ref", str(self._city.get_id())) 
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"id:{self._id}, dol:{self._dol}, model year:{self._modyear}, electric range:{self._erange}, VIN: {self._vin}, cafv_ref:{self._cafv}, utility_ref:{self._utility}, city_ref:{self._county}"

Car.counter = 0