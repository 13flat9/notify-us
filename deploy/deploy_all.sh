
./create_resource_group.sh
if [ $? -ne 0 ]; then
  echo "Failed to create resource group" >&2
  exit 1
fi

#needed here to put in environment variables
db_app_password="$(echo $RANDOM | md5sum | head -c 25)"

echo "Deploying ARM templates"
./arm_templates_deploy.sh
if [ $? -ne 0 ]; then
  echo "Failed to deploy ARM templates" >&2
  exit 1
fi

echo "deploying app code"
./func_code_deploy.sh
if [ $? -ne 0 ]; then
  echo "Failed to deploy app code" >&2
  exit 1
fi

echo "creating database user"
# shellcheck disable=SC2153
db_app_password=$DB_APP_PASSWORD
#pipe hides the string, parameter would show it
echo "$db_app_password" | ./create_db_user.sh
if [ $? -ne 0 ]; then
  echo "Failed to create database user" >&2
  exit 1
fi

echo "creating database tables"
source ../.venv/bin/activate
if [ $? -ne 0 ]; then
  echo "Failed to activate venv" >&2
  exit 1
fi
python3 create_tables.py
if [ $? -ne 0 ]; then
  echo "Failed to create database tables" >&2
  exit 1
fi

echo "Deployment successful"