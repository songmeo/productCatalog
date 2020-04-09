# Product Catalog
A simple python REST API using flask, sqlalchemy and marshmallow.
```
venv/
├── src/
|   ├── api/
|   |   ├── utils/
|   |   |   └── database.py 
|   |   ├── config/
|   |   |   └── config.py
|   |   ├── models/   
|   |   |   └── model.py
|   |   ├── routes/
|   |   |   ├── category.py
|   |   |   └── product.py
|   |   └── tests/
|   |       ├── test_categories.py
|   |       └── test_products.py
|   ├── run.py
|   └── main.py
├── requirements.txt
└── README.md
```
## Deploy:
* Build:
```
  git clone https://github.com/songmeo/productCatalog
```
* Install dependencies:
```
  pip install -r requirements.txt
```
* Run application:
```
  python src/run.py
```
* Run unit tests inside `src` folder:
```
  cd src && python -m unittest discover api/tests
```
## Documentation:
[OpenAPI](https://app.swaggerhub.com/apis-docs/songmeo/productCatalog/0.1-oas3#/default)
