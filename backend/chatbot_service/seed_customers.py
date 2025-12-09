from database import Base, engine, SessionLocal
from models import Customer

def seed():
    Base.metadata.create_all(bind= engine)
    db = SessionLocal()
    if db.query(Customer).first():
        print("Customers already seeded.")
        return
    customers = [
        Customer(name="Aisha Khan", gender="female", location="Mumbai"),
        Customer(name="Rohan Sharma", gender="male", location="Delhi"),
        Customer(name="Neha Patel", gender="female", location="Mumbai"),
        Customer(name="Vikas Singh", gender="male", location="Bangalore"),
        Customer(name="Priya Verma", gender="female", location="Pune"),
    ]
    db.add_all(customers)
    db.commit()
    db.close()
    print("Seeded customers.")

if __name__ == "__main__":
    seed()