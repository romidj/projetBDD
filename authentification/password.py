from django.contrib.auth.hashers import make_password
from django.conf import settings

settings.configure()

# Replace 'your_password_here' with the actual password
raw_password = '2720042021mey'

# Hash the password
hashed_password = make_password(raw_password)

# Print the hashed password
print(hashed_password)