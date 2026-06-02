# ダブルモーター制御
# (1)電源を入れる。
# (2)接続カードを読み込む。
# (3)ボタンを押して接続待機状態にする（ボタンが点滅）。
import tkinter as tk
from tkinter import messagebox
import legoeducation as le
import math

# 接続カードの情報を設定
card_color = le.LEGO_COLOR_RED  # 動作環境に合わせて修正
card_serial = '1309'            # 動作環境に合わせて修正

# DoubleMotor
doublemotor = le.DoubleMotor()
connected = False

# Connect 処理
def connect_motor():
    global connected

    try:
        # Connect ボタンを無効化
        connect_button.config(state=tk.DISABLED)
        
        status_label.config(text='Connecting...')
        root.update()

        doublemotor.connect(
            card_color=card_color,
            card_serial=card_serial
        )

        if doublemotor.connected:
            connected = True
            status_label.config(text='Connected')

            button_enable(1)     # ボタンを有効化

#            messagebox.showinfo('Success', 'ダブルモーターに接続しました。')
        else:
            connected = False
            status_label.config(text='Connection Failed')
            messagebox.showerror('Error', 'ダブルモーターに接続できませんでした。')

            # Connect ボタンを有効化
            connect_button.config(state=tk.NORMAL)

    except Exception as e:
        connected = False
        status_label.config(text='Error')
        messagebox.showerror('Error', str(e))

# 角度表示
def draw_angle(x1,y1,angle):
    r = 40  # 半径
    canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="white")
    rad = math.radians(angle-90)
    x2 = x1 + math.cos(rad) * r
    y2 = y1 + math.sin(rad) * r
    canvas.create_line(x1, y1, x2, y2, fill="magenta", width=4)

# ボタンの有効/無効化
def button_enable(enable):
    if enable != 0:
        read_button.config(state=tk.NORMAL)
        motor_l_button.config(state=tk.NORMAL)
        motor_r_button.config(state=tk.NORMAL)
    else:
        read_button.config(state=tk.DISABLED)
        motor_l_button.config(state=tk.DISABLED)
        motor_r_button.config(state=tk.DISABLED)
        
# 左モーター回転(マイナス方向に回転すると前進)
def move_motor_l():
    angle = -90
    button_enable(0)     # ボタンを無効化
    root.update()
    doublemotor.motor_run_for_degrees(angle, motor=le.MOTOR_LEFT, speed=20)
    button_enable(1)     # ボタンを有効化
    
# 右モーター回転
def move_motor_r():
    angle = 90
    button_enable(0)     # ボタンを無効化
    root.update()
    doublemotor.motor_run_for_degrees(angle, motor=le.MOTOR_RIGHT, speed=20)
    button_enable(1)     # ボタンを有効化

# IMU読み取り
def read_imu():
    button_enable(0)     # ボタンを無効化
    root.update()

    #orientation
    #yawFace
    #yaw
    #pitch
    #roll
    #accelerometerX
    #accelerometerY
    #accelerometerZ
    #gyroscopeX
    #gyroscopeY
    #gyroscopeZ

    yaw   = doublemotor.imu_device.yaw
    yaw   = int(yaw/10)
    pitch = doublemotor.imu_device.pitch
    pitch = int(pitch/10)
    roll  = doublemotor.imu_device.roll
    roll  = int(roll/10)

    imu_text.set(f'Yaw={yaw} : Pitch={pitch} : Roll={roll}')

    canvas.create_rectangle(0, 0, 300, 200, fill="white")
    draw_angle(50,100,-yaw)
    draw_angle(150,100,pitch)
    draw_angle(250,100,roll)

    button_enable(1)     # ボタンを有効化

# ウィンドウ終了時
def on_closing():
    try:
        if doublemotor.connected:
            doublemotor.disconnect()
    except:
        pass

    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title('DoubleMotor')
root.geometry('320x520')

# Connect ボタン
connect_button = tk.Button(
    root,
    text='Connect',
    width=20,
    height=2,
    command=connect_motor
)
connect_button.pack(pady=10)

# Read IMU ボタン
read_button = tk.Button(
    root,
    text='Read IMU',
    width=20,
    height=2,
    command=read_imu,
    state=tk.DISABLED # 初期状態では無効化
)
read_button.pack(pady=10)

# left Motor ボタン
motor_l_button = tk.Button(
    root,
    text='Left Motor',
    width=20,
    height=2,
    command=move_motor_l,
    state=tk.DISABLED # 初期状態では無効化
)
motor_l_button.pack()

# right Motor ボタン
motor_r_button = tk.Button(
    root,
    text='Right Motor',
    width=20,
    height=2,
    command=move_motor_r,
    state=tk.DISABLED # 初期状態では無効化
)
motor_r_button.pack()

# 状態表示
status_label = tk.Label(root, text='Not Connected')
status_label.pack(pady=5)

# パーセント表示
imu_text = tk.StringVar()
imu_text.set(' ')

imu_label = tk.Label(
    root,
    textvariable=imu_text,
    font=('Arial', 14)
)
imu_label.pack(pady=10)

# キャンバス
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack(pady=10)

# ウィンドウ終了処理
root.protocol('WM_DELETE_WINDOW', on_closing)

# 実行
root.mainloop()
