import sqlite3
import requests
from bs4 import BeautifulSoup

class Database:
    def __init__(self, db_name='sites.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def add_site(self, url):
        try:
            self.cursor.execute('INSERT INTO sites (url) VALUES (?)', (url,))
            self.conn.commit()
            print(f"Site {url} added to the database.")
        except sqlite3.IntegrityError:
            print(f"Site {url} is already in the database.")

    def clear_database(self):
        self.cursor.execute('DELETE FROM sites')
        self.conn.commit()
        print("Database cleared.")

    def get_all_sites(self):
        self.cursor.execute('SELECT * FROM sites')
        return self.cursor.fetchall()


class WebParser:
    def parse_site(self, url, search_query):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()

        # Simple search for the query in the text content
        result_count = text_content.lower().count(search_query.lower())
        return result_count


class UserInterface:
    def __init__(self, database, web_parser):
        self.database = database
        self.web_parser = web_parser

    def run(self):
        while True:
            print("\n1. Add a site to the database")
            print("2. Clear the database")
            print("3. Search for information")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                url = input("Enter the site URL: ")
                self.database.add_site(url)
            elif choice == '2':
                self.database.clear_database()
            elif choice == '3':
                search_query = input("Enter the search query: ")
                sites = self.database.get_all_sites()
                results = self.search_information(sites, search_query)
                self.display_results(results)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def search_information(self, sites, search_query):
        results = []

        for site in sites:
            url = site[1]
            result_count = self.web_parser.parse_site(url, search_query)
            results.append((url, result_count))

        # Sort results by result count in descending order
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def display_results(self, results):
        print("\nSearch Results:")
        for result in results:
            print(f"{result[0]} - {result[1]} occurrences")


def run():
    db = Database()
    parser = WebParser()
    ui = UserInterface(db, parser)
    ui.run()


if __name__ == "__main__":
    run()
