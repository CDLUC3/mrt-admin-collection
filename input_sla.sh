
# Create input for owner profile create
jo -p TYPE="sla" \
  ENVIRONMENT="development" \
  NAME="admin_test_sla" \
  DESCRIPTION="Test sla only, please delete" \
  ARK="ark:/99999/testark" \
  NOTIFICATION=$(jo -a "testslaemail01@cdlib.org" "testemail02@cdlib.org" "testemail03@cdlib.org") \
  STORAGENODE="9999" \
  CREATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z") \
  MODIFICATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z")
