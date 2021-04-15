from flask import Flask, render_template, request
from datetime import date, datetime
import requests
import os


app = Flask("NasaPhotoApp")


@app.route("/")
def home_page():
	return render_template("index.html")


########## Astronomy Photo of the Day ##########

def return_page_with_photo_info(photo_date, find_photo_text):
	url = 'https://api.nasa.gov/planetary/apod'
	payload = {"api_key": os.environ["NASA_API_KEY"], "date": photo_date}
	
	response = requests.get(url, params=payload)
	
	nasa_img_of_day_data = response.json()
	
	img_expl = nasa_img_of_day_data['explanation']
	img_title = nasa_img_of_day_data['title']
	img_url = nasa_img_of_day_data['url']

	date = photo_date.strftime("%a %-d %B, %Y")

	return render_template("apod.html",
				explanation=img_expl,
				title=img_title,
				image=img_url,
				date=date,
				find_photo_text=find_photo_text)


@app.route("/apod-today")
def photo_page():
	today = date.today()
	return return_page_with_photo_info(today, "Find past photos of the day")


@app.route("/apod-search", methods=['POST'])
def past_photo_page():
	form_date = request.form["date"]
	date = datetime.strptime(form_date, "%Y-%m-%d").date()
	return return_page_with_photo_info(date, "Find another photo of the day")


############## Mars Rover Photos ##############


def get_rover_info(rover_name):
	url = 'https://api.nasa.gov/mars-photos/api/v1/manifests/' + rover_name
	payload = {"api_key": os.environ["NASA_API_KEY"]}
	response = requests.get(url, params=payload)
	rover_data = response.json()
	del rover_data["photo_manifest"]["photos"]
	return rover_data["photo_manifest"]


@app.route("/mars-rover")
def mars_page():
	curiosity_data = get_rover_info("Curiosity")
	spirit_data = get_rover_info("Spirit")
	opportunity_data = get_rover_info("Opportunity")
	rover_data = [curiosity_data, spirit_data, opportunity_data]
	return render_template("mars-search.html", rover_data=rover_data)


@app.route("/mars-rover-search", methods=['POST'])
def mars_photo_page():
	camera_type = request.form["camera"]
	sol = request.form["sol"]
	rover = request.form["rover"]

	# If sol not entered in search, default to 1000
	if not sol:
		sol = "1000"

	url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/' + rover + '/photos'
	payload = {"api_key": os.environ["NASA_API_KEY"], "sol": sol, "camera": camera_type}
	response = requests.get(url, params=payload)
	
	mars_rover_data = response.json()
	photo_results = mars_rover_data["photos"]

	if not photo_results:
		return render_template("mars-noresults.html")
	else:
		return render_template("mars-photo.html",
					photo_results=photo_results,
					camera=camera_type,
					sol=sol,
					rover=rover.title())


@app.route("/about")
def about_page():
	return render_template("about.html")


if __name__ == '__main__':
	app.run(debug=True)