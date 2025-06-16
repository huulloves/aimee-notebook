import tkinter as tk
import sqlite3 as sql3

def connect_to_db():
    try:
        conn = sql3.connect('aimee-content.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS notes")
        return conn, cursor
    except sql3.Error as e:
        print(f"[database] database error: {e}")
        return None, None
    except Exception as e:
        print(f"[database] unexpected error: {e}")
        return None, None
        
def create_buttons(parent):
    speak_btn = tk.Button(parent, text="speak", command=speak_event)
    distill_btn = tk.Button(parent, text="distill", command=distill_event)

    return speak_btn, distill_btn


""" """
def parser_module(input):
    topicArray = ["family", "personal", "dreams", "school", "work", "emotions"]
    topic = ""
    theme = ""
    relation = ""
    topicID = None

    for word in input.lower().split():
        if word in topicArray:
            topic = word
            break

    conn, cursor = connect_to_db()
    print("[parser] module initializing...")
    if conn and cursor:
        try:
            cursor = conn.cursor()

            print("[parser] module initialized...")

            cursor.execute('''CREATE TABLE IF NOT EXISTS topics (topicID INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT UNIQUE)''')
                
            if topic:
                print(f"[parser] detected topic: {topic}")
                cursor.execute("INSERT INTO topics (topic) VALUES (?)",(topic,))
                conn.commit()
                
                print("[parser] detecting topicID...")
                cursor.execute("SELECT topicID FROM topics WHERE topic = ?", (topic,))

                result = cursor.fetchone()
                if result:
                    topicID = result[0]

                    print(f"[parser] detected topicID: {topicID}")

        except sql3.Error as e:
            print(f"[parser] error inserting topic: {e}")
        finally:
            conn.close()
            return topicID, topic, theme, relation

    # Placeholder for parser module functionality

def speak_event():
    input = text_entry.get()

    print(type(input))

    topicID, topic, theme, relation = parser_module(input)

    print(f"[speak] user input: {input}")
    print(f"[speak] topicID: {topicID}, topic: {topic}, theme: {theme}, relation: {relation}")

    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("ALTER TABLE notes ADD COLUMN topicID INTEGER")
                print("[speak] altered notes table to add topicID")
            except sql3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("[speak] topicID column already exists, exiting alter table.")
                else:
                    print(f"[speak] unexpected alter statement error", {e})
                    raise

            try:
                cursor.execute('''CREATE TABLE IF NOT EXISTS notes ( noteID INTEGER PRIMARY KEY AUTOINCREMENT, topicID INTEGER, content TEXT, FOREIGN KEY (topicID) REFERENCES topics(topicID))''')
            
                cursor.execute("INSERT INTO notes (topicID, content) VALUES (?)", (topicID, input,))
                conn.commit()
                print("[speak] content added to database")
            except sql3.Error as e:
                print(f"[speak] error inserting content: {e}") 

        except sql3.Error as e:
            print(f"[speak] error creating table: {e}")
        except Exception as e:
            print(f"[speak] error getting cursor", {e})
        finally:
            conn.close()

""" """

""" """
def whisperer_module():
    print("[whisperer] module initialized...")
    # Placeholder for whisperer module functionality[whisperer]
    
def distill_event():
    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            user_data = cursor.execute("SELECT content FROM notes")
            conn.commit()
            print("[distill] notes retrieved from database...")
            print("[distill] note content:")
            for row in user_data:
                print(f"{row[0]}")
        except sql3.Error as e:
            print(f"[distill] error retrieving from database: {e}")
        finally:
            conn.close()
""""""


def main():
    global text_entry
    global input

    root = tk.Tk()

    root.title("aimee")
    root.geometry("800x600")

    canvas_width = 600
    canvas_height = 500

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    text_entry = tk.Entry(root, width=40)
    canvas.create_window(canvas_width // 2, canvas_height - 30, window=text_entry)
    text_entry.insert(0, "enter your notes here...")

    input = text_entry.get()
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    speak_btn, distill_btn = create_buttons(frame)
    speak_btn.pack(padx=5, pady=5)
    distill_btn.pack(padx=5, pady=5)

    root.mainloop()
main()
