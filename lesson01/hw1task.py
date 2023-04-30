from abc import abstractmethod, ABCMeta
import json, pickle

class SerializationInterface(metaclass = ABCMeta):

    @abstractmethod
    def serialize(self, way):
        pass

    @abstractmethod
    def deserialize(self, data, way):
        pass

class JSONContainer(SerializationInterface):
    data = {}

    def serialize(self, way):
        with open(way, 'w') as file:
            json.dump(self.data, file)
        print('Data(json) was serialized!')

    def deserialize(self, way):
        with open(way, 'r') as file:
            self.data = json.load(file)
        print('Data(json) was loaded!')
                        

class PickleContainer(SerializationInterface):
    data = None

    def serialize(self, way):
        with open(way, 'wb') as file:
            pickle.dump(self.data, file)
        print('Data(pickle) was serialized!')

    def deserialize(self, way):
        with open(way, 'rb') as file:
            self.data = pickle.load(file)
        print('Data(pickle) was loaded!')
