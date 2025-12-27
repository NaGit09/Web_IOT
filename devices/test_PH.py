import mraa
import time
import sys

# --- CẤU HÌNH ---
ANALOG_PIN = 4      # Sử dụng chân A0
V_REF = 5.0             # Điện áp tham chiếu (IOT2050 Arduino header là 5V)
ADC_RES = 1024.0        # Độ phân giải ADC (thường là 10-bit: 0-1023)

# --- HIỆU CHUẨN (CALIBRATION) ---
# Bạn cần chỉnh 2 số này dựa trên thực tế đo dung dịch đệm
# Offset: Chỉnh sao cho khi đo dung dịch pH 7.0 thì ra đúng 7.0
OFFSET = 0.00           
# Hệ số chuyển đổi từ Volt sang pH (thường khoảng 3.5 với cảm biến này)
# Nếu đo pH 4.0 mà ra giá trị sai, hãy chỉnh số này.
PH_STEP = 3.5           

def main():
    try:
        # Khởi tạo pin Analog A0
        # MRAA mapping: A0 trên board thường map index 0
        ph_sensor = mraa.Aio(ANALOG_PIN)
    except ValueError:
        print("Lỗi: Không thể khởi tạo chân Analog A0.")
        print("Hãy kiểm tra 'iot2050setup' để chắc chắn chân A0 đã được bật.")
        sys.exit(1)

    print("--- Bắt đầu đo pH trên IOT2050 ---")
    print("Nhấn Ctrl+C để dừng.")

    while True:
        try:
            # 1. Đọc giá trị Raw từ ADC (0 - 1023)
            # Đọc nhiều lần để lọc nhiễu (Lấy trung bình 10 mẫu)
            raw_sum = 0
            for _ in range(10):
                raw_sum += ph_sensor.read()
                time.sleep(0.02) # Nghỉ 20ms giữa các lần đọc
            
            raw_avg = raw_sum / 10.0

            # 2. Chuyển đổi sang Điện áp (Voltage)
            voltage = raw_avg * (V_REF / ADC_RES)

            # 3. Chuyển đổi sang giá trị pH
            # Công thức tuyến tính: pH = 7.0 + (Voltage - V_trung_tinh) / Slope
            # Hoặc công thức đơn giản cho module này:
            ph_value = 7.0 + ((voltage- 2.5) / 0.18)
            # Giải thích: 
            # - Tại pH 7, module thường xuất ra 2.5V (cần chỉnh biến trở trên mạch)
            # - Độ nhạy module thường là 0.18V cho mỗi đơn vị pH thay đổi
            
            # --- CÁCH TÍNH ĐƠN GIẢN HƠN (Dùng Offset) ---
            # ph_value = PH_STEP * voltage + OFFSET
            
            print(f"Raw: {raw_avg:.1f} | Volt: {voltage:.2f}V | pH: {ph_value:.2f}")

            time.sleep(1.0) # Đọc mỗi giây 1 lần

        except KeyboardInterrupt:
            print("\nĐã dừng chương trình.")
            break
        except Exception as e:
            print(f"Lỗi khi đọc: {e}")

if __name__ == "__main__":
    main()