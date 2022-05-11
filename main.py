import sys
import datetime
from utilities import *
from operator import attrgetter

def hogwarts_library(file_string):
    for command in file_string.split('\n'):
        command = command.strip(' ')
        start_let = command[:2].lower()
        if command.startswith('**'):
            pass
        elif start_let.startswith('nb'):
            New_Book(command)
        elif start_let.startswith('li'):
            List_Inventory()
        elif start_let.startswith('db'):
            Delete_Book(command)
        elif start_let.startswith('fb'):
            Find_Book(command)
        elif start_let.startswith('as'):
            Add_Student(command)
        elif start_let.startswith('lm'):
            List_Members()
        elif start_let.startswith('pl'):
            Print_Line(command)
        elif start_let.startswith('sd'):
            Start_Date(command)
        elif start_let.startswith('cb'):
            Checkout_Book(command)
        elif start_let.startswith('cr'):
            Checkout_Report()
        elif start_let.startswith('la'):
            List_Available()
        elif start_let.startswith('dt'):
            Due_Today()
        elif start_let.startswith('ad'):
            Advance_Date()
        elif start_let.startswith('rh'):
            Request_Hold(command)
        elif start_let.startswith('hr'):
            Hold_Report()
        elif start_let.startswith('rb'):
            Return_Book(command)
        elif start_let.startswith('or'):
            Overdue_Report()
        elif start_let.startswith('ur'):
            User_Report(command)
        elif start_let.startswith('dr'):
            Date_Return(command)


def lst_line(lin):
    line = lin[:]
    lst = line.split(',')
    fkyu = lst[0].split(' ')
    lst[0] = ' '.join(fkyu[1:])
    for i,val in enumerate(lst):
        eq = val.find('=')
        lst[i] = val[(eq + 1):].strip()
    return lst


def strip_search(lin):
    line = lin[:]
    lst = line.split(',')
    fkyu = lst[0].split(' ')
    lst[0] = ' '.join(fkyu[1:])
    for i, val in enumerate(lst):
        val = val.strip()
        lst[i] = val.split('=')
    return lst


def search(dic, lin):
    temp = strip_search(lin)
    new = []
    che = 0
    for fir in dic:
        che = 1
        d_string = str(dic[fir])
        peri = '.'
        if eval(d_string + peri + temp[0][0]) == temp[0][1]:
            new.append(dic[fir])
    if che == 1:
        for sub in range(1, len(temp), 1):
            for ject in new:
                j_str = str(ject)
                if eval(j_str + peri + temp[sub][0]) == temp[sub][1]:
                    pass
                else:
                    new.remove(ject)
    return new


def print_book(book):
    print(f"""Title: {book.title}
Author: {book.author}
Date: {book.year_published}
Subject: {book.subject}
Section: {book.section}
------------------------------------""")


def New_Book(lin):
    line = lst_line(lin)
    title = line[0]
    author = line[1]
    dat = line[2]
    sub = line[3]
    sec = line[4]
    nb = Book(title, author, dat, sub, sec)
    if book_collection.get(nb.title, 'NA') != 'NA':
        print(nb.title, 'already present.')
    else:
        book_collection[nb.title] = nb


def List_Inventory(tit=1):
    if tit == 1:
        print('*********************LIBRARY INVENTORY**********************')
    tits = sorted(book_collection.keys())
    print(f'Number of books available:{len(book_collection):>3}')
    print('------------------------------------')
    for i in tits:
        print_book(book_collection[i])


def Delete_Book(line):
    l = lst_line(line)
    if l[0] in book_collection:
        book_collection.pop(l[0])
        if l[0] in checkouts:
            checkouts.pop(l[0])
        if l[0] in reservations:
            reservations.pop(l[0])
    else:
        print('{} Not Found. Cannot be deleted.'.format(l[0]))


def Find_Book(line):
    print('************************BOOK SEARCH*************************')
    if len(line.split('=')) == 1:
        print(f'Number of books found:{len(book_collection):>3}')
        print('------------------------------------')
        for i in book_collection.keys():
            print_book(book_collection[i])
    else:
        results = search(book_collection, line)
        if len(results) == 0:
            print('No Book Found.')
        else:
            print(f'Number of books found:{len(results):>3}')
            print('------------------------------------')
            for i in results:
                print_book(i)


def Add_Student(line):
    stud = lst_line(line)
    if library_members.get(stud[0], 'NA') == 'NA':
        library_members[stud[0]] = Student(stud[0], stud[1], 0)
    else:
        print(f"{stud[0]} is already present.")


def lm(house):
    print(f'{house:>10}:')
    members = []
    for i in library_members:
        if library_members[i].house == house:
            members.append(i)
    if len(members) == 0:
        print('         No Registered Members')
    members.sort()
    for i in members:
        print(f'{i:>30}')


def List_Members():
    print('**********************LIBRARY MEMBERS***********************')
    lm('Gryffindor')
    lm('Hufflepuff')
    lm('Ravenclaw')
    lm('Slytherin')


