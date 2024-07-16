from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import lxml

import os

from urllib.parse import urlparse

import hashlib

import argparse

from dotenv import load_dotenv

import time
import sys

from dataclasses import dataclass

@dataclass
class Experience:
    title = str
    company = str
    location = str
    start_date = str
    end_date = str
    duration = str
    description = str

@dataclass
class Post:
    type = str
    title = str
    content = str
    likes = int
    comments = int
    shares = int

@dataclass
class Profile:
    name = str
    headline = str
    location = str
    about = str
    recient_posts = list[]


def parse_profile_html(url_hash: str) -> None:
    src = open("./scraped_urls/profiles/" + url_hash, "r", encoding="utf-8").read()

    if src == None or src == "":
        print("Error reading the file")
        return

    # Now using beautiful soup
    soup = BeautifulSoup(src, 'lxml')

    # Get the url of the profile, sits on the first line of the file
    profile_url = src.split("\n")[0]

    # Get the name of the person
    name = soup.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words").text.strip()

    # Get the headline of the person
    headline = soup.find("div", class_="text-body-medium break-words").text.strip()

    # Get the location of the person
    location = soup.find("span", class_="text-body-small inline t-black--light break-words").text.strip()

    about = soup.find("div", class_="display-flex ph5 pv3").text.replace("…see more", "").strip()

    recient_posts = soup.find("ul", class_="display-flex flex-wrap list-style-none justify-space-between")

    recient_posts = recient_posts.find_all("li")

    for post in recient_posts:
        post_type = post.find("span", class_="feed-mini-update-contextual-description__text").text.strip()
        post_title = post.find("span", class_="break-words").text.strip()
        post_content = post.find("div", class_="feed-shared-update-v2__description-wrapper ember-view").text.strip()
        post_likes = post.find("button", class_="social-details-social-counts__reactions-count").text.strip()
        post_comments = post.find("button", class_="social-details-social-counts__comments-count").text.strip()
        post_shares = post.find("button", class_="social-details-social-counts__shares-count").text.strip()

        print(f"Post Type: {post_type}")
        print(f"Post Title: {post_title}")
        print(f"Post Content: {post_content}")
        print(f"Post Likes: {post_likes}")
        print(f"Post Comments: {post_comments}")
        print(f"Post Shares: {post_shares}")

    print(f"Name: {name}")
    print(f"Headline: {headline}")
    print(f"Location: {location}")
    print(f"About: {about}")


def scrape_profile(given_url: str, env_username: str, env_password: str) -> int:
    # Creating an instance
    service = Service(executable_path="./driver/chromedriver")
    chrome_options = Options()

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Logging into LinkedIn
    driver.get("https://linkedin.com/uas/login")
    time.sleep(5)
    
    username = driver.find_element(By.ID, "username")
    username.send_keys(env_username)  # Enter Your Email Address
    
    pword = driver.find_element(By.ID, "password")
    pword.send_keys(env_password)        # Enter Your Password
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    driver.get(given_url)        # this will open the link

    start = time.time()
 
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll 
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000
    
        # we will stop the script for 3 seconds so that 
        # the data can load
        time.sleep(3)
        # You can change it as per your needs and internet speed
    
        end = time.time()
    
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 20:
            break

    src = driver.page_source

    # Write the HTML of the page to a file
    with open(given_url, "a", encoding="utf-8") as file:
        file.write(src)
        print(f"HTML of the page written to file at {given_url}")

    return 0

def main():
    # Load the .env file
    if not load_dotenv():
        print("Error loading .env file")
        sys.exit(1)

    # Get the username and password from the .env file
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    # Check if the username and password are not None or empty, if so print an error message and exit the program
    if username == None or password == None or username == "" or password == "":
        print("Please provide a username and password in the .env file")
        sys.exit(1)
    else:
        print(f"Username and password found in .env file with username: {username} and password: {password}")

    parser = argparse.ArgumentParser(
                    prog='resume-bud',
                    description='This program has a few functions that can help you with your resume based on infomation you provide.',
                    epilog='Text at the bottom of help')
    
    subparsers = parser.add_subparsers()

    # Create a subparser for the ScrapeProfile function
    scrape_profile_parser = subparsers.add_parser("ScrapeProfile",
                                                  help="Scrape a LinkedIn profile by giving the URL")
    
    # If the function is ScrapeProfile, expect a url argument to be passed with it
    scrape_profile_parser.add_argument("scrape_profile_url", 
                                       help="The URL of the LinkedIn profile you want to scrape", 
                                       nargs=1)
    
    args = parser.parse_args()

    # If the function is ScrapeProfile, call the scrape_profile function
    if args.scrape_profile_url[0] != None or args.scrape_profile_url[0] != "":
    
        url_hash = hashlib.sha256(args.scrape_profile_url[0].encode()).hexdigest()
        print(f"URL: {args.scrape_profile_url[0]}")
        print(f"URL Hash: {url_hash}")
        print(f"File location: {'./scraped_urls/profiles/' + url_hash}")

        if os.path.exists("./scraped_urls/profiles/" + url_hash):
            while True:
                response = input("The URL has been scraped before. Do you want to scrape the URL again? (Y/N): ")
                if response.lower() == "y":
                    if scrape_profile(args.scrape_prfile_url[0], username, password) > 0:
                        print("Error scraping profile")
                    else:
                        print("Successfully scraped scraped this profile")
                    break
                elif response.lower() == "n":
                    parse_profile_html(url_hash)
                    return 0
                else:
                    print("Please enter a valid response")
            return
        else:
            with open("./scraped_urls/profiles/" + url_hash, "w") as file:
                print(f"Created file at {'./scraped_urls/profiles/' + url_hash}")
                file.write(args.scrape_profile_url[0] + "\n")
                if scrape_profile(args.scrape_prfile_url[0], username, password) > 0:
                    print("Error scraping profile")
                else:
                    print("Successfully scraped scraped this profile")

    return 0

    


if __name__ == "__main__":
    main()