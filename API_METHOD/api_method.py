import requests
import mysql.connector
import json

# configuration
# APIKEY generated from https://legiscan.com
APIKEY = '5e466f356dde2014db14d483c993aec1'
base_url = 'https://api.legiscan.com/?key=' + APIKEY

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'XieXuhan23.',
    'database': 'bridge_legal',
}


def get_session_list():
    data = {'op': 'getSessionList'}
    try:
        response = requests.get(url=base_url, params=data)
        response.raise_for_status()  # Check for HTTP errors

        content = response.content
        obj = json.loads(content)['sessions']

        # Save the JSON data to a file
        with open('session_list.json', 'w') as json_file:
            json.dump(obj, json_file, indent=4)

        print('JSON data saved to session_list.json')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # store the data downloaded to the mysql database
    store_sessions('./session_list.json')


def get_bill_list():
    with open('session_list.json', 'r') as json_file:
        json_data = json.load(json_file)
    merged_data = []
    for item in json_data:
        data = {'op': 'getMasterList',
                'id': item['session_id']}
        try:
            response = requests.get(url=base_url, params=data)
            if response.status_code == 200:
                json_bill = response.json()['masterlist']
                # we only want bill data
                if isinstance(json_bill, dict):
                    for key in json_bill:
                        if 'bill_id' in json_bill[key]:
                            obj = json_bill[key]
                            obj['session_id'] = data['id']
                            merged_data.append(obj)
                else:
                    print("JSON data is not an object (dictionary).")
            else:
                print(f"Failed to download JSON from {item['session_id']}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    output_file = "bill_list.json"
    with open(output_file, "w") as outfile:
        json.dump(merged_data, outfile, indent=4)
    print(f"Merged data saved to {output_file}")


def get_people_list():
    with open('session_list.json', 'r') as json_file:
        json_data = json.load(json_file)
    merged_data = []
    for item in json_data:
        data = {'op': 'getSessionPeople',
                'id': item['session_id']}
        try:
            response = requests.get(url=base_url, params=data)
            if response.status_code == 200:
                json_people = response.json()['sessionpeople']['people']
                for p in json_people:
                    p['session_id'] = data['id']
                merged_data.extend(json_people)
            else:
                print(f"Failed to download JSON from {item['session_id']}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading JSON from {item['session_id']}: {str(e)}")
    output_file = "people_list.json"
    with open(output_file, "w") as outfile:
        json.dump(merged_data, outfile, indent=4)

    print(f"Merged data saved to {output_file}")


def get_amendment_list():
    merged_data = []
    for i in range(1, 5001):
        data = {'op': 'getAmendment',
                'id': i}
        try:
            response = requests.get(url=base_url, params=data)
            if response.status_code == 200:
                json_amendment = response.json()
                obj = json_amendment['amendment']
                merged_data.append(obj)
            else:
                print(f"Failed to download JSON from amendment id {i}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading JSON from amendment id {i}: {str(e)}")
    output_file = "amendment_list.json"
    with open(output_file, "w") as outfile:
        json.dump(merged_data, outfile, indent=4)
    print(f"Merged data saved to {output_file}")


'''
jsonpath is the path of data downloaded from the get functions above.
'''


def store_sessions(jsonpath):
    # Read JSON data from a file
    with open(jsonpath, 'r') as json_file:
        json_data = json.load(json_file)
    # Establish a connection to MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Insert JSON data into the table
        for item in json_data:
            insert_query = "INSERT IGNORE INTO sessions (session_id, state_id, year_start, year_end, prefile, sine_die, prior, special, session_tag, session_title, session_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # Execute the INSERT statement with the data
            cursor.execute(insert_query, (
                item['session_id'],
                item["state_id"],
                item["year_start"],
                item["year_end"],
                item["prefile"],
                item["sine_die"],
                item["prior"],
                item["special"],
                item["session_tag"],
                item["session_title"],
                item["session_name"]
            ))
        conn.commit()
        print("Data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


def store_people(jsonpath):
    # Read JSON data from a file
    with open(jsonpath, 'r') as json_file:
        json_data = json.load(json_file)
    # Establish a connection to MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Insert JSON data into the table
        for item in json_data:
            insert_query = """
                INSERT INTO people (
                    people_id, party_id, state_id, party, role_id, role,
                    name, first_name, middle_name, last_name, suffix, nickname, district,
                    ftm_eid, votesmart_id, opensecrets_id, knowwho_pid, ballotpedia,
                    bioguide_id, committee_sponsor, committee_id, state_federal, session_id
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """
            # Execute the INSERT statement with the data
            cursor.execute(insert_query, (
                item['people_id'],
                item['party_id'],
                item['state_id'],
                item['party'],
                item['role_id'],
                item['role'],
                item['name'],
                item['first_name'],
                item['middle_name'],
                item['last_name'],
                item['suffix'],
                item['nickname'],
                item['district'],
                item['ftm_eid'],
                item['votesmart_id'],
                item['opensecrets_id'],
                item['knowwho_pid'],
                item['ballotpedia'],
                item['bioguide_id'],
                item['committee_sponsor'],
                item['committee_id'],
                item['state_federal'],
                item['session_id']
            ))
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def store_bills(jsonpath):
    # Read JSON data from a file
    with open(jsonpath, 'r') as json_file:
        json_data = json.load(json_file)
    # Establish a connection to MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Insert JSON data into the table
        for item in json_data:
            # solve valid date in mysql database
            if item["last_action_date"] == "0000-00-00":
                item["last_action_date"] = None
            insert_query = insert_statement = """
                INSERT INTO bills (bill_id, number, url, status_date, status, last_action_date, last_action, title, description, session_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the INSERT statement with the data
            cursor.execute(insert_query, (
                item['bill_id'],
                item['number'],
                item['url'],
                item['status_date'],
                item['status'],
                item['last_action_date'],
                item['last_action'],
                item['title'],
                item['description'],
                item['session_id']
            ))
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def store_amendments(jsonpath):
    # Read JSON data from a file
    with open(jsonpath, 'r') as json_file:
        json_data = json.load(json_file)
    # Establish a connection to MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Insert JSON data into the table
        for item in json_data:
            # solve valid date in mysql database
            if item["date"] == "0000-00-00":
                item["date"] = None
            insert_query = """
                INSERT INTO amendments
                (amendment_id, bill_id, adopted, date, title, description, url, state_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            # Execute the INSERT statement with the data
            cursor.execute(insert_query, (
                item['amendment_id'],
                item['bill_id'],
                item['adopted'],
                item['date'],
                item['title'],
                item['description'],
                item['url'],
                item['state_link']
            ))
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


'''
Please run functions below inorder due to the API designed by the website
'''
# get_session_list()
# store_sessions('./session_list.json')

# get_people_list()
# store_people('./people_list.json')

# get_bill_list()
# store_bills('./bill_list.json')

# getAmendmentList()
# store_amendments('./amendment_list.json')
