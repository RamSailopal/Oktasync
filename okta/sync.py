"""Python script to extract users out of a csv file and sync them with Okta user directory"""
import asyncio
import csv
import os
import sys
import argparse
from okta.client import Client as OktaClient # pylint: disable=import-error

parser = argparse.ArgumentParser(prog="sync.py",
                                 description="Sync a CSV file with Okta user directory",
                                 epilog="-f Path to csv file")
parser.add_argument("-f", "--file", dest="fil", default="okta/dump.csv")
args = parser.parse_args()
if not os.path.exists(args.fil):
    print("ERROR - " + args.fil + " cannot be found")
    sys.exit(1)
if os.getenv('OKTATOKEN') is None or os.getenv('OKTATOKEN') == "":
    print("ERROR - OKTATOKEN variable not set")
    sys.exit(1)
if os.getenv('OKTADOMAIN') is None or os.getenv('OKTADOMAIN') == "":
    print("ERROR - OKTADOMAIN variable not set")
    sys.exit(1)
config = {
    'orgUrl': 'https://' + os.getenv('OKTADOMAIN'),
    'token': os.getenv('OKTATOKEN')
}
okta_client = OktaClient(config)

# example of usage, list all users and print their first name and last name
async def main():
    """Function for listing users in Okta"""
    users, okta_resp, err= await okta_client.list_users()
    if users is not None and err is None and okta_resp is not None:
        for user in users:
            print(user.profile.firstName + " " + user.profile.lastName + " - " + user.profile.email)

async def create():
    """Function for creating a user"""
    with open('okta/dump.csv', 'r', encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            user = await okta_client.get_user(row[2])
            if user is None:
                print("Adding "  + row[2])
                body = {
                    "profile": {
                    "firstName": row[0],
                    "lastName": row[1],
                    "email": row[2],
                    "login": row[2],
                    }
                }
                result, okta_resp, err = await okta_client.create_user(body)
                if err is None and okta_resp is not None:
                    print(result)
            else:
                print(row[2] + " already exists")

loop = asyncio.get_event_loop()
loop.run_until_complete(create())
loop.run_until_complete(main())
