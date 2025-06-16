"""aimee speak functionality + viewer with SQLite database integration"""
import tkinter as tk
import sqlite3 as sql3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.llm.whisperer import WhispererLLM

def create_canvas(root, width=800, height=600, bg='white', **kwargs):
    """
    basic reusable canvas configuration.
    """
    canvas = tk.Canvas(root, width=width, height=height, bg=bg, **kwargs)
    canvas.pack()
    return canvas

def connect_to_db():
    try:
        conn = sql3.connect('aimee-content.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes
        (noteID INTEGER PRIMARY KEY, content TEXT)''')
        conn.commit()
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
    for word in user_input.lower().split():
        if word in topicArray:
            topic = word
            break
    print(f"[parser] detected topic: {topic if topic else 'none'}")
    return topic

def speak_event():
    user_input = text_entry.get()
    topic = parser_module(user_input)
    print(f"[speak] user input: {user_input}")

    # call the whisperer and print its output
    deeper_question = whisperer.ask_deeper_question(user_input)
    print(f"[whisperer] {deeper_question}")

    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (user_input,))
            conn.commit()
            print("[speak] content added to database")
        except sql3.Error as e:
            print(f"[speak] error inserting content: {e}")
        finally:
            conn.close()

def main():
    global text_entry, whisperer

    root = tk.Tk()
    root.title("aimee")
    root.geometry("800x600")

    canvas = create_canvas(root, width=800, height=600, bg='white')

    text_entry = tk.Entry(root, width=40)
    canvas.create_window(400, 570, window=text_entry)  # Centered at bottom
    text_entry.insert(0, "enter your notes here...")

    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    speak_btn = tk.Button(frame, text="speak", command=speak_event)
    speak_btn.pack(padx=10, pady=10)

    # initialize and load the LLM
    whisperer = WhispererLLM(model_path="/home/dev/prsnl-prgms/mistral-test/Magistral-Small-2506")
    whisperer.load_model()

    root.mainloop()

if __name__ == "__main__":
    main()