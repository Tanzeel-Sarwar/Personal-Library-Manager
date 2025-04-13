import json
import os

def display_menu():
    """Display the main menu options"""
    print("\nPersonal Library Manager")
    print("1. Add a new book")
    print("2. Remove a book")
    print("3. Search for books")
    print("4. Display all books")
    print("5. Mark a book as read/unread")
    print("6. View statistics")
    print("7. Save library to file")
    print("8. Load library from file")
    print("9. Exit")

def add_book(library):
    """Add a new book to the library"""
    print("\nAdd a New Book")
    
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    year = input("Enter publication year: ").strip()
    genre = input("Enter genre: ").strip()
    
    # Validate year input
    while not year.isdigit():
        print("Please enter a valid year (numbers only).")
        year = input("Enter publication year: ").strip()
    
    read_status = input("Have you read this book? (yes/no): ").strip().lower()
    while read_status not in ['yes', 'no']:
        print("Please answer with 'yes' or 'no'.")
        read_status = input("Have you read this book? (yes/no): ").strip().lower()
    
    book = {
        'title': title,
        'author': author,
        'year': int(year),
        'genre': genre,
        'read': read_status == 'yes'
    }
    
    library.append(book)
    print(f"'{title}' has been added to your library!")

def remove_book(library):
    """Remove a book from the library"""
    if not library:
        print("Your library is empty!")
        return
    
    print("\nRemove a Book")
    display_all_books(library)
    
    try:
        choice = int(input("Enter the number of the book to remove: ")) - 1
        if 0 <= choice < len(library):
            removed_book = library.pop(choice)
            print(f"'{removed_book['title']}' has been removed from your library.")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Please enter a valid number.")

def search_books(library):
    """Search for books by various criteria"""
    if not library:
        print("Your library is empty!")
        return
    
    print("\nSearch Options")
    print("1. Search by title")
    print("2. Search by author")
    print("3. Search by genre")
    print("4. Search by year")
    print("5. Search by read status")
    
    try:
        search_option = int(input("Choose a search option (1-5): "))
    except ValueError:
        print("Please enter a number between 1 and 5.")
        return
    
    search_term = input("Enter your search term: ").strip().lower()
    found_books = []
    
    for book in library:
        if search_option == 1 and search_term in book['title'].lower():
            found_books.append(book)
        elif search_option == 2 and search_term in book['author'].lower():
            found_books.append(book)
        elif search_option == 3 and search_term in book['genre'].lower():
            found_books.append(book)
        elif search_option == 4 and search_term == str(book['year']):
            found_books.append(book)
        elif search_option == 5:
            if (search_term == 'read' and book['read']) or (search_term == 'unread' and not book['read']):
                found_books.append(book)
    
    if found_books:
        print(f"\nFound {len(found_books)} matching book(s):")
        display_all_books(found_books)
    else:
        print("No books found matching your criteria.")

def display_all_books(library):
    """Display all books in the library with numbering"""
    if not library:
        print("Your library is empty!")
        return
    
    print("\nYour Library:")
    for i, book in enumerate(library, 1):
        status = "Read" if book['read'] else "Unread"
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} [{status}]")

def toggle_read_status(library):
    """Mark a book as read or unread"""
    if not library:
        print("Your library is empty!")
        return
    
    display_all_books(library)
    
    try:
        choice = int(input("Enter the number of the book to toggle read status: ")) - 1
        if 0 <= choice < len(library):
            library[choice]['read'] = not library[choice]['read']
            status = "read" if library[choice]['read'] else "unread"
            print(f"'{library[choice]['title']}' is now marked as {status}.")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Please enter a valid number.")

def show_statistics(library):
    """Display basic statistics about the library"""
    if not library:
        print("Your library is empty!")
        return
    
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    unread_books = total_books - read_books
    
    # Count books by genre
    genre_counts = {}
    for book in library:
        genre = book['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Find the oldest and newest books
    years = [book['year'] for book in library]
    oldest_year = min(years) if years else None
    newest_year = max(years) if years else None
    
    print("\nLibrary Statistics")
    print(f"Total books: {total_books}")
    print(f"Read books: {read_books}")
    print(f"Unread books: {unread_books}")
    
    if oldest_year and newest_year:
        print(f"Oldest book published in: {oldest_year}")
        print(f"Newest book published in: {newest_year}")
    
    print("\nBooks by genre:")
    for genre, count in genre_counts.items():
        print(f"{genre}: {count} book(s)")

def save_library(library):
    """Save the library to a JSON file"""
    filename = input("Enter filename to save (e.g., my_library.json): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        with open(filename, 'w') as file:
            json.dump(library, file)
        print(f"Library saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")

def load_library():
    """Load the library from a JSON file"""
    filename = input("Enter filename to load (e.g., my_library.json): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return None
    
    if not os.path.exists(filename):
        print("File does not exist.")
        return None
    
    try:
        with open(filename, 'r') as file:
            library = json.load(file)
        print(f"Library loaded from {filename} successfully!")
        return library
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def main():
    """Main program loop"""
    library = []
    
    print("Welcome to your Personal Library Manager!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            toggle_read_status(library)
        elif choice == '6':
            show_statistics(library)
        elif choice == '7':
            save_library(library)
        elif choice == '8':
            loaded_library = load_library()
            if loaded_library is not None:
                library = loaded_library
        elif choice == '9':
            print("Goodbye! Happy reading!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()