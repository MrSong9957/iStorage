import sqlite3
import os

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
print('DB:', DB)
conn = sqlite3.connect(DB)
c = conn.cursor()

def table_exists(name):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (name,))
    return c.fetchone() is not None

for tbl in ['items_storagecell', 'items_furniture', 'items_item_storage_cells', 'items_item']:
    print(tbl, 'exists?', table_exists(tbl))

if table_exists('items_storagecell') and table_exists('items_furniture'):
    c.execute('SELECT s.id, s.furniture_id FROM items_storagecell s LEFT JOIN items_furniture f ON s.furniture_id=f.id WHERE f.id IS NULL;')
    rows = c.fetchall()
    print('Orphan storagecells referencing missing furniture:', len(rows))
    for r in rows[:20]:
        print(r)

if table_exists('items_item_storage_cells') and table_exists('items_storagecell') and table_exists('items_item'):
    c.execute('SELECT isc.id, isc.storagecell_id, isc.item_id FROM items_item_storage_cells isc LEFT JOIN items_storagecell s ON isc.storagecell_id=s.id WHERE s.id IS NULL;')
    rows2 = c.fetchall()
    print('Orphan item-storage links:', len(rows2))
    for r in rows2[:20]:
        print(r)

conn.close()

conn = sqlite3.connect(DB)
cc = conn.cursor()
cc.execute('PRAGMA foreign_key_check;')
violations = cc.fetchall()
print('PRAGMA foreign_key_check violations:', len(violations))
for v in violations[:50]:
    print(v)
conn.close()
