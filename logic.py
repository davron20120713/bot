import sqlite3

def update_project_status(project_id: int, status: str):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
    conn.commit()
    conn.close()
