from werkzeug.security import generate_password_hash, check_password_hash

# Function to hash the password
def hash_password(password):
    return generate_password_hash(password)

# Function to verify the hashed password
def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)
