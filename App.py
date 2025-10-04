import sqlite3

# Database create/connect
conn = sqlite3.connect("demo_app.db")
cursor = conn.cursor()

# Teacher table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Question table
cursor.execute("""
CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qustion TEXT,
    op1 TEXT,
    op2 TEXT,
    op3 TEXT,
    op4 TEXT,
    rop TEXT
)
""")

conn.commit()

# ---------------- TEACHER ----------------
def register_teacher():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO teacher (email,password) VALUES (?,?)", (email,password))
        conn.commit()
        print("Teacher registered successfully!")
    except:
        print("Email already exists!")

def login_teacher():
    email = input("Enter email: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM teacher WHERE email=? AND password=?", (email,password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        teacher_menu()
    else:
        print("Invalid credentials")

def teacher_menu():
    while True:
        print("\n--- Teacher Menu ---")
        print("1. Add Question\n2. Remove Question\n3. Update Question\n4. Display Questions\n0. Exit")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            q = input("Enter question: ")
            op1 = input("Option 1: ")
            op2 = input("Option 2: ")
            op3 = input("Option 3: ")
            op4 = input("Option 4: ")
            rop = input("Right option: ")

            cursor.execute("INSERT INTO question (qustion,op1,op2,op3,op4,rop) VALUES (?,?,?,?,?,?)",
                           (q,op1,op2,op3,op4,rop))
            conn.commit()
            print("Question added!")

        elif choice == 2:
            q = input("Enter question to remove: ")
            cursor.execute("DELETE FROM question WHERE qustion=?", (q,))
            conn.commit()
            print("Question removed!")

        elif choice == 3:
            old_q = input("Enter old question: ")
            cursor.execute("SELECT * FROM question WHERE qustion=?", (old_q,))
            if cursor.fetchone():
                new_q = input("New question: ")
                op1 = input("Option 1: ")
                op2 = input("Option 2: ")
                op3 = input("Option 3: ")
                op4 = input("Option 4: ")
                rop = input("Right option: ")

                cursor.execute("UPDATE question SET qustion=?, op1=?, op2=?, op3=?, op4=?, rop=? WHERE qustion=?",
                               (new_q,op1,op2,op3,op4,rop,old_q))
                conn.commit()
                print("Question updated!")
            else:
                print("Question not found!")

        elif choice == 4:
            cursor.execute("SELECT * FROM question")
            for row in cursor.fetchall():
                print(row)

        elif choice == 0:
            break
        else:
            print("Invalid choice")

# ---------------- STUDENT ----------------
def register_student():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO student (email,password) VALUES (?,?)", (email,password))
        conn.commit()
        print("Student registered successfully!")
    except:
        print("Email already exists!")

def login_student():
    email = input("Enter email: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM student WHERE email=? AND password=?", (email,password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        take_quiz()
    else:
        print("Invalid credentials")

def take_quiz():
    cursor.execute("SELECT * FROM question")
    questions = cursor.fetchall()
    total = 0
    for q in questions:
        print("\nQ:",q[1])
        print("1.",q[2])
        print("2.",q[3])
        print("3.",q[4])
        print("4.",q[5])
        ans = input("Enter correct answer: ")
        if ans == q[6]:
            total += 1
    print(f"Your score: {total}/{len(questions)}")

# ---------------- MAIN ----------------
while True:
    print("\n=== Main Menu ===")
    print("1. Teacher\n2. Student\n3. Exit")
    choice = int(input("Enter choice: "))

    if choice == 1:
        print("\n1. Register Teacher\n2. Login Teacher\n3. Back")
        t_choice = int(input("Enter choice: "))
        if t_choice == 1:
            register_teacher()
        elif t_choice == 2:
            login_teacher()
            

    elif choice == 2:
        print("\n1. Register Student\n2. Login Student\n3. Back")
        s_choice = int(input("Enter choice: "))
        if s_choice == 1:
            register_student()
        elif s_choice == 2:
            login_student()

    elif choice == 3:
        print("Bye!")
        break
    else:
        print("Invalid choice")
