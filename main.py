from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os

from urllib.parse import urlparse

import argparse

from dotenv import load_dotenv

import time
import sys

def scrape_profile(url, username, password):
    pass

def main():
    # Load the .env file
    load_dotenv()

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
    scrape_profile_parser.add_argument("url", 
                                       help="The URL of the LinkedIn profile you want to scrape", 
                                       nargs=1)
    
    args = parser.parse_args()

    print(args.url)

    
                        


if __name__ == "__main__":
    main()