import mraa
import time
import sys
import os 

# ================= CẤU HÌNH =================
PIN_FLOW = 2            
K_FACTOR = 10.0         
UPDATE_INTERVAL = 1.0   
FILE_NAME = "du_lieu_luu_luong.csv"
# ============================================

pulse_count = 0

def interrupt_handler(args):
    global pulse_count
    pulse_count += 1

def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{int(s):02d}"

def main():
    global pulse_count

    # --- 1. KHỞI TẠO FILE ---
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a") as f:
        if not file_exists:
            f.write("ThoiGian;SoXung;LuuLuong_L_p;NuocTrong1s_L;TongNuoc_L\n")
            print(f"Đã tạo file mới: {FILE_NAME}")
        else:
            print(f"Đang ghi nối tiếp vào file: {FILE_NAME}")

    # --- 2. KHỞI TẠO PHẦN CỨNG ---
    try:
        flow = mraa.Gpio(PIN_FLOW)
        flow.dir(mraa.DIR_IN)
        flow.mode(mraa.MODE_PULLUP)
        # SỬA QUAN TRỌNG: Dùng isr_exit hay isrExit tùy phiên bản, 
        # nhưng ở đoạn khởi tạo này vẫn dùng isr bình thường.
        flow.isr(mraa.EDGE_FALLING, interrupt_handler, interrupt_handler)
    except ValueError:
        print(f"Lỗi phần cứng chân D{PIN_FLOW}")
        sys.exit(1)

    print("-" * 88)
    print(f"| {'TGIAN':^7} | {'XUNG':^8} | {'LƯU LƯỢNG':^12} | {'NƯỚC 1s':^15} | {'TỔNG':^12} |")
    print("-" * 88)

    total_volume = 0.0      
    last_time = time.time()
    start_time = time.time() 
    last_pulse_count = 0

    try:
        while True:
            time.sleep(UPDATE_INTERVAL)
            
            # --- TÍNH TOÁN ---
            current_time = time.time()
            current_pulses = pulse_count 
            
            dt = current_time - last_time
            delta_pulses = current_pulses - last_pulse_count
            
            hz = delta_pulses / dt
            flow_rate_lpm = hz / K_FACTOR
            volume_this_second = (flow_rate_lpm / 60.0) * dt
            total_volume += volume_this_second
            
            elapsed_str = format_time(current_time - start_time)

            # --- HIỂN THỊ MÀN HÌNH ---
            print(f"| {elapsed_str:^7} | {delta_pulses:^8} | {flow_rate_lpm:8.2f} L/p | {volume_this_second:11.4f} L | {total_volume:8.3f} L  |")

            # --- GHI VÀO FILE ---
            data_line = f"{elapsed_str};{delta_pulses};{flow_rate_lpm:.2f};{volume_this_second:.4f};{total_volume:.3f}\n"
            with open(FILE_NAME, "a") as f:
                f.write(data_line)

            last_time = current_time
            last_pulse_count = current_pulses

    except KeyboardInterrupt:
        # SỬA LỖI QUAN TRỌNG TẠI ĐÂY: Dùng isrExit (chữ E hoa) cho IOT2050
        try:
            flow.isrExit()
        except AttributeError:
            # Phòng hờ nếu thư viện mraa bản mới dùng isr_exit thường
            try:
                flow.isr_exit()
            except:
                pass
                
        print(f"\nĐã dừng. Dữ liệu đã được lưu vào file: {FILE_NAME}")

if __name__ == "__main__":
    main()

    #chân vàng(tín hiệu)nối vào D2, đỏ nối vào 5V, đen nối vào GND