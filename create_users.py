import argparse
import json
import boto3
import csv

client = boto3.client('identitystore', region_name='us-west-2')


def create_user(sso_id_storeid,
    user_name,
    given_name,
    family_name,
    group_name,
    email):

    display_name = "{} {}".format(given_name, family_name)
    create_user_response = client.create_user(
        IdentityStoreId=sso_id_storeid,
        UserName=user_name,
        Name={
            'FamilyName': family_name,
            'GivenName': given_name
        },    
        Emails=[
        {
            'Value': email,
            'Type': 'string',
            'Primary': True
        },
    ],
        DisplayName=display_name
    )
    user_id = create_user_response["UserId"]
    print(f"User:{user_name} with UserId:{user_id} created successfully")
    
    get_group_id_response = client.get_group_id(
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'displayName',
                'AttributeValue': group_name
            }
        },
        IdentityStoreId=sso_id_storeid
    )

    create_group_membership_response = client.create_group_membership(
        GroupId=(get_group_id_response["GroupId"]),
        IdentityStoreId=sso_id_storeid,
        MemberId={
            'UserId': user_id
        }
    )
        
    print(f"User:{user_name} added to Group:{group_name} successfully")


if __name__ == '__main__':
    csv_file_path = input("Enter the path of the CSV file: ")
    sso_id_storeid = input ("Enter the SSO Identity Store ID: ")
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            username = row['username']
            first_name = row['firstName']
            last_name = row['lastName']
            group_name = 'Students'
            email = row['emailAddress']
            response = create_user(sso_id_storeid,
            username,
            first_name,
            last_name,
            group_name,
            email)

            print(response)
    
