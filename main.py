import json,requests, argparse, hmac, hashlib, datetime, base64
from typing import Optional

class Logger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def log(self, type, message):
        if self.verbose:
            print(f"[{type}] {message}")
    def error(self, message):
        #if self.verbose:
        print(f"[-] {message}")
        quit()

logger = None

def login(endpoint, username, secret):
    headers = {'Content-Type' : 'application/json', 'accept': 'application/json'}
    data = {
        "login_method" : "secret",
        "username" : username,
        "secret" : secret
    }
    r = requests.post(f'{endpoint}/api/v2/login', headers=headers, json=data)
    if r.status_code == 200:
        return r.json().get('data', {}).get('session_token')
    else:
        logger.error('Could not login with the given credentials!')

def upload_queries(endpoint, queries, auth):
    global logger
    errors = {}
    url = f'{endpoint}/api/v2/saved-queries'
    headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }
    headers.update(auth)
    for query in queries:
        r = requests.post(url, headers=headers, json=query)
        if r.status_code != 201:
            errors[query['name']] = r.json()['errors']
    
    success = len(queries) - len(errors.keys())
    if success > 0:
        print(f'[+] {success}/{len(queries)} queries uploaded successfully!')
    if len(errors.keys()) > 0:
        print(f'[!] {len(errors.keys())}/{len(queries)} queries did not upload successfully! Use verbose flag (-v) to get more information.')
        for item, error in errors.items():
            logger.log('!', f'Error "{' '.join([msg['message'] for msg in error])}" occurred on query {item}')
    
def parse_queries(fname, description):
    global logger
    queries = []
    if not description:
        description = f"Custom query imported from {fname}"
    try:
        data = open(f'{fname}').read()
        json_data = json.loads(data)["queries"]
        for data in json_data:
            name = data['name']
            cyper = data['queryList'][0]['query']
            query = {"name": name, "query": cyper, "description": description}
            logger.log('*', f'Parsed query: {query}')
            queries.append(query)
    except Exception as ex:
        logger.error(f'Could not parse queries: {ex}')
    logger.log('*', f'Parsed {len(queries)} queries')
    return queries

def parse_arguments():
    parser = argparse.ArgumentParser(description='Upload custom queries to Bloodhound-CE\n\nhttps://x.com/chr0x6eos\nhttps://github.com/Chr0x6eOs\n____________________________________________________________________________', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--filename', required=True, help='The JSON filename containing the query data, see example.json for formatting')
    parser.add_argument('-u', '--username', required=True, help='The username for authentication')
    parser.add_argument('-p', '--password', required=True, help='The password for authentication')
    parser.add_argument('-e', '--endpoint', help='The Bloodhound-CE enpoint (default: http://localhost:8080)', default='http://localhost:8080')
    parser.add_argument('-d', '--description', help='Add a custom description to the created queries. Default: "Custom query imported from <filename>"')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose mode (default: False)')

    return parser.parse_args()

def main(endpoint, username, password, filename, description):
    token = login(endpoint, username, password)
    auth = {'Authorization': f'Bearer {token}'}
    queries = parse_queries(filename, description)
    upload_queries(endpoint, queries, auth)

if __name__ == '__main__':
    args = parse_arguments()
    logger = Logger(args.verbose)
    main(args.endpoint, args.username, args.password, args.filename, args.description)