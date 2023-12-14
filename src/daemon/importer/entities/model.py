import xml.etree.ElementTree as ET
from functions.entities.car import Car

class Model:

    def __init__(self, name, etype):
        Model.counter += 1
        self._id = Model.counter
        self._name = name
        self._etype = etype
        self._cars = []
        
    def add_car(self, car: Car):
        self._cars.append(car)

    def to_xml(self):
        el = ET.Element("Model")  
        el.set("id", str(self._id))  
        el.set("name", self._name)
        el.set("type", str(self._etype))
        
        for car in self._cars:
            el.append(car.to_xml())
        
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}, electrict type:{self._etype}"

Model.counter = 0
