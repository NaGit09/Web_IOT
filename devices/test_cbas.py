import mraa
import time
import sys

# --- CẤU HÌNH ---
PIN_A1 = 1           # MRAA index cho A1 (thường là 1, tùy phiên bản OS có thể cần check lại map)
MAX_BAR = 10.0       # Áp suất tối đa của cảm biến (Bar)
R_SHUNT = 165.0      # Ohm (330 // 330)

try:
    # Khởi tạo pin A1
    ai = mraa.Aio(PIN_A1)
    
    # Set độ phân giải 10-bit (cho chắc chắn)
    ai.setBit(10) 
    
    print("Dang doc ap suat tu chan A1...")
    print("Nhan Ctrl+C de dung.")

    while True:
        # Đọc giá trị Raw (0 - 1023)
        raw_val = ai.read()
        
        # Đổi sang Điện áp (Hệ 5V)
        voltage = (raw_val / 1023.0) * 5.0
        
        # Các ngưỡng điện áp cho R = 165 Ohm
        v_zero = 0.66  # Tại 4mA
        v_span = 2.64  # Dải (3.3V - 0.66V)
        
        # Tính toán áp suất
        # Công thức tuyến tính: Y = (X - Min) / Span * Max_Scale
        pressure = ((voltage - v_zero) / v_span) * MAX_BAR
        
        # Xử lý biên (Chặn số âm và chặn quá áp)
        if pressure < 0:
            if voltage < 0.5:
                print(f"Canh bao: Dut day! (Volts: {voltage:.2f}V)")
                pressure = 0
            else:
                pressure = 0
                
        print(f"Raw: {raw_val} | Volts: {voltage:.2f}V | Ap suat: {pressure:.2f} Bar")
        
        time.sleep(1)

except ValueError as e:
    print(f"Loi MRAA: {e}")
except KeyboardInterrupt:
    print("\nDa dung chuong trinh.")