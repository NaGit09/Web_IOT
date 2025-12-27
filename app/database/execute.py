import sqlite3

class HandleDB:
    def __init__(self):
        self.conn = sqlite3.connect("data_sensor_all.db")
        self.cursor = self.conn.cursor()

    def get_relay_states_db(self):
        self.cursor.execute("SELECT relay_id, state FROM relay_states")
        rows = self.cursor.fetchall()
        self.conn.close()
        return {str(r[0]): r[1] for r in rows}

    def update_relay_state_db(self, relay_id, state):
        self.cursor.execute(
            "UPDATE relay_states SET state=? WHERE relay_id=?", (state, relay_id)
        )
        self.conn.commit()
        self.conn.close()
