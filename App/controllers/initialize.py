from .user import create_user
from App.models import Apartment
from App.database import db
import csv


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    with open('apartment.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}

            try:
                apartment = Apartment(
                    title=row['title'],
                    body=row['body'],
                    amenities=row.get('amenities', None),
                    photo=row.get('photo', None),
                    pets_allowed=row.get('pets_allowed', None),
                    price=float(row['price']),
                    address=row.get('address', None),
                    cityname=row['cityname'],
                    landlord_id=int(row['landlord_id'])  # or however you map landlord
                )
                db.session.add(apartment)
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    db.session.commit()
    
