"""Verify UserProfile model column types at runtime"""
import sys
sys.path.insert(0, '.')

from models.user_profile import UserProfile
from sqlalchemy import inspect

# Get column info
mapper = inspect(UserProfile)
for col in mapper.columns:
    if col.name == 'total_questions':
        print(f"Column: {col.name}")
        print(f"Type: {col.type}")
        print(f"Python type: {type(col.type)}")
        print(f"Default: {col.default}")
        if col.default:
            print(f"Default arg: {col.default.arg}")
            print(f"Default arg type: {type(col.default.arg)}")
