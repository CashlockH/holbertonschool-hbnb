import uuid
from datetime import date
import os
from abc import ABC, abstractmethod
import json
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, abort
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
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.host = host
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities or []
        self.reviews = []
        self.id = uuid.uuid4()
        self.created_at = date.today()
        self.updated_at = date.today()
    
    def to_dict(self):
         return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'country': self.country.to_dict() if isinstance(self.country, Country) else self.country,
            'city': self.city.to_dict(),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host': self.host.to_dict(),
            'number_of_rooms': self.number_of_rooms,
            'bathrooms': self.bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews': [review.to_dict() for review in self.reviews],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def add_review(self, user, feedback, rating):
        review = Reviews(user, self, feedback, rating)
        self.reviews.append(review)
        return review

class User():
    emails = set()


    def __init__(self,  email, password, first_name, last_name):
        if email in User.emails:
            raise ValueError("Email already in use.")
        User.emails.add(email)
    
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
        self.created_at = date.today()
        self.updated_at = date.now()

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
    
    def create_place(self, name, description, address, country, city, latitude, longitude, number_of_rooms, bathrooms, price_per_night, max_guests, amenities=None):
        new_place = Places(name, description, address, country, city, latitude, longitude, self, number_of_rooms, bathrooms, price_per_night, max_guests, amenities)
        city.places.append(new_place)
        self.places.append(new_place)
        Places.places.append(new_place)
        return new_place

    def add_review(self, place, feedback, rating):
        review = Reviews(self, place, feedback, rating)
        place.reviews.append(review)
        self.reviews.append(review)
        return review

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'places': [place.to_dict() for place in self.places],
            'reviews': [review.to_dict() for review in self.reviews],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
class Reviews():
    def __init__(self, user, place_name, feedback, rating):
        self.id = uuid.uuid4()
        self.created_at = date.today()
        self.updated_at = date.today()
        self.user = user
        self.feedback = feedback
        self.rating = rating
        self.belongeness = place_name
    
    def to_dict(self):
         return {
            'id': str(self.id),
            'user': self.user.to_dict(),
            'place': self.place.to_dict(),
            'feedback': self.feedback,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Amenities():
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.created_at = date.today()
        self.updated_at = date.today()

    def to_dict(self):
       return {
            'id': str(self.id),
            'name': self.name,
            'type': 'amenity',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
class Country():
    countries = []
    def __init__(self, name):
        self.name = name
        self.cities = []
        Country.countries.append(self)
    
    def new_city(self, name):
        new = City(name, self)
        self.cities.append(new)
        return new
    
    def to_dict(self):
         return {
            'name': self.name,
            'cities': [city.to_dict() for city in self.cities],
            'type': 'country'
        }

class City():
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.places = []

    def to_dict(self):
       return {
            'name': self.name,
            'country': self.country.to_dict(),
            'places': [place.to_dict() for place in self.places],
            'type': 'city'
        }   

class DataManager(IPersistenceManager):
    def __init__(self, file_path='data.json'):
        self.file_path = file_path

    def save(self, entity):
        data = self._load_data()
        data.append(entity.to_dict())
        self._save_data(data)
        print("Entity saved")

    def get(self, entity_id, entity_type):
        data = self._load_data()
        for entity in data:
            if entity['id'] == entity_id and entity['type'] == entity_type:
                return entity
        return None

    def update(self, entity):
        data = self._load_data()
        for i, ent in enumerate(data):
            if ent['id'] == str(entity.id) and ent['type'] == entity.__class__.__name__:
                data[i] = entity.to_dict()
                self._save_data(data)
                print("Entity updated")
                return
        print("Entity not found")

    def delete(self, entity_id, entity_type):
        data = self._load_data()
        data = [ent for ent in data if not (ent['id'] == entity_id and ent['type'] == entity_type)]
        self._save_data(data)
        print("Entity deleted")

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

app = Flask(__name__)
api = Api(app, version='1.0', title='User API', description='A simple User API')
ns_user = api.namespace('users', description='User operations')
ns_country = api.namespace('countries', description='Country operations')
ns_city = api.namespace('cities', description='City operations')

data_manager = DataManager()

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email address'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.String(readonly=True, description='The user creation date'),
    'updated_at': fields.String(readonly=True, description='The user last update date')
})

