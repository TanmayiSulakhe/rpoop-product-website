from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import get_products
import smtplib


app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route("/<str>")
def results_page(str):
    plist = []
    get_products.amazon_products(str,plist)
    get_products.flipkart_products(str,plist)

    filtered_and_sorted_list = []


    min_rating = 4
    min_price = 0
    max_price = 1000

    
    for entry in plist:
        entry['price'] = (entry['price'].replace('₹', '').replace(',', ''))
        if ' ' in entry['price']:
            rate, garbage = entry['rating'].split(' ')
            entry['price'] = rate
        if (float(entry['price']) >= min_rating) and (float(entry['price']) <= max_price) and (float(entry['price']) >= min_price):
            filtered_and_sorted_list.append(entry)

    sorted_list = sorted(filtered_and_sorted_list, key=lambda x: x['price'])
    return render_template('results.html', products=plist)
    

@app.route("/search",methods=['GET','POST'])
def search_page():
    if request.method == "POST":
        search_query = request.form["nm"]
        search_query = search_query.replace(" ","+")
        return redirect(url_for('results_page',str=search_query))
    else:
        return render_template('search.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/contact+us")
def contact_page():
    return render_template("contact_us.html")


if __name__ == '__main__':
    app.run(debug=True)


