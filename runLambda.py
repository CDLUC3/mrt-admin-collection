import sys
import importlib

try:
    mod = importlib.import_module('createProfile')
    functionHandler = 'lambda_handler'
    lambdaFunction = getattr(mod, functionHandler)

    fc = open(sys.argv[1], "r")
    data = fc.read()
    event = { 'file' : data }
    context = {}
    fc.close()

    print lambdaFunction(event, context)
except Exception as error:
    print error
