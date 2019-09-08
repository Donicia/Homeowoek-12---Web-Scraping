from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    mission_to_mars = mongo.db.mission_to_mars.find_one()
    return render_template('index.html', mission_to_mars=mission_to_mars)


@app.route('/scrape')
def scrape():
    mission_to_mars = mongo.db.mission_to_mars
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemisphere()
    mission_to_mars.update({},
                            data,
                            upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
