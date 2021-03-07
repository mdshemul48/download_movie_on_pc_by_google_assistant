from flask import Flask, request
from guessit import guessit
app = Flask(__name__)

class Movie:
    def __init__(self, movie):
        # this init will get the movie and store in the obj
        self.movie_full_title = movie

    def extract_info(self,):
        # this will extract movie title and year confirmation while searching for the movie...
        movie_info = guessit(self.movie_full_title)
        self.name = movie_info["title"]
        try:
            self.year = movie_info["year"]
        except KeyError:
            self.year = 0



@app.route("/")
def movie_download():
    # this function will reasive movie request from ifttt webhooks
    reqtested_text = request.args.get("movie_download")
    movie = Movie(reqtested_text)
    movie.extract_info()
    print(reqtested_text)
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True)
