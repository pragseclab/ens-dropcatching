import json
import requests
import logging
import time
from datetime import datetime
import os

# Utility function to write content to a JSON file
def write(content, filename):
    with open(filename, 'w') as f:
        json.dump(content, f)

# Generalized function to collect data from the ENS Subgraph
def collect_from_subgraph(start_time, query, filename_prefix, folder):
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    api_key = "YOUR_API_KEY_HERE"
    subgraph_id = "5XqPmWe6gjyrJtFn9cLy237i4cWw2j9HcUJEXsP5qGtH" # ENS Subgraph ID
    url = f'https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}'

    response = requests.post(url, headers=headers, json=query)
    try:
        data = response.json()
        write(data, f'{folder}/{filename_prefix}_{start_time}.json')
        return data
    except Exception as e:
        logging.error(f"Error during data retrieval: {e}")
        return False

# Helper function to build query string
def build_query(entity, conditions, fields):
    return {
        "query": f"""
        query MyQuery {{
            {entity}(orderBy: {conditions['orderBy']}, where: {{{conditions['filter']}}}, first: 1000, orderDirection: {conditions['orderDirection']}) {{
                {fields}
            }}
        }}"""
    }

# Collect all registrations from the ENS Subgraph
def collect_all_registrations():
    logging.info("Start collection from ENS Subgraph.")
    start_time = 0

    while True:
        conditions = {
            'orderBy': 'registrationDate',
            'filter': f'registrationDate_gt: "{start_time}"',
            'orderDirection': 'asc'
        }
        fields = """
            registrationDate
            domain {
                name
                createdAt
                expiryDate
                subdomainCount
            }
            events {
                ... on NameRegistered {
                    transactionID
                    blockNumber
                    expiryDate
                    registrant { id }
                }
                ... on NameRenewed {
                    transactionID
                    blockNumber
                    expiryDate
                }
                ... on NameTransferred {
                    blockNumber
                    transactionID
                    newOwner { id }
                }
            }
        """
        query = build_query('registrations', conditions, fields)
        registrations_data = collect_from_subgraph(start_time, query, 'registrations', 'registrations')

        if not registrations_data:
            break

        registrations = registrations_data['data']['registrations']
        start_time = registrations[-1]['registrationDate']
        logging.info(f"Collected registrations from {start_time}")
        time.sleep(1)

    logging.info("Completed registration collection.")
    return True

# Collect domain events from the ENS Subgraph
def collect_domain_events():
    logging.info("Start domain-events collection from ENS Subgraph.")
    start_time = 0
    total = 0

    while True:
        conditions = {
            'orderBy': 'createdAt',
            'filter': f'createdAt_gt: "{start_time}"',
            'orderDirection': 'asc'
        }
        fields = """
            id
            name
            createdAt
            events(orderBy: blockNumber) {
                ... on NewOwner {
                    transactionID
                    blockNumber
                    owner { id }
                }
                ... on Transfer {
                    transactionID
                    blockNumber
                    owner { id }
                }
                ... on NameWrapped {
                    transactionID
                    blockNumber
                    expiryDate
                    owner { id }
                }
                ... on ExpiryExtended {
                    transactionID
                    blockNumber
                    expiryDate
                }
            }
        """
        query = build_query('domains', conditions, fields)
        events_data = collect_from_subgraph(start_time, query, 'domain-events', 'domain-events')

        if not events_data:
            break

        events = events_data['data']['domains']
        total += len(events)
        start_time = events[-1]['createdAt']
        logging.info(f"Collected domain events from {start_time}, total: {total}")
        time.sleep(0.5)

    logging.info("Completed domain-events collection.")
    return True

# Collect all domain names and their creation dates from the ENS Subgraph
def collect_all_domains():
    logging.info("Start collection of all domain names and creation dates from ENS Subgraph.")
    start_time = 0
    total = 0

    while True:
        conditions = {
            'orderBy': 'createdAt',
            'filter': f'createdAt_gt: "{start_time}"',
            'orderDirection': 'asc'
        }
        fields = "name createdAt"
        query = build_query('domains', conditions, fields)
        domains_data = collect_from_subgraph(start_time, query, 'domains', 'domains')

        if not domains_data:
            break

        domains = domains_data['data']['domains']
        total += len(domains)
        start_time = domains[-1]['createdAt']
        logging.info(f"Collected domain names from {start_time}, total: {total}")
        time.sleep(0.5)

    logging.info("Completed domain collection.")
    return True

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs('registrations', exist_ok=True)
    os.makedirs('domain-events', exist_ok=True)
    os.makedirs('domains', exist_ok=True)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H',
        filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"
    )

    collect_all_registrations()
    collect_domain_events()
    collect_all_domains()
