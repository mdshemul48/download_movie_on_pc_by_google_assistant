from flask import Flask, request
from guessit import guessit
from difflib import SequenceMatcher
import requests


app = Flask(__name__)


class Movie:
    # this api given by my isp. alternatively you can use any torrent site by scraping search result.
    api_url = "http://circleftp.net/custom_search"

    def __init__(self, movie):
        # this init will get the movie and store in the obj
        self.movie_full_title = movie

    def extract_info(self,):
        # this will extract movie title and year confirmation while searching for the movie...
        try:
            movie_info = guessit(self.movie_full_title)
        except:
            self.name = self.movie_full_title
            self.year = 0
        else:
            self.name = movie_info["title"]
            try:
                self.year = movie_info["year"]
            except KeyError:
                self.year = 0

    def searching_for_the_movie(self):
        # this method will search using given api
        result = requests.get(self.api_url, params={"value": self.name}).json()
        movie_download_info = {}
        for movie in result:
            movie_title = guessit(movie["name"])
            try:
                movie_name, movie_year = movie_title["title"], movie_title["year"]

            except KeyError:
                continue

            else:
                # this will match my requested movie name to the searched movie name. if both name match more then 80% then after
                # that it will match year if year not given by ifttt api then it will match again with name and see if name match more then 90%.
                # if it not match then it will not do anythung. it will return empty dict.
                if SequenceMatcher(None, movie_name, self.name).ratio() * 100 >= 80:
                    if self.year != 0 and self.year == movie_year or SequenceMatcher(None, movie_name, self.name).ratio() * 100 >= 90:
                        movie_download_info["title"] = movie["name"]
                        movie_download_info["link"] = movie["media"]
                        break
                else:
                    continue
        self.movie_download_info = movie_download_info
        # It returning because i have to check if search api found any movie or not. if the dict is not empty then i will start downloading the movie
        return movie_download_info


@app.route("/")
def movie_download():
    # this function will receive movie request from ifttt webhooks
    reqtested_text = request.args.get("movie_download")
    movie = Movie(reqtested_text)
    movie.extract_info()

    # movie.searching_for_the_movie() will return a dict. checking lenth of the dict.. if dict != 0 that mean movie found. else movie not found.
    if len(movie.searching_for_the_movie()) != 0:
        print("movie found by api")
    else:
        print("movie not found")

    print(reqtested_text)
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True)
