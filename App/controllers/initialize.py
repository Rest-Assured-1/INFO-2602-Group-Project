from .user import create_user, create_landlord, create_tenant
from App.models import Apartment, Landlord, Tenant
from App.database import db
from App.controllers.review import create_review
import csv


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_landlord('larry', 'larrypass')
    create_landlord('liam', 'liampass')

    create_landlord('landlord1', 'landlord1pass')
    create_landlord('landlord2', 'landlord2pass')
    create_landlord('landlord3', 'landlord3pass')
    create_landlord('landlord4', 'landlord4pass')
    create_landlord('landlord5', 'landlord5pass')
    create_landlord('landlord6', 'landlord6pass')
    create_landlord('landlord7', 'landlord7pass')
    create_landlord('landlord8', 'landlord8pass')

    create_tenant('tony', 'tonypass')
    create_tenant('tina', 'tinapass')

    with open('apartment.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}

            try:
                if(row['address']=='null'):
                    add='call for info'
                else:
                    add=row['address']
                
                if(row['amenities']=='null'):
                    am='call for info'
                else:
                    am=row['amenities']

                if(row['pets_allowed']=='null' or row['pets_allowed']=='None'):
                    pets='No'
                else:
                    pets=row['pets_allowed']

                for landlord in db.session.query(Landlord).all():
                    if landlord.id == int(row['landlord_id']):
                        apartment = landlord.create_apartment(
                            title=row['title'],
                            body=row['body'],
                            price=float(row['price']),
                            address=add,
                            photo=row.get('photo', None),
                            city=row['cityname'],
                            amenities=am,
                            pets_allowed=pets,
                        )
                        db.session.add(apartment)
                        for tenant in db.session.query(Tenant).all():
                            if tenant.username == 'tony':
                                review = create_review(apartment.id, 5, 'Great place!', tenant.id)
                            if tenant.username == 'tina':
                                review = create_review(apartment.id, 2, 'Not up to my standards.', tenant.id)
                            db.session.add(review)
                        break
                
                
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    db.session.commit()
    
