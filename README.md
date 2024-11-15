# BloodHound-CE-Custom-Query-uploader

Created to upload custom queries such as [azurehound-queries](https://github.com/emiliensocchi/azurehound-queries)

## Usage

```bash
~$ python3 main.py -h
usage: main.py [-h] -f FILENAME [-u USERNAME] [-p PASSWORD] [-e ENDPOINT] [-d DESCRIPTION] [-v]

Upload custom queries to Bloodhound-CE

https://x.com/chr0x6eos
https://github.com/Chr0x6eOs
____________________________________________________________________________

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The JSON filename containing the query data, see example.json for formatting
  -u USERNAME, --username USERNAME
                        The username for authentication
  -p PASSWORD, --password PASSWORD
                        The password for authentication
  -e ENDPOINT, --endpoint ENDPOINT
                        The Bloodhound-CE enpoint (default: http://localhost:8080)
  -d DESCRIPTION, --description DESCRIPTION
                        Add a custom description to the created queries. Default: "Custom query imported from <filename>"
  -v, --verbose         Enable verbose mode (default: False)
```

### Example

```bash
~$ python3 main.py --filename example.json --username <USERNAME> --password <PASSWORD>  
[+] 2/2 queries uploaded successfully!
```