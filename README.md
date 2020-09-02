getnet-py [![Build Status](https://travis-ci.org/ramon/getnet-py.svg?branch=master)](https://travis-ci.org/ramon/getnet-py) [![Coverage Status](https://coveralls.io/repos/github/ramon/getnet-py/badge.svg?branch=master)](https://coveralls.io/github/ramon/getnet-py?branch=master)
=========

This project provider a SDK to handler with Santander Getnet API.

Installation
------------

To install getnet-py you can use pip:

    $ pip install getnet-py

or pipenv:

    $ pipenv install getnet-py

    
Usage
-----

For use this library the following information is needed:
 
 * Seller ID
 * Client ID
 * Client Secret
 
The following environments are supported:

 * Staging
 * Homolog
 * Production
 
### Instancing the client
```python
from getnet import Environment, Client

client = Client("seller_id", "client_id", "client_secret", Environment.SANDBOX)
client.auth() # Optional, will be executed if needed
``` 

### Using the Services
With client instanced, the services can be accessed in two ways:

Using the client shotcuts:
```python
service = client.token_service()
service.generate(...)
```

or instancing the services and passing the client as the first param:
```python
from getnet.services.token import Service

service = Service(client)
service.generate(...)
```

At moment, we have support to the following services:

 * Token
 * Cards (Cofre) 
 * Payments
   * Credit Card
   * Boleto
 * Subscriptions
   * Customers
   * Plans
   * Charges 
 

Author
------

Ramon Soares <contact@ramon.dev.br>
