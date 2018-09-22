
#!/usr/bin/env python3

import contextlib
from io import StringIO
import re
import urllib.request

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
_d = FIELD_DELIMITER
NEW_LINE_CHAR = '\n'

_var_row_patt = re.compile(r'^[a-zA-Z]+\S?=\S+$')

def _parse_var(var_row_str):
    if _var_row_patt.match(var_row_str):
        return var_row_str.split('=')
    else:
        return None


def _lazy_eval(r):
    if isinstance(r, str):
        return (line for line in r.split(NEW_LINE_CHAR))



# Parsers.

def loads(adstxt_string):
    
    data = {"fields":[], "variables":{}}

    for line in (l.strip() for l in _lazy_eval(adstxt_string)):

        # Check if line is comment or if line is key-value pair or blank line
        if line == '':
            continue
        if line.startswith('#'):
            continue
        var_pair = _parse_var(line)
        if var_pair:
            if var_pair[0] not in data["variables"]:
                data["variables"][var_pair[0]] = var_pair[1]
            elif isinstance(data["variables"][var_pair[0]], list):
                data["variables"][var_pair[0]].append(var_pair[1])
            else:
                elem_0 = data["variables"][var_pair[0]]
                data["variables"][var_pair[0]] = [elem_0, var_pair[1]]
            continue
        
        row = line.split(FIELD_DELIMITER)

        rowData = {}
        if len(row) == 0:
            continue
        if "#" in row[-1]:
            rowData["comment"] = row[-1].split("#")[1].strip()
            row[-1] = row[-1].split("#")[0].strip() # Remove comment from last field
        
        for ix, val in enumerate(v.strip() for v in row):
            if ix == 0:
                rowData["domain"] = val
            elif ix == 1:
                rowData["publisherAccountID"] = val
            elif ix == 2:
                rowData["accountType"] = val
            elif ix == 3:
                rowData["certificateAuthorityID"] = val

        data['fields'].append(rowData)
    return data
    

def load(f_file):
    return loads(f_file.read())


def loadw(url):
    with contextlib.closing(urllib.request.urlopen(url)) as resp:
        return loads(resp.read().decode())



# Encoders.

def dumps(data, header=None):

    with contextlib.closing( StringIO() ) as f_file:
        dump(data, f_file, header=header)
        f_file.seek(0)
        return f_file.read()
    

def dump(data, f_file, header=None):
    if header:
        f_file.write((('# ' if not header.strip().startswith('#') else '')
                        + header
                        + '\n#\n'))
    
    for r in data['fields']:
        comment = data.get('comment')
        caid = data.get('certificateAuthorityID')
        f_file.write(f"{r['domain']}{_d} {r['publisherAccountID']}{_d} {r['accountType']}{_d+' '+caid if caid else ''}{' # '+comment if comment else ''}{NEW_LINE_CHAR}")
    
    for key, val in data.get('variables', {}).items():
        if isinstance(val, list):
            for v in val:
                f_file.write(f"{key}={v}{NEW_LINE_CHAR}")
        else:
            f_file.write(f"{key}={val}{NEW_LINE_CHAR}")
                
    return f_file