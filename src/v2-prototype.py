"""v2-prototype.py - A simple note-taking application using Tkinter and SQLite3.
This application allows users to enter notes, which are categorized by topics.
It includes functionality to save notes to a database and retrieve them for display."""

import tkinter as tk
import sqlite3 as sql3

def connect_to_db():
    try:
        conn = sql3.connect('aimee-prototype-content.db')
        cursor = conn.cursor()
        return conn, cursor
    except sql3.Error as e:
        print(f"[database] database error: {e}")
        return None, None
    except Exception as e:
        print(f"[database] unexpected error: {e}")
        return None, None

def parser_module(user_input):
    topicArray = ["family", "personal", "dreams", "school", "work", "emotions"]
    topic = ""
    theme = ""
    relation = ""
    topicID = None

    for word in user_input.lower().split():
        if word in topicArray:
            topic = word
            break

    conn, cursor = connect_to_db()
    print("[parser] module initializing...")
    if conn and cursor:
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                topicID INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE
            )''')
            if topic:
                print(f"[parser] detected topic: {topic}")
                try:
                    cursor.execute("INSERT INTO topics (topic) VALUES (?)", (topic,))
                    conn.commit()
                except sql3.IntegrityError:
                    # topic already exists, ignore
                    pass
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

def speak_event():
    user_input = text_entry.get()
    topicID, topic, theme, relation = parser_module(user_input)
    print(f"[speak] user input: {user_input}")
    print(f"[speak] topicID: {topicID}, topic: {topic}, theme: {theme}, relation: {relation}")

    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                noteID INTEGER PRIMARY KEY AUTOINCREMENT,
                topicID INTEGER,
                content TEXT,
                FOREIGN KEY (topicID) REFERENCES topics(topicID)
            )''')
            # add topicID column if not exists 
            try:
                cursor.execute("ALTER TABLE notes ADD COLUMN topicID INTEGER")
                print("[speak] altered notes table to add topicID")
            except sql3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("[speak] topicID column already exists, skipping alter.")
                else:
                    print(f"[speak] unexpected alter statement error: {e}")
            cursor.execute("INSERT INTO notes (topicID, content) VALUES (?, ?)", (topicID, user_input))
            conn.commit()
            print("[speak] content added to database")
        except sql3.Error as e:
            print(f"[speak] error inserting content: {e}")
        finally:
            conn.close()

def whisperer_module(user_input):
    # Placeholder for future functionality
    print(f"[whisperer] processing input: {user_input}")
    # This could be expanded to include more complex processing or analysis
    return user_input

def distill_event(canvas, canvas_width, canvas_height):
    global output_text_id
    conn, cursor = connect_to_db()
    output_text = "[distill] content will appear here..."
    if conn and cursor:
        try:
            user_data = cursor.execute("SELECT content FROM notes")
            notes = [row[0] for row in user_data]
            if notes:
                output_text = "\n".join(notes)
            print("[distill] notes retrieved from database...")
            print("[distill] note content:")
            for note in notes:
                print(note)
        except sql3.Error as e:
            print(f"[distill] error retrieving from database: {e}")
        finally:
            conn.close()
    # update only the output text on the canvas
    if output_text_id is not None:
        canvas.itemconfig(output_text_id, text=output_text)

def create_buttons(parent, canvas, canvas_width, canvas_height):
    speak_btn = tk.Button(parent, text="speak", command=speak_event)
    
    distill_btn = tk.Button(parent, text="distill", command=lambda: distill_event(canvas, canvas_width, canvas_height))

    return speak_btn, distill_btn

def main():
    global text_entry, output_text_id

    root = tk.Tk()
    root.title("aimee-v2")
    root.geometry("800x600")

    canvas_width = 600
    canvas_height = 500

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    # initial output text
    output_text = "[main] distilled content will appear here..."
    output_text_id = canvas.create_text(canvas_width // 2, canvas_height // 2, text=output_text, fill='black', font=('Arial', 12))

    text_entry = tk.Entry(root, width=40)
    canvas.create_window(canvas_width // 2, canvas_height - 30, window=text_entry)
    text_entry.insert(0, "enter notes here...")

    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    speak_btn, distill_btn = create_buttons(parent=frame, canvas=canvas, canvas_width=canvas_width, canvas_height=canvas_height)
    speak_btn.pack(padx=5, pady=5)
    distill_btn.pack(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()