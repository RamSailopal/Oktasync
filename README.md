# Okta Data Import

![example workflow](https://github.com/RamSailopal/Oktasync/actions/workflows/check.yml/badge.svg)

An example of extracting data out of a csv file and then importing it into Okta using the [Okta Python SDK](https://github.com/okta/okta-sdk-python)

Each line of user data is processed. A check is carried out to see if the user already exists or not and if not, the user is setup in the Okta user directory. A complete list of the users in the Okta directory is then output.

An alternative csv file import is also available within the Okta platform but such a method means that automation cannot be achieved,

## Raw Data

Example raw data is stored in the **okta/dump.csv** file where the first comma separated value is the forename, the second the surname and the last value the email address.

## Running the script

With Python3, Python3-venv and pip3 installed, run:

    
    python3 -m venv .
    bin/pip install -r requirements,txt
    export OKTADOMAIN="<your Okta domain>"
    export OKTATOKEN="<Your Okta API token>"
    bin/python3 okta/sync.py -f <file path>

file path signifies the path to dump.csv file 

Further details on setting up an Okta API token can be found [here](https://developer.okta.com/docs/guides/create-an-api-token/main/)



