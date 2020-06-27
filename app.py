from flask import Flask, render_template, request
from datetime import date, datetime
import requests
import config


app = Flask("NasaPhotoApp")


def return_page_with_photo_info(photo_date, find_photo_text):
	url = 'https://api.nasa.gov/planetary/apod'
	payload = {"api_key": config.api_key, "date": photo_date}
	
	response = requests.get(url, params=payload)
	
	nasa_img_of_day_data = response.json()
	
	img_expl = nasa_img_of_day_data['explanation']
	img_title = nasa_img_of_day_data['title']
	img_url = nasa_img_of_day_data['url']

	date = photo_date.strftime("%a %-d %B, %Y")
	print(date)

	return render_template("photo.html", explanation=img_expl, title=img_title, image=img_url, date=date, find_photo_text=find_photo_text)


@app.route("/")
def home_page():
	return render_template("index.html")


@app.route("/photo")
def photo_page():
	today = date.today()
	return return_page_with_photo_info(today, "Find past photos of the day")


@app.route("/pastphoto", methods=['POST'])
def past_photo_page():
	form_date = request.form["date"]
	date = datetime.strptime(form_date, "%Y-%m-%d").date()
	return return_page_with_photo_info(date, "Find another photo of the day")


@app.route("/mars")
def mars_page():
	return render_template("mars.html")


@app.route("/about")
def about_page():
	return render_template("about.html")


app.run(debug=True)