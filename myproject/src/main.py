import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import re

# File paths
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
USER_FILE = os.path.join(DATA_FOLDER, "user.csv")
MOVIE_FILE = os.path.join(DATA_FOLDER, "imdb_movie_dataset.csv")

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Ensure user CSV exists with error handling
try:
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "email", "password"])
except Exception as e:
    print(f"Error creating user file: {e}")

# Account Management
class Account:
    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def save_account(self):
        with open(USER_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.__username, self.__email, self.__password])
        print(f"Welcome {self.__username}!")

    def __str__(self):
        return f"Account(username={self.__username}, email={self.__email})"

    def __repr__(self):
        return f"Account('{self.__username}', '{self.__email}', '****')"

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.__username == other.__username
        return False

    def __len__(self):
        return len(self.__username)

class User(Account):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)

    def save_account(self):
        super().save_account()
        print("Account created successfully!")

# Create new account
def create_account():
    username = input("Enter a username (at least 8 characters): ")
    email = input("Enter your email (e.g., abc@gmail.com): ")
    password = input("Enter a password: ")
    confirm_password = input("Confirm your password: ")

    while not len(username) >= 8:
        print("Username must be at least 8 characters long (including spaces).")
        username = input("Enter a username: ")

    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    
    while not re.match(r"[^@]+@[^@]+\.[^@]+", email) or email.split("@")[1] not in domains:
        print("Invalid email format. Please enter a valid email address (e.g., gmail.com, yahoo.com, outlook.com, hotmail.com).")
        email = input("Enter your email again: ")

    special_chars = ["!", "@", "#", "$", "%", "?", "*", "+", ")", "(", "&"]

    while (len(password) < 8 or
           password.isupper() or
           password.islower() or
           password.isdigit() or
           not any(char in special_chars for char in password)):
        print("Password is Weak. It must be at least 8 characters long, contain both uppercase and lowercase letters, a number, and a special character.")
        password = input("Enter a password: ")

    while password != confirm_password:
        print("Passwords do not match. Try again.")
        confirm_password = input("Confirm your password: ")
    try:
        with open(USER_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    print("Username already exists! Try a different one or login again.")
                    return 
    except FileNotFoundError:
        pass

    # Create and save the user account
    user = User(username, email, password)
    user.save_account()

# User login
def login():
    attempts = 3

    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        try:
            with open(USER_FILE, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and username == row[0] and password == row[2]:
                        print("Login successful!\n")
                        return True
            attempts -= 1
            print(f"Invalid username or password. {attempts} attempts remaining.")
        except FileNotFoundError:
            print("No accounts found. Please create an account first.")
            return False

    print("Login failed.")
    return False

# Load dataset
df = pd.read_csv(MOVIE_FILE)

# Search functions
def search_by_title():
    title = input("Enter movie title: ").strip().lower()
    result = df[df["Title"].str.lower() == title.lower()]

    if not result.empty:
        for _, row in result.iterrows():
            print("\n")
            print(f"Title: {row['Title']}")
            print(f"Genre: {row['Genre']}")
            print(f"Year: {row['Year']}")
            print(f"Director: {row['Director']}")
            print(f"Actors: {row['Actors']}")
    else:
        print("No movie found with that title.")

def search_by_actor():
    actor = input("Enter actor's name: ").strip().lower()
    result = df[df["Actors"].str.lower().str.contains(actor, na=False)]

    if not result.empty:
        print("\n")
        print("\n" + result[["Title", "Actors"]].to_string(index=False))
    else:
        print("No movies found for that actor.")

def search_by_year():
    year = input("Enter year: ").strip()
    result = df[df["Year"].astype(str) == year]

    if not result.empty:
        print("\n" +result[["Title", "Year"]].to_string(index=False))
    else:
        print("No movies found for that year.")


def search_by_director():
    director = input("Enter director's name: ").strip().lower()
    result = df[df["Director"].str.lower().str.contains(director, na=False)]

    if not result.empty:
        print("\n" +result[["Title", "Director"]].to_string(index=False))
    else:
        print("No movies found for that director.")


# Display top 10 most popular movies (Pie Chart)
def display_top_popular_movies():
    top_popular = df.nlargest(10, "Popularity")

    plt.figure(figsize=(8, 8))
    plt.pie(top_popular["Popularity"], labels=top_popular["Title"], autopct="%1.1f%%", startangle=110)
    plt.title("Top 10 Movies by Popularity:")
    plt.show()

# Display top 10 highest-rated movies

def display_top_rated_movies():
    top_rated = df.nlargest(10, "Rating")

    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_rated["Title"], top_rated["Rating"], color="skyblue")

    for bar, Rating in zip(bars, top_rated["Rating"]):
        plt.text(bar.get_x() + bar.get_width() / 2,  
                 bar.get_height() + 0.1,              
                 f"{Rating:.1f}",                     
                 ha='center', va='bottom', fontsize=10)

    plt.ylabel("Rating")
    plt.xlabel("Movies")
    plt.title("Top 10 Movies by Rating")
    plt.xticks(rotation=25, ha="right") 
    plt.show()


def rate_movie():
    global df
    Title = input("\nEnter the title of the movie you want to rate: ").strip().lower()

    # Find the row where the title matches
    mask = df["Title"].str.lower() == Title
    if not mask.any():
        print("Movie not found.")
        return
    try:
        new_rating = float(input("\nEnter your rating (1 - 10): "))
        if not (1 <= new_rating <= 10):
            print("Invalid rating. Please enter a value between 1 to 10.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric value between 1 and 10.")
        return

    # Update rating (average of old and new rating)
    df.loc[mask, "Rating"] = (df.loc[mask, "Rating"] + new_rating) / 2

    # Increase popularity by 1 instead of 5
    df.loc[mask, "Popularity"] += 1  

    print(f"You have successfully rated '{Title}' with {new_rating} stars!")
    print("Popularity has also increased by 1!")

    # Save the updated dataset
    try:
        df.to_csv(MOVIE_FILE, index=False)
        print("Rating and popularity updated successfully!")
    except PermissionError:
        print("Error: Could not save the file. Make sure it is not open in another program.")




# Main menu
def main():
    while True:
        print("\n" + "*" * 100)
        print("\n1. Search by Title\n2. Search by Actor\n3. Search by Year\n4. Search by Director\n5. Exit")
        print("\n" + "*" * 100)
        option = input("Choose an option: ")
        if option == "1":
            search_by_title()
        elif option == "2":
            search_by_actor()
        elif option == "3":
            search_by_year()
        elif option == "4":
            search_by_director()
        elif option == "5":
            print("Exiting search...")
            break 
        else:
            print("Invalid option. Try again.")

while True:
    print("\n" + "=" * 100)
    print(" " * 35 + "Welcome to the IMDb Movie System!")
    print("=" * 100)
    print("\n1. Create Account")
    print("2. Login")
    print("3. Exit")
    print("\n" + "=" * 100)
    choice = input("Choose an option: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        if login():
            while True:
                print("\n" + "*" * 100)
                print(" " * 38 + "IMDb Movie Search System")
                print("*" * 100)
                print("\n1. Search Information of Movies")
                print("2. View Top 10 Popular Movies")
                print("3. View Top 10 Highest-Rated Movies")
                print("4. Rate a Movie")
                print("5. Logout")
                print("\n" + "*" * 100)
                opt = input("Select your option (1-5): ")

                if opt == "1":
                    print("\n" + "=" * 100)
                    print(" " * 40 + "Movie Search Options")
                    print("=" * 100)
                    main()
                elif opt == "2":
                    print("\n" + "=" * 100)
                    print(" " * 35 + "Displays Top 10 Popular Movies!")
                    print("=" * 100)
                    display_top_popular_movies()
                elif opt == "3":
                    print("\n" + "=" * 100)
                    print(" " * 32 + "Displays Top 10 Highest-Rated Movies!")
                    print("=" * 100)
                    display_top_rated_movies()
                elif opt == "4":
                    print("\n" + "=" * 100)
                    print(" " * 45 + "Rate a Movie")
                    print("=" * 100)
                    rate_movie()
                elif opt == "5":
                    print("\n" + "=" * 100)
                    print(" " * 40 + "Exiting... Goodbye!")
                    print("=" * 100)
                    break
                else:
                    print("Invalid choice. Try again.")
            break

    elif choice == "3":
        print("\n" + "=" * 100)
        print(" " * 40 + "Exiting... Program!")
        print("=" * 100)
        break

if __name__ == "main":
    main()