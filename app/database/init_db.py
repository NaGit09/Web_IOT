import sqlite3

conn = sqlite3.connect("main.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS LuuLuong (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        LuuLuongID INTEGER NOT NULL,
        SoXung INTEGER NOT NULL,
        LP DECIMAL NOT NULL,
        LS DECIMAL NOT NULL,
        TongLuuLuong DECIMAL NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ApXuat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ApXuat DECIMAL NOT NULL,
        TrangThai TEXT NOT NULL,
        DienAp DECIMAL NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS EC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Raw INTEGER NOT NULL,
        Voltage DECIMAL NOT NULL,
        EC DECIMAL NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS PH (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Raw INTEGER NOT NULL,
        Voltage DECIMAL NOT NULL,
        PH DECIMAL NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS INVTG20 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        TanSo INTEGER NOT NULL,
        DongDien DECIMAL NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()
