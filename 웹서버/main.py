from flask import Flask, render_template
import crawler
app = Flask(__name__)


@app.route('/')
def home():
    return crawler.gethtml("https://www.google.com/")


if __name__ == '__main__':
    app.run()
