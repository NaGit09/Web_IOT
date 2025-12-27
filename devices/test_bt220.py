import minimalmodbus
import serial
import time

# --- CẤU HÌNH KẾT NỐI ---
# Nếu chạy trên Windows, đổi thành 'COM3', 'COM4' v.v...
# Nếu chạy trên IOT2050/Linux, thường là '/dev/ttyUSB0'
PORT_NAME = '/dev/ttyUSB1'  # <--- HÃY SỬA LẠI CỔNG NÀY CHO ĐÚNG

SLAVE_ID = 1        # Trùng với cài đặt P14.00 trên biến tần

# Khởi tạo kết nối
try:
    invt = minimalmodbus.Instrument(PORT_NAME, SLAVE_ID)
    invt.serial.baudrate = 9600        # Trùng với P14.01 = 3
    invt.serial.bytesize = 8
    invt.serial.parity   = serial.PARITY_EVEN # Trùng với P14.02 = 1 (Even)
    invt.serial.stopbits = 1
    invt.serial.timeout  = 1           # Thời gian chờ phản hồi (giây)
    invt.mode = minimalmodbus.MODE_RTU
    
    # Xóa bộ đệm để tránh lỗi dữ liệu cũ
    invt.clear_buffers_before_each_transaction = True
    
    print(f"-> Đã kết nối với cổng {PORT_NAME}")

except Exception as e:
    print(f"Lỗi kết nối cổng Serial: {e}")
    exit()

# --- CÁC ĐỊA CHỈ MODBUS (INVT GD20) ---
# Địa chỉ Hex chuyển sang Decimal để dùng trong thư viện
ADDR_CONTROL_CMD = 0x2000  # 8192 (Dec) - Lệnh chạy/dừng
ADDR_SET_FREQ    = 0x2001  # 8193 (Dec) - Đặt tần số
ADDR_READ_FREQ   = 0x3000  # 12288 (Dec) - Đọc tần số đang chạy
ADDR_READ_CURRENT= 0x3004  # 12292 (Dec) - Đọc dòng điện ra

# --- HÀM HỖ TRỢ ---
def write_freq(freq_hz):
    """Đặt tần số (Ví dụ 50.00Hz -> gửi 5000)"""
    val = int(freq_hz * 100) 
    # functioncode=6 (Write Single Register)
    invt.write_register(ADDR_SET_FREQ, val, functioncode=6)
    print(f"-> Đã đặt tần số: {freq_hz} Hz")

def run_forward():
    """Chạy thuận"""
    invt.write_register(ADDR_CONTROL_CMD, 1, functioncode=6)
    print("-> Lệnh: CHẠY THUẬN (Forward)")

def stop_invt():
    """Dừng biến tần"""
    invt.write_register(ADDR_CONTROL_CMD, 5, functioncode=6)
    print("-> Lệnh: DỪNG (Stop)")

def read_status():
    """Đọc thông số vận hành"""
    try:
        # Đọc tần số thực tế (chia 100)
        freq = invt.read_register(ADDR_READ_FREQ, 2) # số thập phân = 2
        # Đọc dòng điện (chia 10 vì biến tần trả về Ampe x 10)
        current = invt.read_register(ADDR_READ_CURRENT, 1) 
        print(f"   [MONITOR] Tần số thực: {freq} Hz | Dòng điện: {current} A")
    except IOError:
        print("   [ERROR] Không đọc được dữ liệu!")

# --- CHƯƠNG TRÌNH CHÍNH (DEMO) ---
if __name__ == "__main__":
    try:
        print("--- BẮT ĐẦU TEST BIẾN TẦN INVT GD20 ---")
        
        # 1. Đặt tần số 30Hz
        write_freq(30.0)
        time.sleep(1)

        # 2. Phát lệnh chạy
        run_forward()
        
        # 3. Vòng lặp đọc thông số trong 10 giây
        for i in range(10):
            time.sleep(1)
            read_status()
            
            # Tăng tốc độ lên 50Hz ở giây thứ 5
            if i == 5:
                print("\n-> Tăng tốc lên 50Hz...")
                write_freq(50.0)

        # 4. Dừng biến tần
        stop_invt()
        print("--- KẾT THÚC TEST ---")

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình điều khiển: {e}")
        # Cố gắng gửi lệnh dừng an toàn nếu lỗi
        try:
            stop_invt()
        except:
            pass