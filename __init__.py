

from io import StringIO
import re

'''
Adstxt File JSON format. Same structure as https://www.npmjs.com/package/ads.txt

{
    "fields": [
        {
            "domain": "openx.com",
            "publisherAccountID": "343560932",
            "accountType": "DIRECT",
            "certificateAuthorityID": "38f6ae102b"
        }, 
        {
            "domain": "kargo.com",
            "publisherAccountID": "105",
            "accountType": "DIRECT",
            "comment": "banner"
        }
        ...
    ]
    "variables": {
        "subdomain": ["divisionone.example.com", "divisiontwo.example.com"],
        "contact": "Jane Doe"
        ...
    }

}

'''

FIELD_DELIMITER = ','
NEW_LINE_CHAR = '\n'

_var_row_patt = re.compile(r'^[a-zA-Z]+\w?=\w+$')

def _parse_var(var_row_str):
    if _var_row_patt.match(var_row_str):
        parts = var_row_str.split('=')
        return {parts[0]:parts[1]}
    else:
        return None


def _lazy_eval(r):
    if isinstance(r, str):
        return (line for line in r.split(NEW_LINE_CHAR))


# Parsers.
def loads(adstxt_string):
    
    data = {"fields":[], "variables":{}}

    for line in (l.strip() for l in _lazy_eval(adstxt_string)):
        
        # Check if line is comment or if line is key-value pair
        if line.startswith('#'):
            continue
        var_pair = _parse_var(line)
        if var_pair:
            data["variables"] = {**data["variables"], **var_pair}
            continue
        
        row = line.split(FIELD_DELIMITER)
        rowData = {}
        if len(row) == 0:
            continue
        if "#" in row[-1]:
            rowData["comment"] = row[-1].split("#")[1].strip()
            row[-1] = row[-1].split("#")[0].strip() # Remove comment from last field
        
        for ix, val in enumerate(v.strip() v for row):
            if ix == 0:
                rowData["domain"] = val
            elif ix == 1:
                rowData["publisherAccountID"] = val
            elif ix == 2:
                rowData["accountType"] = val
            elif ix == 3:
                rowData["certificateAuthorityID"] = val

        data['fields'].append(rowData)
    


def loadw(web_resource):
    pass


def load(f_file):
    pass


# Encoders.
def dumps(data, header=None, footer=None):
    pass


def dump(data, f_file):
    pass