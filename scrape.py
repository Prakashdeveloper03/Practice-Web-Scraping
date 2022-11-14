import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={"id": "priceblock_ourprice"}).string.strip()
    except AttributeError:
        try:
            price = soup.find(
                "span", attrs={"id": "priceblock_dealprice"}
            ).string.strip()
        except Exception:
            price = ""
    return price


# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find(
            "i", attrs={"class": "a-icon a-icon-star a-star-4-5"}
        ).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={"class": "a-icon-alt"}).string.strip()
        except Exception:
            rating = ""
    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={"id": "acrCustomerReviewText"}
        ).string.strip()
    except AttributeError:
        review_count = ""
    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={"id": "availability"})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available


if __name__ == "__main__":
    webpage = requests.get(
        "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2",
        headers={"User-Agent": "", "Accept-Language": "en-US, en;q=0.5"},
    )  # HTTP Request
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={"class": "a-link-normal s-no-outline"})
    links_list = [link.get("href") for link in links]
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get(
            "https://www.amazon.com" + link,
            headers={"User-Agent": "", "Accept-Language": "en-US, en;q=0.5"},
        )
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        d["title"].append(get_title(new_soup))
        d["price"].append(get_price(new_soup))
        d["rating"].append(get_rating(new_soup))
        d["reviews"].append(get_review_count(new_soup))
        d["availability"].append(get_availability(new_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df["title"].replace("", np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=["title"])
    amazon_df.to_csv("data/amazon_data.csv", header=True, index=False)
