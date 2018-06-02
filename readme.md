## Build a Flask app with the MongoDB API on the Azure Portal



## Application stack and tools
Framework/tool | Description
----------------- | -----------------
[Flask](http://flask.pocoo.org/) | Backend micro-framework. Parses and handles HTTP requests.
[Python](https://www.python.org/) | Version 3.4.6
[pymongo](https://api.mongodb.com/python/current/) | Python distribution containing tools for working with MongoDB

The first step in creating your app is to create the web app via the [Azure Portal](https://portal.azure.com).

1. Log into the Azure Portal, click 'App Service' and then click the ** +Add **  button in the top.
2. Click **Web App ** to create the new App Service


You then need to add **db_url, db_user and db_password** to the application settings under Azure.

## Code Example

### Sample to create an instance of the Flask class for our web app

```python

app = Flask(__name__)

```


#### Sample code for connecting to MongoDB on Azure

```python
client = MongoClient(os.environ["db_url"])
db = client.admin     
db.authenticate(name=os.environ["db_user"],password=os.environ["db_password"] )
```

#### Sample code for handling HTTP request

```python
@app.route('/')
@app.route('/pets', methods=['GET'])
def get_all_pets():

    output = []
    heading = "Pet List"

    for s in pets.find():
       output.append({'_id' : s['_id'],
                      'origin' : s['origin'], 'name' : s['name'],
                      'categoryName' : s['categoryName'],
                      'status' : s['status'] , 'age' : s['age'] })
    return render_template('home.html',pets=output,t=title,h=heading)   
```
