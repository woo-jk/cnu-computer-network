from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()
conn = sqlite3.connect('answer.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Paste (
                 id INTEGER PRIMARY KEY,
                 content TEXT);''')
conn.commit()

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/paste/{paste_id}')
def get_paste(paste_id: int):
    res = cur.execute('''SELECT id, content
                         FROM Paste
                         WHERE id = ?''', (paste_id,))
    data = res.fetchone()
    if data is not None:
        paste = Paste(content=data[1])
        return {'paste_id': data[0],
                'paste': paste}
    else:
        return {'paste_id': paste_id,
                'paste': None}

    # if paste_id < len(db):
    #     return {'paste_id': paste_id,
    #             'paste': db[paste_id]}
    # else:
    #     return {'paste_id': paste_id,
    #             'paste': None}

class Paste(BaseModel):
    content: str

@app.post('/paste/')
def post_paste(paste: Paste):
    res = cur.execute('''SELECT id, content
                        FROM Paste
                        ORDER BY id DESC''')
    data = res.fetchone()
    if data is not None:
        paste_id = data[0] + 1
    else: 
        paste_id = 1
    cur.execute('''INSERT INTO Paste (id, content) VALUES (?, ?)''', (paste_id, paste.content,))
    conn.commit()
    return {'paste_id': paste_id,
                'paste': paste}
    # db.append(paste)
    # paste_id = len(db)-1
    # return {'paste_id': paste_id,
    #         'paste': db[paste_id]}

@app.put('/paste/{paste_id}')
def put_paste(paste_id: int, paste: Paste):
    res = cur.execute('''SELECT id, content
                         FROM Paste
                         WHERE id = ?''', (paste_id,))
    data = res.fetchone()
    if data is not None:
        cur.execute('''UPDATE Paste 
                    SET content = ? 
                    WHERE id = ?''', (paste.content, paste_id,))
        conn.commit()
        return {'paste_id': paste_id,
                'paste': paste}
    else:
        return {'paste_id': paste_id,
                'paste': None}
#     if paste_id < len(db):
#         db[paste_id] = paste
#         return {'paste_id': paste_id, 
#                 'paste': paste}
#     else:
#         return {'paste_id': paste_id,
#                 'paste': None}

@app.delete('/paste/{paste_id}')
def delete_paste(paste_id:int):
    res = cur.execute('''SELECT id, content
                         FROM Paste
                         WHERE id = ?''', (paste_id,))
    data = res.fetchone()
    if data is not None:
        cur.execute('''DELETE FROM Paste
                        WHERE id = ?''', ( paste_id,))
        conn.commit()
        paste = Paste(content=data[1])
        return {'paste_id': paste_id,
                'paste': paste}
    else:
        return {'paste_id': paste_id,
                'paste': None}
#     if paste_id < len(db):
#         db[paste_id] = None
#         return {'paste_id': paste_id,
#                 'paste': db[paste_id]}
#     else:
#         return {'paste_id': paste_id,
#                 'paste': None}

