# A parser &amp; encoder for ads.txt files.

#### Setup

```bash
./setup.py install
```

#### Parsing adstxt files
```python
import adstxt

# parse from the web
data = adstxt.loadw('https://washingtonpost.com/ads.txt')

# parse a file
with open('ads.txt') as f:
    data = adstxt.load(f)

# parse a string
data = adstxt.loads(http_response.read())

```

#### Writing adstxt files

```python
import adstxt

data = adstxt.loadw('https://washingtonpost.com/ads.txt')

# write to a file
with open('ads.txt', 'w') as f:
    adstxt.dump(data, f)

# dump to a string
adstxt_string = adstxt.dumps(data)
```

#### Data Structure

```javascript
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
```