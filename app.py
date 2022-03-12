from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from pprint import pprint
import scraping

#set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define route for HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    pprint(mars)
    return render_template("index.html", mars=mars)

#define route for scraping
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# tell flask to run
if __name__ == "__main__":
    app.run(debug=True)