
if [ "$#" -ne 1 ]; then
    echo "$0 <Lambda input JSON file>"
    exit 1
fi

inputFile=$1
python ./runLambda.py ${inputFile}
