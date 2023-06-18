from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import uvicorn

app = FastAPI()

# Set up the database connection
engine = create_engine("sqlite:///mydatabase.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a database model
class User(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True, index=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))

# Create the database tables
Base.metadata.create_all(bind=engine)

# API endpoint to create a new user
@app.post("/users/create/")
def create_user(username: str, email: str, password: str):
    # Create a new session
    db = SessionLocal()
    
    # Check if the user already exists
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {"status": "failed", "message": "User already exists"}
    
    # Create a new user instance
    new_user = User(username=username, email=email, password=password)
    
    # Add the user to the session
    db.add(new_user)
    
    # Commit the changes to the database
    db.commit()
    
    # Close the session
    db.close()
    
    return {"status": "success", "message": "User created successfully"}

# API endpoint to check if a user exists and the password is correct
@app.get("/users/login/")
def check_user(username: str, password: str):
    # Create a new session
    db = SessionLocal()
    
    # Check if the user exists
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"status": "failed", "message": "user not found"}
    
    # Check if the password is correct
    if user.password != password:
        return {"status": "failed", "message": "Wrong password"}
    
    # Close the session
    db.close()
    
    return {"status": "success", "message": "Login successful"}

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
