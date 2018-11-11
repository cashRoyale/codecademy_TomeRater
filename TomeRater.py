#We need to keep track of our Users
class User(object):
    def __init__(self,name,email):
        #define self so we can call the initalized variables in other methods within the class
        self.name = name
        self.email = email
        #create an empty books class so we can keep a list of the books the user has read
        self.user_books = {}

    def get_email(self):
        #Show user e-mail
        return self.email

    def change_email(self, address):
        #Change e-mail adress and return print() that alerts user e-mail has been updated
        self.email = address
        print('E-Mail has been updated to: '+address)

    def __repr__(self):
        #Print User Creds when called
        return 'User: {name}, E-mail Address: {email}, Books read: {countBooks}'.format(name=self.name, email=self.email, countBooks=len(self.user_books))

    def __eq__(self, other_user):
        #if Other user creds = user creds return True
        if self.name == other_user['name'] and self.email == other_user['email']:
            return True
        return False
    #add two methods read_book, get_average_rating
    def read_book(self,book,rating=None):
        if rating == None:
            rating = 0
        self.user_books[book] = rating
    
    def num_books_read(self):
        return len(self.user_books)

    def get_value_of_collection(self):
        value_of_books = [value.get_price() for value in self.user_books.keys()]
        totalValue = 0
        for price in value_of_books:
            if price != None:
                try:
                    totalValue += price
                except:
                    continue
        return float('{0:.2f}'.format(totalValue))

    def get_average_rating(self):
        totalRatings = 0
        totalBooks = 0
        for rating in self.user_books.values():
            if rating != None:
                totalRatings += rating
                totalBooks += 1
        try:
            return totalRatings/totalBooks
        except:
            return 0
    '''
read_book = takes in book and optional var 'rating' (default to none) add key:value pair {book:rating}
get_average_rating = itereate through self.books (all of the books user has read) calculate and return the average rating
    '''


#create a class for Books (our User Objects will be reading books)
class Book(object):
    def __init__(self,title,isbn,price):
        #define self so we can call the initalized variables in other methods within the class
        self.title = title
        self.isbn = isbn
        #add in a ratings var which will start as an empty list
        self.ratings = []
        self.price = price

    def get_title(self):
        #return title of book
        return self.title

    def get_isbn(self):
        #return isbn of book
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self,new_isbn):
        #sets the books isbn and prints that the isbn has been updated
        self.isbn = new_isbn
        print('"{book}"\'s ISBN has been updated to: {new_isbn}'.format(book=self.title,new_isbn=new_isbn))

    def change_price(self,new_price):
        self.price = new_price
        print('"{book}"\'s price has been updated to {new_price}'.format(book=self.title,new_price=new_price))

    def add_rating(self,rating):
        #We need to add in an e-mail associated with a rating so books can not be over or under rated by one user multiple times!!!!
        if(rating != None):
            if rating >= 0 and rating <= 5:
                self.ratings.append(rating)
    def __eq__(self,other_book):
        #compare this book with other books, if they have the same isbn and name return true
        if self.get_title() == other_book.get_title() and self.get_isbn() == other_book.get_isbn():
            return True
        return False

    def __repr__(self):
        #return string of book (eg. {title}, a {level} manual on {subject})
        return 'There is no information on :"{title}"'.format(title=self.title)
    
    def __hash__(self):
        return hash((self.title,self.isbn))

    #add method get_average_rating
    def get_average_rating(self):
        totalRatings = 0
        for rating in self.ratings:
            totalRatings += rating
        try:
            return totalRatings/len(self.ratings)
        except:
            return 0
    '''
get_average_rating = itereate through self.ratings (all of the ratings of this book) calculate and return the average rating
in order to avoid "TypeError:	unhashable	type: 'list'" we must create a method __hash__ to make sure our object is hashable
    e.g. def  __hash__(self):
        	return	hash((self.title, self.isbn))

    '''
#make a fiction child class of Book with (title,author,isbn)
class Fiction(Book):
    def __init__(self,title,author,isbn,price):
        #absorb Parent __init__ info
        super().__init__(title,isbn,price)
        self.author = author
    def get_author(self):
        #return author name
        return self.author
    def __repr__(self):
        #return string of book (eg. {title} by {author})
        return '"{title}" by {author}.'.format(title=self.title,author=self.author)
