from collections import namedtuple
import datetime


Book = namedtuple('Book', ['title', 'author', 'year_published', 'subject', 'section']) #title(str), author(str), year_published(int), subject(str), section(str)
Checkout = namedtuple('Checkout', ['book', 'student', 'due_date']) #book(Book), student(Student), due_date(datetime.date)
Student = namedtuple('Student', ['student_name', 'house', 'checked_out_books']) #student_name(str), house(str), checked_out_books(list=[])
Penalty = namedtuple('Penalty', ['curse', 'point_deduction']) #curse(str), point_deduction(int)


no_penalty = Penalty("None", 0)
one_day_penalty = Penalty("Ear-Shrivelling", 10)
two_day_penalty = Penalty("Hair Loss", 20)
three_day_penalty = Penalty("Curse of the Bogies", 30)
four_day_penalty = Penalty("Slug-Vomiting", 50)
five_day_penalty = Penalty("Book Return", 80)


# Define Container of the total outstanding point balance of every house
house_penalties = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}

# Define Library Data Structures
book_collection = {} #book_title:Book
library_members = {} #student_name:Student
checkouts = {} #book_title:Checkout
reservations = {} #book_title:[(student_name, start_date,end_date)]
penalties = [no_penalty, one_day_penalty, two_day_penalty, three_day_penalty, four_day_penalty, five_day_penalty] 
library_passcodes = ["Accio", "Protego"]
start_date = None

# Print Format Strings. NOTE: Most output uses width 60-characters.
due_today_format_string = "{title:<35}{name:>25}"
due_report_format_string = "{title:<35}{name:>25}"
checkout_report_format_string = "{title:<30}{name:^20}{due_date:>10}"
user_report_format_string = "{title:<35}{due_date:>25}"
hold_report_format_string = "{name:<33}{number_of_days:^27}"



# See below for example namedtuple instances
if __name__ == "__main__":
    
    # Define Container of the total outstanding point balance of every house
    house_balance = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}

    #Books
    curses = Book("Curses and Counter-Curses", "Vindictus Viridian", 1703, "Curses", "Restricted") 
        
    # Define Members
    harry_potter = Student("Harry Potter", "Gryffindor", [curses])
    
    # Define checkouts
    curse_checkout = Checkout(curses, harry_potter, datetime.date(year=1991, month=9, day=3))