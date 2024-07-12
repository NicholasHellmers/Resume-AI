from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import argparse

import time
import sys

def main():

    parser = argparse.ArgumentParser(
                    prog='LinkedIn Scraper',
                    description='This program takes in a LinkedIn Profile URL and scrapes the profile\'s information',
                    epilog='The format of the URL should be: lparse <PROFILE_URL>')
    
    parser.add_argument('URL',
                        metavar='URL',
                        type=str,
                        help='The URL of the LinkedIn Profile to scrape')

    args = parser.parse_args()
    print(args.URL)
    


if __name__ == "__main__":
    main()