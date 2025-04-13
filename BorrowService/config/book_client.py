import os
from dotenv import load_dotenv
import requests


load_dotenv()

# BookService URL (for inter-service communication)
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL")


def fetch_book(book_id: str, auth_header: str):
    '''
    fetch book details from BookService
    '''

    # Attach the header
    headers = {"Authorization": auth_header}  

    try:
        response = requests.get(f"{BOOK_SERVICE_URL}/get-book-by-bookid/{book_id}", headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()  # Return book details as a dictionary
        
        else:
            return None  # No book found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching book: {e}")
        
        return None
    

def update_book(book_id, status: str):
    '''
    update BookService for available_copies
    '''

    try:
        response = requests.put(f"{BOOK_SERVICE_URL}/update-available-copies/{book_id}", json={"status": status}, timeout=30)
        
        if response.status_code == 200:
            return response.json()  # Return book details as a dictionary
        
        else:
            return None  # No book found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching book: {e}")
        
        return None