import xml.etree.ElementTree as ET
from functions.entities.model import Model

class Maker:

    def __init__(self, name):
        Maker.counter += 1
        self._id = Maker.counter
        self._name = name
        self._models = []
        
    def add_model(self, model: Model):
        self._models.append(model)

    def to_xml(self):
        el = ET.Element("Maker")  
        el.set("id", str(self._id))  
        el.set("name", self._name)
        
        for model in self._models:
            el.append(model.to_xml())

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"

Maker.counter = 0


class Type:

    def __init__(self, name):
        Type.counter += 1
        self._id = Type.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("Electric Type") 
        el.set("id", str(self._id)) 
        el.set("name", self._name)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"

Type.counter = 0
