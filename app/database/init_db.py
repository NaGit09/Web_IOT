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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS USER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mssv TEXT NOT NULL,
        password TEXT NOT NULL,
        ThoiGian DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SCHEDULE (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        CheDo TEXT NOT NULL,
        Lich TEXT NOT NULL,
        Van TEXT NOT NULL
    )""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS relay_states (
    relay_id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    mode TEXT NOT NULL
)
 """)
# cursor.execute("""
#     INSERT INTO relay_states (relay_id, state, mode) VALUES
#     (1, 'OFF','Tự động'), (2, 'OFF','Tự động'), (3, 'OFF','Tự động'), (4, 'OFF','Tự động'), (5, 'OFF','Tự động'), (6, 'OFF','Tự động'), (7, 'OFF','Tự động'), (8, 'OFF','Tự động')
# """)
# cursor.execute("""
#     INSERT INTO SCHEDULE (CheDo, Lich, Van) VALUES ('Tự động', '16:00', '1'),
#     ('Tự động', '16:00', '2'),
#     ('Tự động', '16:00', '3'),
#     ('Tự động', '16:00', '4'),
#     ('Tự động', '16:00', '5'),
#     ('Tự động', '16:00', '6'),
#     ('Tự động', '16:00', '7'),
#     ('Tự động', '16:00', '8')
# """)    

# cursor.execute("""
#     INSERT INTO USER (mssv, password) VALUES ('22130015', '123456')
# """)

# cursor.execute("""
#     INSERT INTO LuuLuong (LuuLuongID, SoXung, LP, LS, TongLuuLuong) 
#     VALUES (1, 50, 4.99, 0.0831, 0.328),
#     (1, 28, 2.79, 0.0466, 0.375),
#     (1, 3, 0.3, 0.005, 0.38),
#     (1, 0, 0, 0, 0.38),
#     (1, 26, 2.59, 0.0432, 0.432),
#     (1, 89, 8.88, 0.148, 0.572),
#     (1, 83, 8.22, 0.138, 0.72),
#     (1, 181, 18.6, 0.301, 1.012),
#     (1, 151, 15.6, 0.2511, 1.263),
#     (1, 68, 6.78, 0.1131, 1.377),
#     (2, 24, 2.49, 0.0411, 0.29),
#     (2, 28, 2.29, 0.0411, 0.371),
#     (2, 4, 0.2, 0.005, 0.38),
#     (2, 0, 0, 0, 0.38),
#     (2, 26, 2.59, 0.0432, 0.452),
#     (2, 69, 8.6, 0.166, 0.522),
#     (2, 83, 8.22, 0.168, 0.72),
#     (2, 121, 12.6, 0.2511, 1.062),
#     (2, 101, 10.6, 0.2511, 1.263),
#     (2, 68, 6.78, 0.1531, 1.377)
# """)

# cursor.execute("""
#     INSERT INTO ApXuat (ApXuat, TrangThai, DienAp) 
#     VALUES 
#     (0, 'Bình thường', 0.98),
#     (0, 'Bình thường', 0.98),
#     (0, 'Bình thường', 0.99),
#     (0, 'Bình thường', 0.99),
#     (0.03, 'Bình thường', 1.01),
#     (0.03, 'Bình thường', 1.01),
#     (0.19, 'Bình thường', 1.08),
#     (0.19, 'Bình thường', 1.08),
#     (0.07, 'Bình thường', 1.03),
#     (0.07, 'Bình thường', 1.03),
#     (0.05, 'Bình thường', 1.02)
# """)

# cursor.execute("""
#     INSERT INTO EC (Raw, Voltage, EC) 
#     VALUES 
#     (56, 0.274, 1665.8),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9),
#     (48, 0.235, 1441),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9),
#     (55, 0.269, 1637.9)
# """)

# cursor.execute("""
#     INSERT INTO PH (Raw, Voltage, PH) 
#     VALUES 
#     (426.5, 2.083, 4.68),
#     (426.8, 2.084, 4.69),
#     (427, 2.085, 4.69),
#     (427, 2.085, 4.69),
#     (426.9, 2.084, 4.68),
#     (427, 2.085, 4.69),
#     (427, 2.085, 4.69),
#     (427, 2.085, 4.69),
#     (426.7, 2.083, 4.69),
#     (427, 2.085, 4.69),
#     (427, 2.085, 4.69)
# """)

# cursor.execute("""
#     INSERT INTO INVTG20 (TanSo, DongDien) 
#     VALUES 
#     (0, 0),
#     (18.3, 0),
#     (38.68, 0),
#     (50, 0),
#     (50, 0),
#     (50, 0),
#     (50,0),
#     (45,0),
#     (45,0),
#     (45,0)
# """)

cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table';
""")
print(cursor.fetchall())

conn.commit()
conn.close()




