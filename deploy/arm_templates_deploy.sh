timestamp="$(date +%s)"
#echo "Please enter an admin password for the database:"
#read -s db_admin_pw
db_admin_pw="$placeholder_admin_pw"
home_ip_address="$(dig +short myip.opendns.com @resolver1.opendns.com)"

trap '' SIGINT  # if deployment doesn't finish, it can't rerun immediately. Therefore trap SIGINT.
                # Note: can't put a command like echo there since it would interrupt deployment anyway

az deployment group create \
  --name "function-app-deployment-""$timestamp"\
  --resource-group "$resource_group" \
  --template-file app_resources.json \
  --parameters dbAdminPw="$db_admin_pw" dbAdmin="$DB_ADMIN" dbServerName="$DB_SERVER_NAME" dbName="$DB_NAME" dbUserPassword="$DB_APP_PASSWORD"\
  functionAppName="$function_app_name" homeIpAddress="$home_ip_address" @app_resources.parameters.json

if [ $? -ne 0 ]; then
  echo "Failed to deploy ARM templates" >&2
  exit 1
fi
