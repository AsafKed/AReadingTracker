# Scraping libraries
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import from .env
import os
from dotenv import load_dotenv
load_dotenv()
from classes.Book import Book
from classes.Author import Author

class GoodReadsScraper:
    def __init__(self, hide=False):
        self.CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
        self.driver = None
        self.hide = hide
        self.gr_URL = 'https://www.goodreads.com/'

    def createDriver(self):
        print ("Creating driver -- GoodReads")
        # Webdriver options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_experimental_option("detach", True) # Keep browser open
        if self.hide is True:
            chrome_options.add_argument('headless')

        self.driver = webdriver.Chrome(options=chrome_options)
        # driver.get('https://www.goodreads.com/')

    def closeDriver(self):
        if self.driver is None:
            print("No driver to close")
        else:
            print ("Closing GoodReads")
            self.driver.quit()

    def searchBook(self, bookName):
        def extract_rating_and_count(rating_text):
            # Split the text into parts using '—' as the separator
            parts = rating_text.split(' — ')
            # The first part contains 'avg rating' and the actual rating number, we split it by spaces and take the first part
            rating = parts[0].split()[0]
            # The second part contains 'ratings' and the actual ratings count, we remove commas and 'ratings' to get the number
            rating_count = parts[1].split()[0].replace(',', '')
            
            return rating, rating_count
        
        print ("Searching for book")
        # turn the spaces in the string to plus signs
        bookName = bookName.replace(" ", "+")
        self.driver.get(f'{self.gr_URL}search?q={bookName}')

        books = []

        book_blocks = self.driver.find_elements(by=By.XPATH, value='//tr[@itemscope and @itemtype="http://schema.org/Book"]')
        for book_block in book_blocks:
            try:
                # Extract book title
                name_el = book_block.find_element(by=By.CLASS_NAME, value='bookTitle')
                book_title = name_el.text
                book_link = name_el.get_attribute('href')
                
                # Extract authors
                authors_list = []
                author_els = book_block.find_elements(by=By.CLASS_NAME, value='authorName')
                for auth_el in author_els:
                    author_name = auth_el.text
                    author_link = auth_el.get_attribute('href')
                    authors_list.append(Author(author_name, author_link))  # Create Author object and append to list
                
                # Extract rating
                rating_el = book_block.find_element(by=By.CLASS_NAME, value='minirating')
                rating, rating_count = extract_rating_and_count(rating_el.text)
                
                # Create Book object with all information
                book = Book(title=book_title, link=book_link, authors=authors_list, rating=rating, rating_count=rating_count)
                
                # Add the Book object to the books list
                books.append(book)
                
            except Exception as e:
                print("Error while parsing a book block:", e)
        
        # At this point, 'books' is a list of Book objects with all the required data
        return books
    
    def getBookInfo(self):
        print ("Getting book info")

    def saveBookToDB(self):
        print ("Saving book to DB")

