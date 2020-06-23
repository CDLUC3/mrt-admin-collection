
# Create input for collection profile create
jo -p TYPE="collection" \
  ENVIRONMENT="development" \
  NAME="admin_test_collection" \
  DESCRIPTION="Test collection only, please delete" \
  ARK="ark:/99999/testark" \
  OWNER="ark:/99999/testowner" \
  NOTIFICATION=$(jo -a "testemail01@cdlib.org" "testemail02@cdlib.org" "testemail03@cdlib.org") \
  STORAGENODE="9999" \
  CREATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z") \
  MODIFICATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z")
