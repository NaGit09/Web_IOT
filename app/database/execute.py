import sqlite3
import os


class HandleDB:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.abspath("app/database/main.db"))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        print("Connected to database")

    def get_all_relay_state_db(self):
        query = """
            SELECT * FROM relay_states
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_relay_state_db(self, relay_id):
        query = """
            SELECT state, mode
            FROM relay_states
            WHERE relay_id = ?
        """
        self.cursor.execute(query, (relay_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else {"state": "off", "mode": "manual"}

    def update_relay_state_db(self, relay_id, state):
        query = """
            UPDATE relay_states
            SET state = ?
            WHERE relay_id = ?
        """
        self.cursor.execute(query, (state, relay_id))
        self.conn.commit()

    def update_relay_mode_db(self, relay_id, mode):
        query = """
            UPDATE relay_states
            SET mode = ?
            WHERE relay_id = ?
        """
        self.cursor.execute(query, (mode, relay_id))
        self.conn.commit()

    def get_data_luu_luong(self, luuluong_id):
        query = """
            SELECT *
            FROM LuuLuong
            WHERE LuuLuongID = ?
            ORDER BY ThoiGian DESC
        """
        self.cursor.execute(query, (luuluong_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_data_apxuat(self):
        query = """
            SELECT *
            FROM ApXuat
            ORDER BY ThoiGian DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_data_ec(self):
        query = """
            SELECT *
            FROM EC
            ORDER BY ThoiGian DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_data_ph(self):
        query = """
            SELECT *
            FROM PH
            ORDER BY ThoiGian DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_latest_luuluong_1_2_and_total(self):
        query = """
            SELECT LuuLuongID, TongLuuLuong
            FROM LuuLuong
            WHERE LuuLuongID IN (1, 2)
            ORDER BY ThoiGian DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        luuluong_1 = None
        luuluong_2 = None

        for row in rows:
            if row["LuuLuongID"] == 1 and luuluong_1 is None:
                luuluong_1 = dict(row)
            elif row["LuuLuongID"] == 2 and luuluong_2 is None:
                luuluong_2 = dict(row)

            if luuluong_1 and luuluong_2:
                break

        tong = sum(float(x["TongLuuLuong"]) for x in (luuluong_1, luuluong_2) if x)

        return {
            "luu_luong_1": luuluong_1,
            "luu_luong_2": luuluong_2,
            "tong_luu_luong": tong,
        }

    def get_latest_apxuat(self):
        query = """
            SELECT ApXuat
            FROM ApXuat
            ORDER BY ThoiGian DESC
            LIMIT 1
        """
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row["ApXuat"] if row else None

    def get_latest_ec(self):
        query = """
            SELECT EC
            FROM EC
            ORDER BY ThoiGian DESC
            LIMIT 1
        """
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row["EC"] if row else None

    def get_latest_ph(self):
        query = """
            SELECT PH
            FROM PH
            ORDER BY ThoiGian DESC
            LIMIT 1
        """
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row["PH"] if row else None

    def get_history_data(self, start_time=None, end_time=None, limit=20):
        # Base query helper
        def get_query(table, value_col, time_col="ThoiGian", where_clause=""):
            base = f"SELECT {value_col} as value, {time_col} as time FROM {table}"
            if start_time and end_time:
                extra_condition = f"AND {where_clause}" if where_clause else ""
                return f"{base} WHERE {time_col} BETWEEN ? AND ? {extra_condition} ORDER BY {time_col} ASC"
            return f"{base} {('WHERE ' + where_clause) if where_clause else ''} ORDER BY {time_col} DESC LIMIT ?"

        params = (start_time, end_time) if start_time and end_time else (limit,)

        # Fetch Flow 1
        self.cursor.execute(
            get_query("LuuLuong", "TongLuuLuong", where_clause="LuuLuongID=1"), params
        )
        flow1 = [dict(row) for row in self.cursor.fetchall()]

        # Fetch Flow 2
        self.cursor.execute(
            get_query("LuuLuong", "TongLuuLuong", where_clause="LuuLuongID=2"), params
        )
        flow2 = [dict(row) for row in self.cursor.fetchall()]

        # Fetch Pressure
        self.cursor.execute(get_query("ApXuat", "ApXuat"), params)
        pressure = [dict(row) for row in self.cursor.fetchall()]

        # Fetch EC
        self.cursor.execute(get_query("EC", "EC"), params)
        ec = [dict(row) for row in self.cursor.fetchall()]

        # Fetch pH
        self.cursor.execute(get_query("PH", "PH"), params)
        ph = [dict(row) for row in self.cursor.fetchall()]

        # If data was fetched with DESC + LIMIT, reverse it for charts
        if not (start_time and end_time):
            flow1 = flow1[::-1]
            flow2 = flow2[::-1]
            pressure = pressure[::-1]
            ec = ec[::-1]
            ph = ph[::-1]

        return {
            "flow1": flow1,
            "flow2": flow2,
            "pressure": pressure,
            "ec": ec,
            "ph": ph,
        }

    def check_login(self, username, password):
        if username == "admin" and password == "admin123":
            return True
        return False
