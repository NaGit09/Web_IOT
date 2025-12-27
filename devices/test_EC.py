#!/usr/bin/env python3
import mraa
import time
from flask import Flask, jsonify
from datetime import datetime

PIN_INDEX = 3
V_REF = 5.0
K_VALUE = 0.007633

app = Flask(__name__)

# Khởi tạo ADC
ai = mraa.Aio(PIN_INDEX)
ai.setBit(10)

latest_data = {}

@app.route('/api/ec')
def get_ec():
    return jsonify(latest_data)


def read_ec_loop():
    global latest_data
    while True:
        raw_val = ai.read()
        voltage = (raw_val / 1023.0) * V_REF

        if voltage <= 0.05:
            ec_mS = 0
        else:
            ec_mS = (133.42 * (voltage**3)
                     - 255.86 * (voltage**2)
                     + 857.39 * voltage) * K_VALUE

        ec_uS = ec_mS * 1000

        latest_data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "raw": raw_val,
            "voltage": round(voltage, 3),
            "ec": round(ec_uS, 0)
        }

        time.sleep(1)


if __name__ == '__main__':
    import threading
    t = threading.Thread(target=read_ec_loop, daemon=True)
    t.start()

    app.run(host='0.0.0.0', port=5000)