def clean_lin(line):
    sp = line.split(' ')
    del sp[0]
    s = ' '.join(sp)
    s.strip()
    return s


def Print_Line(line):
    sp = line.split(' ')
    del sp[0]
    s = ' '.join(sp)
    s.strip()
    print(s)


def Start_Date(line):
    print('*************HOGWARTS LIBRARY MANAGEMENT SYSTEM*************')
    lin = clean_lin(line)
    pars = lin.split('/')
    for i in range(len(pars)):
        pars[i] = int(pars[i].strip())
    global start_date
    start_date = datetime.datetime(pars[2], pars[0], pars[1])
    v = start_date.strftime('%A %d, %B %Y')
    print('{head_char:{base_char}^60}'.format(head_char=v, base_char='*'))


def Checkout_Book(line, sig = 0):
    opt = strip_search(line)
    if len(opt) >= 3 and opt[2][0] == 'number_of_days':
        ad = Checkout(opt[0][1], opt[1][1], start_date + datetime.timedelta(days=int(opt[2][1])))
    elif len(opt) >= 4 and opt[3][0] == 'number_of_days':
        ad = Checkout(opt[0][1], opt[1][1], start_date + datetime.timedelta(days=int(opt[3][1])))
    else:
        ad = Checkout(opt[0][1], opt[1][1], start_date + datetime.timedelta(days=14))

    if opt[0][1] in book_collection and book_collection[opt[0][1]].section == 'Non-Restricted' and opt[1][1] in library_members and opt[0][1] not in checkouts:
        checkouts[opt[0][1]] = ad
    elif opt[1][1] not in library_members:
        print("{} is not a registered library member.".format(opt[1][1]))
    elif opt[0][1] not in book_collection:
        print('{} not in inventory.'.format(opt[0][1]))
    elif opt[0][1] in checkouts:
        print('{} is currently unavailable to be checked out.'.format(opt[0][1]))
    else:
        for i in opt:
            if i[0] == 'pass_code':
                if book_collection[opt[0][1]].section == 'Restricted' and i[1] in library_passcodes:
                    checkouts[opt[0][1]] = ad
                    return None
                else:
                    print('{} is not a valid pass code.'.format(i[1]))
                    return None
        if sig == 1:
            checkouts[opt[0][1]] = ad
        else:
            print('{} is a Restricted book, and requires a pass code to be checked out.'.format(opt[0][1]))


def Checkout_Report():
    print('***CURRENT CHECKOUT REPORT**************{}**********'.format(start_date.strftime('%m / %d / %Y')))
    if len(checkouts) == 0:
        print('                   No Books Checked Out.                    ')
    print('Book Title                        Student Name      Due Date')
    print('------------------------------------------------------------')
    alpha = {
        'Gryffindor':[],
        'Hufflepuff':[],
        'Ravenclaw':[],
        'Slytherin':[]
    }
    master = {}
    for v in checkouts.values():
        alpha[library_members[v.student].house].append(v)
    for i in alpha:
        alpha[i] = sorted(alpha[i], key=attrgetter('student'))
        for stud in alpha[i]:
            if stud.student in master:
                master[stud.student].append(stud)
            else:
                master[stud.student] = [stud]
    for i in master:
        master[i] = sorted(master[i], key=attrgetter('book'))
        for lst in master[i]:
            print("{:<30.30}{:^20}{:>10}".format(lst.book, lst.student, lst.due_date.strftime('%m / %d / %Y')))


def List_Available():
    aval = len(book_collection) - len(checkouts)
    print(f'Number of books in available: {aval}')
    print('------------------------------------')
    tits = sorted(book_collection.keys())
    for i in tits:
        if i not in checkouts:
            print_book(book_collection[i])


def Due_Today():
    print('*******BOOKS DUE TODAY******************{}**********'.format(start_date.strftime('%m / %d / %Y')))
    dt = []
    for i in checkouts:
        if checkouts[i].due_date == start_date:
            dt.append(checkouts[i])
    if len(dt) == 0:
        print('{:^60}'.format('No books due today.'))
    else:
        sor = sorted(dt, key=attrgetter('book'))
        for i in sor:
            print('{:<35.35}{:>25}'.format(i.book, i.student))


def Advance_Date():
    print('*************HOGWARTS LIBRARY MANAGEMENT SYSTEM*************')
    global start_date
    start_date = start_date + datetime.timedelta(days=1)
    v = start_date.strftime('%A %d, %B %Y')
    print('{head_char:{base_char}^60}'.format(head_char=v, base_char='*'))
    for i in checkouts:
        if checkouts[i][2] < start_date:
            if checkouts[i][1] in penalty:
                da = start_date - checkouts[i][2]
                if int(da.days) > 5:
                    da = 5
                    penalty[checkouts[i][1]] = penalties[da]
                    return None
                penalty[checkouts[i][1]] = penalties[int(da.days)]
            else:
                penalty[checkouts[i][1]] = penalties[1]