#make a non-fiction child of Book with (title,subject,level,isbn)

class Non_Fiction(Book):
    def __init__(self,title,subject,level,isbn,price):
        #absorb Parent __init__ info
        super().__init__(title,isbn,price)
        #set instance variables
        self.subject = subject
        self.level = level
        '''
        subject	will be	a	string,	like	"Geology"
        level	will	be	a	string,	like	"advanced"
        '''    
    def get_subject(self):
        #return subject
        return self.subject
    def get_level(self):
        #return level
        return self.level
    def __repr__(self):
        #return string of book (eg. {title}, a {level} manual on {subject})
        return '"{title}", a {level} manual on {subject}'.format(title=self.title,level=self.level,subject=self.subject)

#We	have Users and Books, but how do they interact? Now it’s time to create the application to store those users.	
# It	is	time	to	create	TomeRater!
class TomeRater:
    def __init__(self):
        #need to create users and books
        #users = empty dictionary that will map a user to the corresponding user object
        #books = empty dictionary that will map a book to the number of users that have read it
        self.users = {}
        self.books = {}
    def launch_error_checker__(self,options,check_option_correct='N'):
        while check_option_correct != 'Y':
            print('What Task would you like to perform:')
            option = None
            number = 1
            for method in options:
                print('{number}. {method}'.format(number=number, method=method))
                number += 1
            while type(option) != int or (option < 1 or option > len(options)):
                print()
                option = input('Enter Number: ').strip()
                try:
                    option = int(option)
                except:
                    print('We\'re sorry, we don\'t recognise that as an integer.')
                if type(option) == int:
                    if option < 1 or option > len(options):
                        print('Sorry that is not a valid option. Please select an option within 1 and {maxNumber}'.format(maxNumber=len(options)))
            print('You\'ve selected {option}.'.format(option=options[option-1]))
            check_option_correct = input('Is that correct? (Y/N): ').strip().upper()
            print()
            if check_option_correct != 'Y':
                print('Let\'s try that again!')
                print()
        print('****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~****')
        print()
        return option-1


    def launch(self,option=1,startUp=False):
        #print(self.users)
        print('****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~****')
        print('Welcome to Tome Rater!')
        print()
        print('1. Login')
        print('2. Create an account')
        print()
        while startUp == False:
            start = input('Enter Number: ').strip()
            try:
                start = int(start)
            except:
                start = 0
            if start == 1 or start == 2:
                startUp = True
            else:
                print('Sorry we didn\'t understand that. Please enter 1 or 2.')
        if start == 1:
            email = self.login()
        else:
            email = self.create_account('2')
        if email == -1:
            option = -1
        methods_of_TomeRater = [
            'Add Book to Tome Rater Database',
            'Add Book to Account',
            'See your Book Database',
            'Value of your collection',
            'Change a Book Rating',
            'What\'s the Highest Rated Book',
            'Who\'s the Most Prolific User',
            'What\'s the Most Read Book',
            'See Catalogue',
            'Purchase Book',
            'Change E-Mail',
            'Log Off'
        ]
        while methods_of_TomeRater[option] != 'Exit':
            print()
            print(self.users[email])
            print()
            option = self.launch_error_checker__(methods_of_TomeRater)
            if option == 0:
                self.add_book_to_database(email)
            elif option == 1:
                self.select_book(email)
            elif option == 2:
                self.print_personal_database(email)
            elif option == 3:
                self.value_of_collection(email)
            elif option == 4:
                self.change_book_rating(email)
            elif option == 5:
                self.highest_rated_book(email)
            elif option == 6:
                self.most_prolific_user(email)
            elif option == 7:
                self.most_read_book(email)
            elif option == 8:
                self.print_catalog(email)
            elif option == 9:
                self.purchase_book(email)
            elif option == 10:
                email = self.change_email(email)
            elif option == len(methods_of_TomeRater)-1:
                self.exit()
        self.exit()

    #Allow user to order a book for pickup in store
    def purchase_book(self,email):
        print('Which Book would you like to purchase?')
        purchaseBook = self.select_book(email,True)
        if type(purchaseBook) != int:
            print(purchaseBook)
            print()
            print('We are reserving a copy of "{book}" for {name} at our Store.'.format(book=purchaseBook.get_title(),name=self.users[email].name))
            print('The total will be ${total}. Please come in to pick up your new book!'.format(total=float('{0:.2f}'.format(purchaseBook.get_price()+(purchaseBook.get_price()*.0815)))))
            return
        print('We are actively expanding our catalog. Please check back soon!')
        return

    #Allow user to see value of there collection
    def value_of_collection(self,email):
        value = self.users[email].get_value_of_collection()
        if value != 0:
            print('Your collection is valued at ${value}!'.format(value=value))
        else: 
            print('It appears that you don\'t have any books in your collection.')
            print('Try Adding a Book to your Account!')
        return

    #Allow the user to see the books they have read
    def print_personal_database(self,email):
        print('Your database:')
        number = 1
        bookList = [book for book in self.users[email].user_books]
        if len(bookList) > 0:
            for book in bookList:
                print('{number}. {book} ~ {ranking}* Ranking!'.format(number=number,book=book,ranking=self.users[email].user_books[book]))
                number += 1
            return bookList
        else:
            print('It appears that you don\'t have any books in your collection.')
            print('Try Adding a Book to your Account!')
        return []

    #Allow user to change the rating of a book they have read
    def change_book_rating(self,email,selectionPass=False,bookRating=False,):
        bookList = self.print_personal_database(email)
        if len(bookList) > 0:
            while selectionPass != True:
                print('which book do you wish to change? ')
                book_rating_to_change = input('Enter Number: ').strip()
                try:
                    book_rating_to_change = int(book_rating_to_change)
                except:
                    print('We\'re sorry, we don\'t recognise that entry.')
                    book_rating_to_change = -1
                if book_rating_to_change >= 0 and book_rating_to_change <= len(bookList):
                    selectionPass = True
                else:
                    print('We\'re sorry, that is not a valid selection.')
            while bookRating != True:
                print('What rating do you want to give to "{title}"?'.format(title=bookList[book_rating_to_change-1].get_title()))
                print('Please enter a value within 0 and 5.')
                new_rating = input('Rating from 0 to 5: ').strip()
                try:
                    new_rating = int(new_rating)
                except ValueError:
                    print('Invalid Rating')
                    new_rating = -1
                if new_rating >= 0 and new_rating <= 5:
                    bookRating = True
            bookList[book_rating_to_change-1].add_rating(new_rating)
            self.users[email].read_book(bookList[book_rating_to_change-1],new_rating)
        return

    #Allow the user to change there e-mail
    def change_email(self,email,validEmail=False):
        new_email = input('Enter new e-mail address: ').strip()
        while validEmail != True:
            if len(new_email) < 7:
                print('This is not a valid e-mail address.')
                new_email = input('Please enter your new e-mail address: ').strip()
                print()
            elif new_email[0] == '@' or new_email[-5] == '@':
                print('This is not a valid e-mail address.')
                new_email = input('Please enter your new e-mail address: ').strip()
                print()
            elif '@' not in new_email:
                print('We did not find \'@\' in your entry.')
                new_email = input('Please enter your new e-mail address: ').strip()
                print()
            elif new_email[-4:] != '.com' and new_email[-4:] != '.edu' and new_email[-4:] != '.org':
                print('Please make sure your e-mail ends in \'.com\', \'.org\', or\'.edu\'.')
                print()
                new_email = input('Please enter your new e-mail address: ').strip()
                print()
            else:
                validEmail = True
        
        self.users[email].change_email(new_email)
        self.users[new_email] = self.users.pop(email)
        return new_email

    def login(self,credentials=False):
        email = input('E-mail Address: ' ).strip()
        if email not in self.users:
            while credentials != True:
                print('Hmmmm... We can\'t find this e-mail.')
                print('Enter 1 to create an acount')
                print('Enter 2 to exit')
                print('Or try Logging on with your e-mail again')
                email = input('E-mail Address: ').strip()
                if email in self.users:
                    credentials = True
                elif email == '1':
                    create_account_question = input('Do you want to create an account? (Y/N): ').strip().upper()
                    if(create_account_question != 'Y'):
                        print('Auto Exit')
                        return -1
                    email = self.create_account(email)
                    credentials = True
                elif email == '2':
                    return -1
        return email

    def exit(self):
        print('Thanks for using Tome Rater!')
        print()
        print('****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~****')
        self.launch()
    #def create_book takes title and isbn and returns Book object(class)
    def create_book(self,title,isbn,price=None):
        new_book = Book(title,isbn,price)
        if new_book not in self.books:
            self.books[new_book.get_title()] = {'book': new_book, 'readers': 0}
            return new_book

    #def create_novel takes title,author, and isbn and returns Fiction object(class)
    def create_novel(self,title,author,isbn,price=None):
        new_fiction = Fiction(title,author,isbn,price)
        if new_fiction not in self.books:
            self.books[new_fiction.get_title()] = {'book': new_fiction, 'readers': 0}
            return new_fiction

    #def create_non_fiction takes title,subject, level, and isbn and returns Non_Fiction object(class)
    def create_non_fiction(self,title,subject,level,isbn,price=None):
        new_non_fiction = Non_Fiction(title,subject,level,isbn,price)
        if new_non_fiction not in self.books:
            self.books[new_non_fiction.get_title()] = {'book': new_non_fiction, 'readers': 0}
            return new_non_fiction

    #def add_book_to_user takes book,email optional rating(defualt none); get user in self.users with email as key
    def add_book_to_user(self,book,email,admin=False,rating=None,ratingPass=False):
        #if no user return "no user with email {email}"
        #if user call read_book with book and rating, call add_rating on book with rating
            #check if book is in TomeRaters self.books
                #if not add book to self.books with value of 1 (one user has read it)
                #else self.books += 1 (one more user has read it)
        if email not in self.users:
            print('No user with email: {email}'.format(email=email))
        else:
            if book.get_title() not in self.books:
                self.books[book.get_title()] = {'book': book, 'readers': 1}
            else:
                self.books[book.get_title()]['readers'] += 1
                #Does the User want to add a rating to the book?
            if rating == None and admin == False:
                rating_question = input('Would you like to add a rating for the book "{title}"? (Y/N):'.format(title=book.title)).strip().upper()
                if rating_question != 'Y':
                    print()
                else:
                    while ratingPass != True:
                    #takes in a rating adds it to ratings list (rating must be between 0 and 4 else return 'Invalid Rating')
                        rating = input('Rating from 0 to 5: ').strip()
                        print()
                        try:
                            rating = int(rating)
                        except ValueError:
                            print('Invalid Rating')
                            rating = -1
                        if rating >= 0 and rating <= 5:
                            ratingPass = True
                        else:
                            print('Please enter a value within 0 and 5.')
                    book.add_rating(rating)
            self.users[email].read_book(book,rating)
    def most_positive_user(self,email):
        user_tuple = [(self.users[email].get_average_rating(),self.users[email].name) for email in self.users]
        sorted_user_tuple = sorted(user_tuple,reverse=True)
        print('{name}, is our most positive user with an average rating of {rating}!'.format(name=sorted_user_tuple[0][1],rating=float('{0:.1f}'.format(sorted_user_tuple[0][0]))))
        return email

    def most_prolific_user(self,email):
        user_tuple = [(len(self.users[email].user_books),self.users[email].name) for email in self.users]
        sorted_user_tuple = sorted(user_tuple,reverse=True)
        if(sorted_user_tuple[0][0] == 1):
            bookMessage = '1 book.'
        else:
            bookMessage = '{value} books'.format(value=sorted_user_tuple[0][0])
        print('{name}, is our most prolific reader with {bookMessage} read.'.format(name=sorted_user_tuple[0][1],bookMessage=bookMessage))
        return email

    def most_read_book(self,email):
        sorted_books_list = sorted(self.books.items(),key=lambda x: x[1]['readers'],reverse=True)
        if(sorted_books_list[0][1]['readers'] == 1):
            bookMessage = '1 read'
        elif(sorted_books_list[0][1]['readers'] == 0):
            bookMessage = 'no reads'
        else:
            bookMessage = '{value} reads'.format(value=sorted_books_list[0][1]['readers'])
        print('"{book}", is our most read book with {numberMessage}.'.format(book=sorted_books_list[0][0],numberMessage=bookMessage))
        return email

    def highest_rated_book(self,email):
        sorted_books_list_rating = sorted(self.books.items(),key=lambda x: x[1]['book'].get_average_rating(),reverse=True)
        print('"{book}", is our highest rated book @ {percent}.'.format(book=sorted_books_list_rating[0][0],percent=float("{0:.1f}".format(sorted_books_list_rating[0][1]['book'].get_average_rating()))))
        return email
    
    #def add_user takes name and email and optional book_list (default empty list) creates new user
    def add_user_admin(self,name,email,user_books=None):
        self.users[email] = User(name,email)
        if user_books != None:
            self.users[email] = User(name,email)
            #if book_list provided loop through and add each book to user using 'add_book_to_user'
            if user_books != None and type(user_books) == list:
                '''
                if len(user_books) > 1:
                    booksMessage = str(len(user_books)) + ' books'
                else:
                    booksMessage = 'book'
                    print('Hi {user}! Let\'s add your {books} to your profile!'.format(user=self.users[email].name,books=booksMessage))
                '''
                for book in user_books:
                    self.add_book_to_user(book,email,True)

    def create_account(self,email=None,name=None,validEmail=False,validAccountEntry=False): 
        while validAccountEntry != True:
            if email == '1' or email == '2':
                print('Let\'s make an account: ')
                email = input('E-mail Address: ').strip()
            #Check to make sure it's a valid e-mail   
            while validEmail != True:
                if len(email) < 7:
                    print('This is not a valid e-mail address.')
                    email = input('Please enter your new e-mail address: ').strip()
                    print()
                elif email[0] == '@' or email[-5] == '@':
                    print('This is not a valid e-mail address.')
                    email = input('Please enter your new e-mail address: ').strip()
                    print()
                elif '@' not in email:
                    print('We did not find \'@\' in your entry.')
                    email = input('Please enter your new e-mail address: ').strip()
                    print()
                elif email[-4:] != '.com' and email[-4:] != '.edu' and email[-4:] != '.org':
                    print('Please make sure your e-mail ends in \'.com\', \'.org\', or\'.edu\'.')
                    print()
                    email = input('Please enter your new e-mail address: ').strip()
                    print()
                else:
                    validEmail = True
            if email not in self.users:
                if name == None:
                    f_name = input('First Name: ').strip()
                    l_name = input('Last Name: ').strip()
                    name = (f_name+' '+l_name).title()
                    print('Name: {name}, E-mail: {email}'.format(name=name, email=email))
                    correct_creds = input('Is the above correct: (Y/N): ').strip().upper()
                else:
                    print('Name: {name}, E-mail: {email}'.format(name=name, email=email))
                    correct_creds = input('Is the above correct: (Y/N): ').strip().upper()
                    print()
                if correct_creds != 'Y':
                    print('Let\'s try that again!')
                    email = '1'
                    name = None
                else:
                    validAccountEntry = True
        self.users[email] = User(name,email)
        return email
           
    def select_book(self,email,shopping=False,valid_new_book=False, newBookSelection=False):
        print('These are the books in our catalogue not registered to your account:')
        book_catalog = self.books
        book_selection = []
        number = 1
        for book in book_catalog.values():
            if book['book'] not in self.users[email].user_books:
                if shopping == True:
                    if book['book'].get_price() != None:
                        price = float('{0:.2f}'.format(book['book'].get_price()))
                    else:
                        price = 'Out of Stock!'
                    print('{number}. {book}: ${price}'.format(number=number, book=book['book'],price=price))
                else:
                    print('{number}. {book}'.format(number=number, book=book['book']))
                number += 1
                book_selection.append(book['book'])
        print()
        if len(book_selection) > 0:
            while valid_new_book != True:
                while newBookSelection != True:
                    print('Enter 0 to return to main menu.')
                    new_book_entry = input('Please enter the book number you wish to add: ').strip()
                    try:
                        new_book_entry = int(new_book_entry)
                    except:
                        new_book_entry = -1
                    if new_book_entry < 0 or new_book_entry > len(book_selection):
                        print('That is not an elligible selection.')
                    else:
                        newBookSelection = True
                    new_book = new_book_entry
                    if new_book == 0:
                        return 0
                if shopping == True:
                    book_question = input('Do you want to reserve {book} for pickup? (Y/N):'.format(book=book_selection[new_book-1])).upper()
                else:
                    book_question = input('Do you want to add {book} to your account? (Y/N):'.format(book=book_selection[new_book-1])).upper()
                if book_question != 'Y':
                    newBookSelection = False
                    print('Let\'s try that again.')
                else:
                    valid_new_book = True
            if shopping==True:
                return book_selection[new_book-1]
            #print(book_selection[new_book-1].get_title())
            book_to_add = book_selection[new_book-1]
            self.add_book_to_user(book_to_add,email)
        else:
            print('Looks like you have read every book in our catalog')
            if shopping==True:
                return None
            add_book_to_database_question = input('Do you want to add a new book to our database? (Y/N): ').strip().upper()
            if add_book_to_database_question != 'Y':
                return
            else:
                self.add_book_to_database(email)
        return email

    def add_book_to_database(self,email,correct_book_addition='N'):
        while correct_book_addition != 'Y':
            print('What Type of book is it?')
            print('1. Fiction')
            print('2. Non-Fiction')
            type_of_book = input('Type of book: ').strip()
            if type_of_book != '1' and type_of_book != '2':
                bookEntry = False
                while bookEntry != True:
                    print('Sorry we didn\'t understand that. Please enter 1 or 2.')
                    type_of_book = input('Enter Number: ').strip()
                    if type_of_book == '1' or type_of_book == '2':
                        bookEntry = True
            if type_of_book == '1':
                print('Let\'s create your Fiction entry:')
                book_name = input('What\'s the name of the book? ').strip()
                book_isbn = input('What\'s the ISBN of the book? ').strip()
                book_author = input('Who\'s the Author? ').strip()
                book_message = '"{title}", by {author} with an ISBN of {isbn}'.format(title=book_name,author=book_author,isbn=book_isbn)
            else:
                print('Let\'s create your Non-Fiction entry:')
                book_name = input('What\'s the name of the book? ').strip()
                book_isbn = input('What\'s the ISBN of the book? ').strip()
                book_subject = input('What\'s the subject ').strip()
                book_level = input('What\'s the level? (e.g. Beginner, Advanced, etc.)').strip()
                book_message = '"{title}", a {level} manual on {subject} with an ISBN of {isbn}'.format(title=book_name,level=book_level,subject=book_subject,isbn=book_isbn)
            print(book_message)
            correct_book_addition = input('Is the above correct? (Y/N): ').strip().upper()
            if correct_book_addition != 'Y':
                print('Let\'s try that again')
            else:
                if type_of_book == '1':
                    add_book_to_database = self.create_novel(book_name,book_author,book_isbn)
                else:
                    add_book_to_database = self.create_non_fiction(book_name,book_subject,book_level,book_isbn)
        self.add_book_to_user(add_book_to_database,email)
        return email

    def print_catalog(self,email):
    #iterate through self.books to print out the catalog of books stored in TomeRater. (Return list by Most Popular)
        number = 1
        sorted_books_list = sorted(self.books.items(),key=lambda x: x[1]['readers'],reverse=True)
        print('Catalogue of Books (Ordered by Most Read):')
        for book in sorted_books_list:
            if(book[1]['book'].get_price() == None):
                price = 'Out of Stock'
            else:
                price = '$'+str(float("{0:.2f}".format(book[1]['book'].get_price())))
            if(book[1]['readers'] != 0):
                print('{number}. {book} ~ {rating}* Rating! Price: {price}'.format(number=number,book=book[1]['book'],rating=float("{0:.1f}".format(book[1]['book'].get_average_rating())),price=price))
            else:
                print('{number}. {book} ~ {rating} Price: {price}'.format(number=number,book=book[1]['book'],rating='No Ratings!',price=price))
            number += 1
        return email
        #print(self.users)
    def print_users(self):
    #iterate through self.users to print out the catalog of users stored in TomeRater
        number = 1
        user_tuple = [(self.users[email].num_books_read(),self.users[email].name) for email in self.users]
        sorted_user_tuple = sorted(user_tuple,reverse=True)
        #print out members and the number of books read, order by number of books read
        print('List of Users (Ordered by most books read):')
        for user in sorted_user_tuple:
            print('{number}. {user} ~ {booksRead} books.'.format(number=number,user=user[1],booksRead=user[0]))
            number += 1

    #def most_read_books which iterates through books and returns the book with the most users
    #def highest_rated_books which returns the book with the highest average rating
    #def most_positive_user which returns the user with the highest average rating





