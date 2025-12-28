from ..database.execute import HandleDB


class API:
    def __init__(self):
        self.database = HandleDB()

    def get_latest_luuluong_1_2_and_total(self):
        return self.database.get_latest_luuluong_1_2_and_total()

    def get_latest_apxuat(self):
        return self.database.get_latest_apxuat()

    def get_latest_ec(self):
        return self.database.get_latest_ec()

    def get_latest_ph(self):
        return self.database.get_latest_ph()

    def get_history_data(self, start_time=None, end_time=None):
        return self.database.get_history_data(start_time, end_time)

    def login(self, username, password):
        return self.database.check_login(username, password)

    def get_data_luu_luong(self, luongluong_id):
        return self.database.get_data_luu_luong(luongluong_id)

    def get_data_apxuat(self):
        return self.database.get_data_apxuat()

    def get_data_ec(self):
        return self.database.get_data_ec()

    def get_data_ph(self):
        return self.database.get_data_ph()

    def get_relay_state(self):
        return self.database.get_all_relay_state_db()

    def get_relay_state_db(self, relay_id=None):
        if relay_id:
            return self.database.get_relay_state_db(relay_id)
        return self.database.get_all_relay_state_db()

    def update_relay_state_db(self, relay_id, state):
        return self.database.update_relay_state_db(relay_id, state)

    def update_relay_mode_db(self, relay_id, mode):
        return self.database.update_relay_mode_db(relay_id, mode)
