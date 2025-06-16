"""aimee speak functionality with SQLite database integration"""
import tkinter as tk
import sqlite3 as sql3
import sys
sys.path.append('../src/modules_base')  # Adjust path as necessary

""" import relative path to canvas config from canvas_config module located in /src/modules_base/canvas_config.py """
from src.modules_base.canvas_config import create_canvas
create_canvas()

def connect_to_db():
    try:
        conn = sql3.connect('aimee-sample-content.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                          (noteID INTEGER PRIMARY KEY, content TEXT)''')
        conn.commit()
        return conn, cursor
    except sql3.Error as e:
        print(f"database error: {e}")
        return None, None
    except Exception as e:
        print(f"unexpected error: {e}")
        return None, None
    
def speak_event():
    user_input = text_entry.get()
    print(f"user input: {user_input}")

    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (user_input,))
            conn.commit()
            print("content added to database")
        except sql3.Error as e:
            print(f"error inserting content: {e}")
        finally:
            conn.close()

def main():
    global text_entry

    root = tk.Tk()
    root.title("aimee")
    root.geometry("800x600")

    canvas = create_canvas(root, width=800, height=600, bg='white')

    text_entry = tk.Entry(root, width=40)
    canvas.create_window(300, 470, window=text_entry)  # Adjust position as needed
    text_entry.insert(0, "enter your notes here...")

    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    speak_btn = tk.Button(frame, text="speak", command=speak_event)
    speak_btn.pack(padx=10, pady=10)

    root.mainloop()
main()