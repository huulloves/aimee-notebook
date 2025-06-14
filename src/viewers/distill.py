"""aimee distill functionality with SQLite database integration"""
import tkinter as tk
import sqlite3 as sql3

def connect_to_db():
    try:
        conn = sql3.connect('aimee-content.db')
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
    
def create_buttons(parent):
    distill_btn = tk.Button(parent, text="distill", command=distill_event)
    clear_btn = tk.Button(parent, text="clear", command=clear_canvas)

    return distill_btn, clear_btn

def distill_event():
    conn, cursor = connect_to_db()
    if conn and cursor:
        try:
            user_data = cursor.execute("SELECT content FROM notes")
            conn.commit()
            print("notes retrieved from database...")
            for row in user_data:
                """print to console and display in gui"""
                print(f"note content: {row[0]}")
                user_data = row[0]

                # Display the content in the GUI
                display = tk.Entry(canvas, width=50)
                display.insert(0, user_data)
        
        except sql3.Error as e:
            print(f"error retrieving from database: {e}")
        finally:
            conn.close()

def clear_canvas():
    """Clear the canvas for new content"""
    canvas.delete("all")

def main():
    global user_data, canvas

    root = tk.Tk()

    root.title("aimee")
    root.geometry("800x600")

    canvas_width = 600
    canvas_height = 500

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    distill_btn = tk.Button(text="distill", command=distill_event)
    clear_btn = tk.Button(text="clear", command=clear_canvas)
    distill_btn.pack(padx=5, pady=5)
    clear_btn.pack(padx=5, pady=5)

    root.mainloop()
main()