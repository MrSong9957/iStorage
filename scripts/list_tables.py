import sqlite3, os
DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
for row in c.fetchall():
    print(row[0])
print('\n---- Schemas ----')
for tbl in ['items_storage', 'items_storagecell', 'items_furniture', 'items_item_storages', 'items_item_storage_cells']:
    c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (tbl,))
    r = c.fetchone()
    print('\nTable:', tbl)
    print(r[0] if r else 'NOT FOUND')
conn.close()
