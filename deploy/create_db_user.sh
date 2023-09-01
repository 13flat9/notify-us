# Azure postgres database information
db_host="${DB_SERVER_NAME}.postgres.database.azure.com"
db_port="5432"
admin_password="$placeholder_admin_pw"

# New user information
new_username="$DB_APP_USERNAME"
read new_user_password # Getting this as an argument would make it visible in ps

# Create the new user using psql
psql "sslmode=require dbname=$DB_NAME host=$db_host port=$db_port user=$DB_ADMIN password=$admin_password"<< EOF
    CREATE USER $new_username WITH PASSWORD '$new_user_password';
    GRANT CONNECT, CREATE ON DATABASE $DB_NAME TO $new_username;
EOF