def Request_Hold(line):
    raw = lst_line(line)
    if len(raw) == 3:
        raw[2] = int(raw[2])
    else:
        raw.append(14)

    if raw[0] in checkouts and checkouts[raw[0]].student == raw[1]:
        print('{} currently has checked out {}.'.format(checkouts[raw[0]].student, raw[0]))
        return None
    if raw[0] in reservations:
        for i in reservations[raw[0]]:
            if i[1] == raw[1]:
                print('{} has already requested a hold for {}.'.format(raw[1], raw[0]))
                return None

    if raw[0] not in checkouts and raw[0] in book_collection and raw[1] in library_members:
        print('{} is available to be checked out. Use command to checkout book.'.format(raw[0]))
    elif raw[0] not in book_collection:
        print('{} not in inventory.'.format(raw[0]))
    elif raw[1] not in library_members:
        print('{} is not a registered library member.'.format(raw[1]))
    else:
        if raw[0] in reservations:
            reservations[raw[0]].append(raw)
        else:
            reservations[raw[0]] = [raw]


def Hold_Report():
    print('*****HOLD REQUEST REPORT****************{}**********'.format(start_date.strftime('%m / %d / %Y')))
    print('Student Name                         # of Days Requested    ')
    print('------------------------------------------------------------')
    if len(reservations) == 0:
        print('                    No Holds Requested.                     ')
    else:
        for i in reservations:
            print(i)
            for t in reservations[i]:
                print("   {:<30}{:^27}".format(t[1], t[2]))
            print('------------------------------------------------------------')


def Return_Book(line):
    throw = lst_line(line)
    tit = throw[0]
    if tit not in book_collection:
        print('{} not in inventory.'.format(tit))
        return None

    if tit not in checkouts:
        print('Invalid Return Request for {}.'.format(tit))
        return None
    stu = checkouts[tit].student
    if stu in penalty and checkouts[tit].due_date < start_date:
        penalty.pop(stu)
    checkouts.pop(tit)



    if tit in reservations:
        Checkout_Book('CB title={},student_name={},number_of_days={}'.format(reservations[tit][0][0], reservations[tit][0][1], reservations[tit][0][2]), 1)
        if len(reservations[tit]) == 1:
            del reservations[tit]
        else:
            del reservations[tit][0]


def Overdue_Report():
    print('********OVERDUE REPORT*************{}*******# Days**'.format(start_date.strftime('%m / %d / %Y')))
    over = True
    suck = []
    for i in checkouts:
        if checkouts[i][2] < start_date:
            over = False
            da = start_date - checkouts[i][2]
            suck.append('{:<34.34}{:^15.15}{:^10}'.format(checkouts[i].book, checkouts[i].student, da.days))
    if len(suck) > 0:
        su = sorted(suck)
        for i in su:
            print(i)
    if over:
        print('                  No books overdue today.                   ')


def User_Report(line):
    stu = lst_line(line)
    stud = stu[0]
    if stud not in library_members:
        print('{} is not a registered member of the library.'.format(stud))
        return None
    stri = 'USER REPORT for ' + stud
    print(f'{stri:*^60}')
    if stud in penalty:
        print('{} Curse: {}'.format(stud, penalty[stud][0]))

    print('-------------------------CHECKOUTS--------------------------')
    check = []
    for i in checkouts:
        if checkouts[i].student == stud:
            check.append(checkouts[i])
    if len(check) == 0:
        print('                       No checkouts.                        ')
    else:
        ch = sorted(check)
        for i in ch:
            print('{:<40}{:>20}'.format(i.book, i.due_date.strftime('%m / %d / %Y')))

    print('---------------------------HOLDS----------------------------')
    check = []
    for i in reservations:
        for t in reservations[i]:
            if t[1] == stud:
                check.append(t)
    if len(check) == 0:
        print('                       No holds.                        ')
    else:
        ch = sorted(check)
        for i in ch:
            print('{:<40}{:>20}'.format(i[0], i[2]))


def Date_Return(line):
    dat = lst_line(line)
    sd_ed = []
    for t in dat:
        pars = t.split('/')
        for i in range(len(pars)):
            pars[i] = int(pars[i].strip())
        sd_ed.append(datetime.datetime(pars[2], pars[0], pars[1]))
    print('***BOOKS DUE BETWEEN********{} to {}********'.format(sd_ed[0].strftime('%m / %d / %Y'), sd_ed[1].strftime('%m / %d / %Y')))
    sor = sorted(checkouts.keys())
    trig = True
    for i in sor:
        if sd_ed[0] <= checkouts[i].due_date <= sd_ed[1]:
            trig = False
            print('{:<40}{:>20}'.format(checkouts[i].book, checkouts[i].student))
    if trig:
        print('{:^60}'.format('No books due for the given dates.'))
    print('')


if __name__ == '__main__':
    penalty = {}
    with open(sys.argv[1]) as f:
        hogwarts_library(f.read())
