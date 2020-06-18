# Set the following two lines.
# If u change them later remove the 
# mysql docker volumes (make rm) and restart (make run).

# Default values, but NEED to be set in order for the application to work correctly.
MYSQL_DATABASE_USER = 'user'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'db'
MYSQL_DATABASE_HOST = 'mysql'

CENTRAL_IP = "http://95.217.178.90"

SECRET_KEY = 'super-secret'
