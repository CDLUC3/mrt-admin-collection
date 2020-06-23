# Merritt collection creation tools

The Merritt collection creation process has always been a manual operation.
The steps are loosely defined and error prone and lend themselved to automation.

This is a prototype of creating extensible tools that can be used as building
blocks with a goal of creating an Merritt admin interface.

### Installation
- Install Form parser
	`pip install Werkzeug` 

- Install JSON creation tool JO
	`https://github.com/jpmens/jo`

### Overview
Ingest profiles are housed at *https://github.com/cdlib/mrt-ingest-profile*

Merritt environments are defined as branches in this repository 
1. development
2. stage
3. production

Creation of User/Collection/Owner/SLA profiles is done by supplying user inputs to
templates which then are processed resulting in the target profile checked into the repo.

Authentication to the github repo is done through SSH keys
### Processing

** Command Line Interface **
Create JSON formatted input using the following shell scripts
- input_collection.sh
- input_owner.sh
- input_profile.sh
- input_sla.sh

Save output to a file and use as input to Python script createProfile.py

To dry run the procedure, set the ENV variable DRYRUN
	`DRYRUN=1 python createProfile.py col01.json`

** WSGI served **
Use Apache or other web server to support the WSGI component of createProfile.py
Testing can be done by running script with the argument *wsgi*
	`python createProfile.py wsgi`

An http POST can be used to supply JSON input to WSGI. 
	`curl -F "file=@profile01.json" http://localhost:8000`

** Lambda served **
A Lambda function is also included in createProfile.py
Testing can be done by using a test python script and wrapper:
- runLambda.py
- runLambda.sh