country_model = api.model('Country', {
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code')
})

city_model = api.model('City', {
    'id': fields.String(attribute=lambda x: str(x.id)),
    'name': fields.String(required=True, description='City name'),
    'country_code': fields.String(required=True, description='ISO 3166-1 alpha-2 country code'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Date and time of creation'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Date and time of last update')
})  


@ns_country.route('/')
class CountryList(Resource):
    @ns_country.marshal_list_with(country_model)
    def get(self):
        """List all countries"""
        return [country.to_dict() for country in Country.countries]


@ns_country.route('/<string:country_code>')
class CountryResource(Resource):
    @ns_country.marshal_with(country_model)
    def get(self, country_code):
        """Get details of a specific country by code"""
        for country in Country.countries:
            if country.code == country_code:
                return country.to_dict()
        api.abort(404, f"Country {country_code} not found")


@ns_country.route('/<string:country_code>/cities')
class CountryCitiesResource(Resource):
    @ns_country.marshal_with(city_model)
    def get(self, country_code):
        """Get all cities belonging to a specific country"""
        cities = []
        for country in Country.countries:
            if country.code == country_code:
                cities.extend(country.cities)
                return [city.to_dict() for city in cities]
        api.abort(404, f"Country {country_code} not found")


@ns_city.route('/')
class CityList(Resource):
    @ns_city.marshal_list_with(city_model)
    def get(self):
        """List all cities"""
        cities = []
        for country in Country.countries:
            cities.extend(country.cities)
        return [city.to_dict() for city in cities]

    @ns_city.expect(city_model)
    @ns_city.marshal_with(city_model, code=201)
    def post(self):
        """Create a new city"""
        data = request.json
        country_code = data.get('country_code')
        city_name = data.get('name')

        if not country_code or not city_name:
            api.abort(400, "Country code and city name are required")

        # Check if the country code exists
        country = next((c for c in Country.countries if c.code == country_code), None)
        if not country:
            api.abort(404, f"Country {country_code} not found")

        # Check if the city name is unique within the country
        for city in country.cities:
            if city.name == city_name:
                api.abort(409, f"City {city_name} already exists in {country.name}")

        new_city = country.new_city(city_name)
        data_manager.save(new_city)
        return new_city.to_dict(), 201


@ns_city.route('/<string:city_id>')
class CityResource(Resource):
    @ns_city.marshal_with(city_model)
    def get(self, city_id):
        """Get details of a specific city by ID"""
        for country in Country.countries:
            for city in country.cities:
                if str(city.id) == city_id:
                    return city.to_dict()
        api.abort(404, f"City {city_id} not found")

    @ns_city.expect(city_model)
    @ns_city.marshal_with(city_model)
    def put(self, city_id):
        """Update an existing city"""
        data = request.json
        country_code = data.get('country_code')
        city_name = data.get('name')

        if not country_code or not city_name:
            api.abort(400, "Country code and city name are required")

        # Check if the country code exists
        country = next((c for c in Country.countries if c.code == country_code), None)
        if not country:
            api.abort(404, f"Country {country_code} not found")

        # Check if the city name is unique within the country
        for city in country.cities:
            if city.name == city_name and str(city.id) != city_id:
                api.abort(409, f"City {city_name} already exists in {country.name}")

        # Find and update the city
        for city in country.cities:
            if str(city.id) == city_id:
                city.name = city_name
                data_manager.update(city)
                return city.to_dict(), 200

        api.abort(404, f"City {city_id} not found")

    @ns_city.response(204, 'City deleted')
    def delete(self, city_id):
        """Delete a city"""
        for country in Country.countries:
            for city in country.cities:
                if str(city.id) == city_id:
                    country.cities.remove(city)
                    data_manager.delete(city_id, 'City')
                    return '', 204

        api.abort(404, f"City {city_id} not found")


if __name__ == '__main__':
    app.run(debug=True)
