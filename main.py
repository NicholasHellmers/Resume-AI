from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os

from urllib.parse import urlparse

import argparse

from dotenv import load_dotenv

import time
import sys

def scrape_profile(given_url, env_username, env_password):
    # Creating a webdriver instance
    driver = webdriver.Chrome("Enter-Location-Of-Your-Web-Driver")
    # This instance will be used to log into LinkedIn
    
    # Opening linkedIn's login page
    driver.get("https://linkedin.com/uas/login")
    
    # waiting for the page to load
    time.sleep(5)
    
    # entering username
    username = driver.find_element(By.ID, "username")
    
    # In case of an error, try changing the element
    # tag used here.
    
    # Enter Your Email Address
    username.send_keys(env_username)
    
    # entering password
    pword = driver.find_element(By.ID, "password")
    # In case of an error, try changing the element 
    # tag used here.
    
    # Enter Your Password
    pword.send_keys(env_password)
    
    # Clicking on the log in button
    # Format (syntax) of writing XPath --> 
    # //tagname[@attribute='value']
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # In case of an error, try changing the
    # XPath used here.

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
    if args.scrape_profile_url:
        scrape_profile(args.scrape_profile_url[0], username, password)

if __name__ == "__main__":
    main()