import uuid
from datetime import date
from abc import ABC, abstractmethod
import json
class IPersistenceManager(ABC):
    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        pass


class Places():
    places = []
    def __init__(self, name, description, address, country, city, latitude, longitude, host, number_of_rooms, bathrooms, price_per_night, max_guests, amenities = None):
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.host = host
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = []
        if amenities is not None:
            self.amenities = amenities
        self.reviews = []
        self.id = uuid.uuid4()
        self.created_at = date.today()
    
    def add_review(self, user, feedback, rating):
        review = Reviews(user, self, feedback, rating)
        self.reviews.append(review)
        return review

    

class User():
    def __init__(self,  email, password, first_name, last_name):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.created_at = date.today()

    def create_place(self, name, description, address, country, city, latitude, longitude, number_of_rooms, bathrooms, price_per_night, max_guests, amenities = None):
        found = 0

        for country_instance in Country.countries:
            if country_instance.name == country:
                for city_instance in country_instance.cities:
                    if city == city_instance.name:
                        city = city_instance
                        found = 1

        for index, amenity in enumerate(amenities):
            amen_checker = 0
            for amen_name in catalog:
                if amen_name.name == amenity:
                    amenities[index] = amen_name
                    amen_checker = 1
            if amen_checker == 0:   
                new_amen = self.add_new_amenity(amenity)
                amenities[index] = new_amen

        
        if found == 1:
            new_place = Places(name, description, address, country, city, latitude, longitude, self, number_of_rooms, bathrooms, price_per_night, max_guests, amenities)
            city.places.append(new_place)
            self.places.append(new_place)
            Places.places.append(new_place)
            return new_place
    
    def add_new_amenity(self, name):
        new = Amenities(name)
        return new
    
    
class Reviews():
    def __init__(self, username, place_name, feedback, rating):
        self.id = uuid.uuid4()
        self.created_at = date.today()
        self.feedback = feedback
        self.rating = rating
        self.belongeness = place_name
    

class Amenities():
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.created_at = date.today()
    
class Country():
    countries = []
    def __init__(self, name):
        self.name = name
        self.cities = []
        Country.countries.append(self)
    
    def new_city(self, name):
        new = City(name)
        self.cities.append(new)

class City():
    def __init__(self, name):
        self.name = name
        self.places = []

class DataManager(IPersistenceManager):
    def save(self, entity):
        with open('file.json', 'a') as filename:
            json.dump(entity, filename)
        print("File saved")
        return 0

    def get(self, entity_id, entity_type):
        pass

    def update(self, entity):
        pass

    def delete(self, entity_id, entity_type):
        pass
