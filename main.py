from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        url = request.form["url"]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title_elem = soup.find("span", {"id": "productTitle"})
        title = title_elem.text.strip() if title_elem else ""
        offerprice_elem = soup.find("span", {"class": "a-price-whole"})
        offerprice = offerprice_elem.text.strip() if offerprice_elem else ""
        price_elem = soup.find("span", {"class": "a-price a-text-price"})
        price = (
            price_elem.find("span", {"class": "a-offscreen"}).text.strip()
            if price_elem
            else ""
        )
        img_elem = soup.find("img", {"id": "landingImage"})
        imglink = img_elem["src"] if img_elem else ""
        words = title.split()
        words = words[:8]

        maintitle = " ".join(words)

        return render_template(
            "greet.html",
            url=url,
            title=maintitle,
            offerprice=offerprice,
            price=price,
            imglink=imglink,
        )
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
