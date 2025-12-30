"""Check SQLAlchemy metadata for UserProfile"""
import sys
sys.path.insert(0, '.')

from database import Base
from models.user_profile import UserProfile
from sqlalchemy import inspect

print("=== Checking SQLAlchemy Metadata ===\n")

# Check the table in Base.metadata
if 'user_profiles' in Base.metadata.tables:
    table = Base.metadata.tables['user_profiles']
    print(f"Table found in Base.metadata: {table.name}")

    for col in table.columns:
        if col.name == 'total_questions':
            print(f"\nColumn in metadata:")
            print(f"  Name: {col.name}")
            print(f"  Type: {col.type}")
            print(f"  Type class: {type(col.type).__name__}")
            print(f"  Python type: {col.type.python_type if hasattr(col.type, 'python_type') else 'N/A'}")
            if col.default:
                print(f"  Default: {col.default}")
                print(f"  Default arg: {col.default.arg}")
else:
    print("user_profiles table NOT in Base.metadata!")

# Check the mapper
mapper = inspect(UserProfile)
print(f"\n=== Mapper for UserProfile ===")
for col in mapper.columns:
    if col.name == 'total_questions':
        print(f"\nColumn in mapper:")
        print(f"  Name: {col.name}")
        print(f"  Type: {col.type}")
        print(f"  Type class: {type(col.type).__name__}")
        if col.default:
            print(f"  Default: {col.default}")
            print(f"  Default arg: {col.default.arg}")

# Check all registered tables
print(f"\n=== All tables in Base.metadata ===")
for table_name in Base.metadata.tables.keys():
    print(f"  - {table_name}")
