from werkzeug.security import generate_password_hash, check_password_hash
import re

## This module contain All additional core Resuable Methods as Utility Tools
## Security: Hashing Passwords
## Client Side Validation 
## Code reusbility 
 
def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(stored_hash: str, input_password: str) -> bool:
    return check_password_hash(stored_hash, input_password)



def is_valid_email(email: str) -> bool:
    """Check if email is in correct format."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_password(password: str) -> bool:
    """
    Password must be at least 6 characters long,
    contain at least one letter and one number.
    """
    if len(password) < 6:
        return False
    return bool(re.search(r"[A-Za-z]", password)) and bool(re.search(r"\d", password))
