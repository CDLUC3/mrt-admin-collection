
# Create input for owner profile create
jo -p TYPE="profile" \
  ENVIRONMENT="development" \
  NAME="admin_test_profile" \
  DESCRIPTION="Test profile only, please delete" \
  COLLECTION="ark:/99999/testcollection" \
  OWNER="ark:/99999/testowner" \
  ARK="ark:/99999/testark" \
  CONTEXT="admin_test_profile_content" \
  NOTIFICATION=$(jo -a "testprofileemail01@cdlib.org" "testemail02@cdlib.org" "testemail03@cdlib.org") \
  STORAGENODE="9999" \
  CREATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z") \
  MODIFICATIONDATE=$(date "+%Y-%m-%dT%H:%M:%S%:z")
