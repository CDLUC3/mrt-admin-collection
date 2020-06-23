
# Create input for owner profile create
jo -p TYPE="owner" \
  ENVIRONMENT="development" \
  NAME="admin_test_owner" \
  DESCRIPTION="Test owner only, please delete" \
  COLLECTION="ark:/99999/testowner" \
  ARK="ark:/99999/testark" \
  NOTIFICATION=$(jo -a "testowneremail01@cdlib.org" "testemail02@cdlib.org" "testemail03@cdlib.org") \
  STORAGENODE="9999" \
  CREATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z") \
  MODIFICATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z")
