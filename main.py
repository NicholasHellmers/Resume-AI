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

def parse_profile_html(file_path: str) -> None:
    src = open(file_path, "r", encoding="utf-8").read()

    # Now using beautiful soup
    soup = BeautifulSoup(src, 'lxml')

    # Extracting the HTML of the complete introduction box
    # that contains the name, company name, and the location
    intro = soup.find('div', {'class': 'ph5'})
    
    # print(intro)

    # In case of an error, try changing the tags used here.

    name_loc = intro.find("h1")

    # Extracting the Name
    name = name_loc.get_text().strip()
    # strip() is used to remove any extra blank spaces

    works_at_loc = intro.find("div", {'class': 'text-body-medium'})

    # this gives us the HTML of the tag in which the Company Name is present
    # Extracting the Company Name
    works_at = works_at_loc.get_text().strip()


    location_loc = intro.find_all("span", {'class': 'text-body-small'})

    # Ectracting the Location
    # The 2nd element in the location_loc variable has the location
    location = location_loc[0].get_text().strip()

    print("Name -->", name,
        "\nWorks At -->", works_at,
        "\nLocation -->", location)
    
    # Getting the HTML of the Experience section in the profile
    experience = soup.find("section", {"id": "experience-section"}).find('ul')
    
    print(experience)

    # In case of an error, try changing the tags used here.

    li_tags = experience.find('div')
    a_tags = li_tags.find("a")
    job_title = a_tags.find("h3").get_text().strip()

    print(job_title)

    company_name = a_tags.find_all("p")[1].get_text().strip()
    print(company_name)

    joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()

    employment_duration = a_tags.find_all("h4")[1].find_all(
        "span")[1].get_text().strip()

    print(joining_date + ", " + employment_duration)

def scrape_profile(given_url: str, env_username: str, env_password: str) -> int:

    if os.path.exists(given_url):
        while True:
            response = input("The URL has been scraped before. Do you want to scrape the URL again? (Y/N): ")
            if response.lower() == "y":
                break
            elif response.lower() == "n":
                return 0
            else:
                print("Please enter a valid response")
        return
    else:
        with open(given_url, "w") as file:
            print(f"Created file at {given_url}")
            file.write(given_url + "\n")

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
        url_hash_file = f"./scraped_urls/profiles/{url_hash}"

        if scrape_profile(url_hash_file, username, password) > 0:
            print("Error scraping profile")
        else:
            print("Successfully scraped or already scraped this profile")
            parse_profile_html(url_hash_file)


if __name__ == "__main__":
    main()