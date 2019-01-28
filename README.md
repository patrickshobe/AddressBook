# AddressBook

AddressBook is a simple address book that ties into the [USPS City/State Lookup API](https://www.usps.com/business/web-tools-apis/address-information-api.htm#_Toc532390356) to verify
and/or look up the correct city and state for a zip code. 

## Screen Shots

### Main Page
![main page](https://i.imgur.com/dxrcKMm.png)

### Add Address Page
![add address page](https://i.imgur.com/zmRwF8v.png)

### City/State Look Up Page
![City/State Lookup Page](https://i.imgur.com/vvZ1rjT.png)

## Tech Stack

- [Flask](http://flask.pocoo.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLite](https://sqlite.org/index.html)

## To Run Locally

1. Clone the repo
2. Install the dependencies using your preferred environment manager
3. Set your `FLASK_APP` env variable to `address_book.py`
4. Set your 'USPS_APP' env variable to your USPS user id
5. Set up the database `flask db init`, `flask db migrate`, `flask db upgrade`
6. Run the tests `python spec.py`
7. to run the server `flask run` visit `localhost:5000`
8. to run the shell `flask shell`

## Issues
Please open issues for any bugs
