from tkinter import *
import customtkinter
from PIL import Image
import serial
import serial.tools.list_ports
import threading
import time
from PIL import Image, ImageTk
from tkinter.messagebox import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("MoonlitSky.json")

# Global serial object
ser = None

def check_login(event=None):
    """Handles user login and validation."""
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "123456":
        login_window.destroy()
        show_main_window()
        send_command("ENABLE_SENSOR")  # Enable the IR sensor after successful login
    else:
        lbl_error.configure(text="Sai tên đăng nhập hoặc mật khẩu", font=("Arial", 14))

def show_main_window():
    """Creates the main application window with device controls."""

    def send_command(command):
        """Sends a command to the Arduino and handles errors."""
        global ser
        if ser:
            try:
                ser.write((command + "\n").encode('utf-8'))
                print(f"Sent command: {command}")
            except Exception as e:
                print(f"Error sending command: {e}")
                lb_error.configure(text=f"Lỗi gửi lệnh: {e}", text_color="red")
                lb_error.place(x=100, y=500)
        else:
            print("Not connected to serial port.")
            lb_error.configure(text="Chưa kết nối đến cổng COM", text_color="red")
            lb_error.place(x=100, y=500)

    def toggle_device(button, label, on_image, off_image, on_text, off_text, command_on, command_off):
        """Generic function to toggle a device on/off."""
        if button.is_on:
            button.configure(image=off_image, text=off_text)
            label.configure(text="Đã bật")
            send_command(command_on)
        else:
            button.configure(image=on_image, text=on_text)
            label.configure(text="Đã tắt")
            send_command(command_off)
        button.is_on = not button.is_on

    def connect_com_port():
        """Connects to the selected COM port."""
        global ser
        port = com_port.get()
        try:
            ser = serial.Serial(port, 9600, timeout=1)
            print(f"Kết nối thành công đến {port}")
            showinfo(title="THÔNG BÁO:", message="Đã kết nói thành công")
            threading.Thread(target=read_from_port, daemon=True).start()
        except Exception as e:
            print(f"Lỗi kết nối đến {port}: {e}")
            showwarning(title="CẢNH BÁO:", message="Đã kết nói thất bại !!!")

    def read_from_port():
        """Continuously reads data from the serial port."""
        global ser
        while True:
            if ser and ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                lb_status.configure(text=line)
                if line == "Có người đột nhập":
                    lb_status.configure(text_color="red")
                else:
                    lb_status.configure(text_color="green")

    root = customtkinter.CTk()
    root.title("Smart house control")
    root.geometry("500x700+300+0")

    frame_buttons = customtkinter.CTkFrame(master=root, width=170, height=350, corner_radius=10, fg_color="#000000", border_color="#A9A9A9", border_width=2)
    frame_buttons.place(x=50, y=280)

    frame_labels = customtkinter.CTkFrame(master=root, width=170, height=350, corner_radius=10, fg_color="#000000", border_color="#A9A9A9", border_width=2)
    frame_labels.place(x=250, y=280)

    # --- Load Images ---
    img_path = "C:\\downoad\\Smarthouse (1)\\"  # Update with your image path!
    img_light_on = customtkinter.CTkImage(Image.open(img_path + "light-on-icon.png"), size=(30, 30))
    img_light_off = customtkinter.CTkImage(Image.open(img_path + "light-off-icon.png"), size=(30, 30))
    img_fan_on = customtkinter.CTkImage(Image.open(img_path + "fan-on.png"), size=(30, 30))
    img_fan_off = customtkinter.CTkImage(Image.open(img_path + "fan-off.png"), size=(30, 30))
    img_door_open = customtkinter.CTkImage(Image.open(img_path + "open-door.png"), size=(30, 30))
    img_door_close = customtkinter.CTkImage(Image.open(img_path + "close-door.png"), size=(30, 30))
    # Add images for AC, TV, and Heater

    # --- Buttons ---
    lb_tb = customtkinter.CTkLabel(master=frame_buttons, text=" THIẾT BỊ ", font=("Arial", 20), text_color="#B0C4DE")
    lb_tb.grid(row=0, column=0, padx=10, pady=10)

    btn_light = customtkinter.CTkButton(master=frame_buttons, text="Bật đèn 1", corner_radius=50,
                                        border_color="#A9A9A9", border_width=2, image=img_light_on,
                                        command=lambda: toggle_device(btn_light, lb_light, img_light_on,
                                                                      img_light_off, "Bật đèn 1", "Tắt đèn 1",
                                                                      "L1ON", "L1OFF"))
    btn_light.grid(row=1, column=0, padx=10, pady=10)
    btn_light.is_on = False

    btn_light2 = customtkinter.CTkButton(master=frame_buttons, text="Bật đèn 2", corner_radius=50,
                                         border_color="#A9A9A9", border_width=2, image=img_light_on,
                                         command=lambda: toggle_device(btn_light2, lb_light2, img_light_on,
                                                                       img_light_off, "Bật đèn 2", "Tắt đèn 2",
                                                                       "L2ON", "L2OFF"))
    btn_light2.grid(row=2, column=0, padx=10, pady=10)
    btn_light2.is_on = False

    btn_light3 = customtkinter.CTkButton(master=frame_buttons, text="Bật đèn 3", corner_radius=50,
                                         border_color="#A9A9A9", border_width=2, image=img_light_on,
                                         command=lambda: toggle_device(btn_light3, lb_light3, img_light_on,
                                                                       img_light_off, "Bật đèn 3", "Tắt đèn 3",
                                                                       "L3ON", "L3OFF"))
    btn_light3.grid(row=3, column=0, padx=10, pady=10)
    btn_light3.is_on = False

    btn_fan = customtkinter.CTkButton(master=frame_buttons, text="Bật quạt", corner_radius=50,
                                      border_color="#A9A9A9", border_width=2, image=img_fan_on,
                                      command=lambda: toggle_device(btn_fan, lb_fan, img_fan_on,
                                                                    img_fan_off, "Bật quạt", "Tắt quạt",
                                                                    "FANON", "FANOFF"))
    btn_fan.grid(row=4, column=0, padx=10, pady=10)
    btn_fan.is_on = False

    btn_door = customtkinter.CTkButton(master=frame_buttons, text="Mở cửa", corner_radius=50,
                                       border_color="#A9A9A9", border_width=2, image=img_door_open,
                                       command=lambda: toggle_device(btn_door, lb_door, img_door_close,
                                                                     img_door_open, "Đóng cửa", "Mở cửa",
                                                                     "D1ON", "D1OFF"))
    btn_door.grid(row=5, column=0, padx=10, pady=10)
    btn_door.is_on = False

    # ... (Add buttons for AC, TV, and Heater similarly)

    # --- Labels ---
    lb_tt = customtkinter.CTkLabel(master=frame_labels, text="BẢNG TRẠNG THÁI", font=("Arial", 20), text_color="#B0C4DE")
    lb_tt.grid(row=0, column=1, padx=15, pady=15)

    lb_light = customtkinter.CTkLabel(master=frame_labels, text="Đang tắt", font=("Arial", 20), text_color="#B0C4DE")
    lb_light.grid(row=1, column=1, padx=15, pady=15)

    lb_light2 = customtkinter.CTkLabel(master=frame_labels, text="Đang tắt", font=("Arial", 20), text_color="#B0C4DE")
    lb_light2.grid(row=2, column=1, padx=15, pady=15)

    lb_light3 = customtkinter.CTkLabel(master=frame_labels, text="Đang tắt", font=("Arial", 20), text_color="#B0C4DE")
    lb_light3.grid(row=3, column=1, padx=15, pady=15)

    lb_fan = customtkinter.CTkLabel(master=frame_labels, text="Đang tắt", font=("Arial", 20), text_color="#B0C4DE")
    lb_fan.grid(row=4, column=1, padx=15, pady=15)

    lb_door = customtkinter.CTkLabel(master=frame_labels, text="Đang tắt", font=("Arial", 20), text_color="#B0C4DE")
    lb_door.grid(row=5, column=1, padx=15, pady=15)

    # ... (Add labels for AC, TV, and Heater similarly)

    lb_error = customtkinter.CTkLabel(master=frame_labels, text="", font=("Arial", 20), text_color="red")
    lb_error.grid(row=6, column=1, padx=15, pady=15)

    lb_status = customtkinter.CTkLabel(master=frame_labels, text="Trạng thái:", font=("Arial", 20), text_color="#B0C4DE")
    lb_status.grid(row=7, column=1, padx=15, pady=15)

    # --- COM Port Selection ---
    com_frame = customtkinter.CTkFrame(master=root, width=500, height=100, corner_radius=10, fg_color="#000000", border_color="#A9A9A9", border_width=2)
    com_frame.place(x=0, y=0)

    lb_com_port = customtkinter.CTkLabel(master=com_frame, text="Chọn cổng COM", font=("Arial", 20), text_color="#B0C4DE")
    lb_com_port.place(x=10, y=20)

    ports = list(serial.tools.list_ports.comports())
    port_list = [p.device for p in ports]

    com_port = customtkinter.CTkComboBox(master=com_frame, values=port_list)
    com_port.place(x=200, y=20)

    btn_connect = customtkinter.CTkButton(master=com_frame, text="Kết nối", command=connect_com_port)
    btn_connect.place(x=400, y=20)

    root.mainloop()

# Create the login window
login_window = customtkinter.CTk()
login_window.geometry("500x300")
login_window.title("Login")

lbl_username = customtkinter.CTkLabel(master=login_window, text="Tên đăng nhập:", font=("Arial", 14))
lbl_username.pack(pady=10)

entry_username = customtkinter.CTkEntry(master=login_window)
entry_username.pack(pady=10)

lbl_password = customtkinter.CTkLabel(master=login_window, text="Mật khẩu:", font=("Arial", 14))
lbl_password.pack(pady=10)

entry_password = customtkinter.CTkEntry(master=login_window, show="*")
entry_password.pack(pady=10)

btn_login = customtkinter.CTkButton(master=login_window, text="Đăng nhập", command=check_login)
btn_login.pack(pady=10)

lbl_error = customtkinter.CTkLabel(master=login_window, text="", font=("Arial", 14), text_color="red")
lbl_error.pack(pady=10)

entry_password.bind("<Return>", check_login)

login_window.mainloop()
