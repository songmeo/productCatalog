# Product Catalog
Python REST API using flask, sqlalchemy and marshmallow.
<br>
```
src/
├── api/
|   ├── utils/
|   |   └── database.py 
|   ├── config/
|   |   └── config.py
|   ├── models/   
|   |   └── model.py
|   ├── routes/
|   |   ├── category.py
|   |   └── product.py
|   └── tests/
|       ├── test_categories.py
|       └── test_products.py
├── run.py
├── main.py
├── requirements.txt
└── README.md
```
## Usage
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
  python run.py
```
* Run unit tests:
```
  python -m unittest discover src/api/tests
```
