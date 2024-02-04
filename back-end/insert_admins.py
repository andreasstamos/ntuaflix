from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Sequence, exc
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from datetime import date
from db_type import *
from models import User  
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

usernames = ['admin_Pik', 'admin_andreas', 'admin_BigNick', 'stefadmin', 'friday_admin', 'mlazoy_as_admin']
passwords = ['admin1', 'admin2', 'admin3', 'admin4', 'admin5', 'admin6']

for i, (username, password) in enumerate(zip(usernames, passwords), 1):
    admin_data = {
        'id': i,
        'username': username,
        'first_name': f'Admin{i}',
        'last_name': f'Last{i}',
        'email': f'{username}@example.com',
        'password': pwd_context.hash(password),
        'dob': date(1990 + i, 1, 1),
        'is_admin': True
    }
    admin_instance = User(**admin_data)

    db = next(get_db())
    try:
        db.add(admin_instance)
        db.commit()
        print(f"Admin {username} inserted successfully")
        db.refresh
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Unable to insert admin {username}!')




