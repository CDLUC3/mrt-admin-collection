import git      # see install/system for installation
from cgi import parse_qs    # Form submission
import json
import os
import sys
import tempfile
from string import Template
from wsgiref import simple_server, util     # Wgsi test server

def getRepo(environment):
    repoDir = "mrtProfile"
    # SSH key access, by host
    profileURL = "git@github.com:cdlib/mrt-ingest-profile.git"

    if not os.path.exists(repoDir):
        git.Repo.clone_from(profileURL, repoDir)

    repo = git.Repo(repoDir)
    b = repo.git.checkout("origin/" + environment)
    repo.git.pull('origin',environment)
    return repo

def createCollection(repo, collectionData):
    templateType = collectionData['TYPE']
    templateName = "TEMPLATE-" + templateType.upper()
    path = repo.working_dir
    if (templateType != "profile"):
        path += "/admin/" + collectionData['ENVIRONMENT'] + "/" + templateType
    templatePath = path + "/" + templateName
    template = open(templatePath, 'r').read()
    
    # hacky way of iterating over mulitple email targets, if supplied
    newTemplate= template
    for i,email in enumerate(collectionData['NOTIFICATION']):
        if (i+1 < len(collectionData['NOTIFICATION'])):
            email += "\nNotification.${NOTIFICATIONENUM}: ${NOTIFICATION}"
        newTemplate = Template(newTemplate).safe_substitute(NOTIFICATIONENUM=i+1, NOTIFICATION=email)

    # Process remaining vars
    for key in collectionData.keys(): 
        if (key != 'NOTIFICATION'):
            d = dict()
            d[key] = collectionData[key]
            newTemplate = Template(newTemplate).safe_substitute(d)
    
    if ( os.environ.get('DRYRUN') ):
        print newTemplate
        exit()
    return newTemplate

def processFile(collectionInput):
    collectionData = json.loads(collectionInput)

    # grab profile repo
    repo = getRepo(collectionData['ENVIRONMENT'])

    # create collection file
    newCollection = createCollection(repo, collectionData)
    f = repo.working_dir + "/admin/" + collectionData['ENVIRONMENT'] + "/collection/" + collectionData['NAME']
    # create only, do not update
    if os.path.exists(f):
        raise Exception("[ERROR]: Collection already exists: " + collectionData['NAME'])
    fc = open(f, "w")
    fc.write(newCollection)
    fc.close()

    # commit collection file
    repo.git.add(f)
    repo.index.commit("Commit from collection_profile.py/"+ collectionData['NAME'])
    
    # push, force HEAD to origin
    repo.git.push("origin", "HEAD:" + collectionData['ENVIRONMENT'])
    response = "Created collection profile: " + collectionData['NAME'] + " in branch: " + collectionData['ENVIRONMENT']
    print response
    return response


# process form via wsgi
def application(environ, start_response):
    from werkzeug.formparser import parse_form_data
    stream, form, file = parse_form_data(environ)
    inputData = file['file'].read()

    # Return body (with no exception)
    response_headers = [('Content-type', 'text/plain')]
    try:
       response_body = str(processFile(inputData) + "\n")
       status = "200 OK"
    except Exception as e:
        status = "400 Bad Request"
        response_body = str(e) + "\n"

    
    start_response(status, response_headers)
    return [response_body]

# process a lambda request
def lambda_handler(event, context):
    return processFile(event['file'])

def testWsgi():
    httpd = simple_server.make_server('', 8000, application)
    print("Serving on port 8000, control-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()

def main():
    if len(sys.argv) != 2:
        print "Usage: ", sys.argv[0], " <collection input file> | wsgi"
        print ""
        print "Create collection profile in profile repo"
        print "Can be called from Lambda, WSGI or CLI"
        exit (0)

    # Test wsgi if no args
    if sys.argv[1].lower() == "wsgi":
        testWsgi()
        exit(0)

    collectionInputFile =  sys.argv[1]
    if not os.path.exists(collectionInputFile):
        raise Exception("Collection Input file does not exist: ", collectionInputFile)

    fc = open(collectionInputFile, "r")
    processFile(fc.read())
    fc.close()

    exit(0)


# start of main
if __name__ == "__main__":
    main()
