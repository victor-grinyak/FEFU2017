## Quick Start

### Dependencies

```pip3.6 install -r requirements.txt```

### Setup web server

Caddyfile example

```
example.com {
    proxy /api http://localhost:5000/
    #header / Access-Control-Allow-Origin  * #for development only
    #header / Access-Control-Allow-Methods "GET, POST, DELETE" #for development only
    root /path/to/project/static
    log log.log
    gzip {
        level 9
    }
}
```
### Run

```python3.6 memap.py```