# シングルモーター制御 (絶対的な角度制御)
# (1)電源を入れる。
# (2)接続カードを読み込む。
# (3)ボタンを押して接続待機状態にする（ボタンが点滅）。
import tkinter as tk
from tkinter import messagebox
import legoeducation as le
import math

# 接続カードの情報を設定
card_color = le.LEGO_COLOR_RED  # 動作環境に合わせて修正
card_serial = '2313'            # 動作環境に合わせて修正

# SingleMotor
singlemotor = le.SingleMotor()
connected = False

# Connect 処理
def connect_motor():
    global connected

    try:
        # Connect ボタンを無効化
        connect_button.config(state=tk.DISABLED)
        
        status_label.config(text='Connecting...')
        root.update()

        singlemotor.connect(
            card_color=card_color,
            card_serial=card_serial
        )

        if singlemotor.connected:
            connected = True
            status_label.config(text='Connected')
            button_enable(1)   # ボタンを有効化

            print('シングルモーターに接続しました。')
#            messagebox.showinfo('Success', 'シングルモーターに接続しました。')
        else:
            connected = False
            status_label.config(text='Connection Failed')
            messagebox.showerror('Error', 'シングルモーターに接続できませんでした。')

            # Connect ボタンを有効化
            connect_button.config(state=tk.NORMAL)

    except Exception as e:
        connected = False
        status_label.config(text='Error')
        messagebox.showerror('Error', str(e))

# ボタンの有効/無効化
def button_enable(enable):
    if enable != 0:
        motor_fow_button.config(state=tk.NORMAL)
        motor_zero_button.config(state=tk.NORMAL)
        motor_back_button.config(state=tk.NORMAL)
    else:
        motor_fow_button.config(state=tk.DISABLED)
        motor_zero_button.config(state=tk.DISABLED)
        motor_back_button.config(state=tk.DISABLED)

# モータ制御(引数angle 絶対的な角度)
def move_motor_sub(angle):
    button_enable(0)   # ボタンを無効化
    root.update()
    # 絶対的モーター制御
    singlemotor.motor_run_to_absolute_position(position=angle ,speed = 20)
    button_enable(1)   # ボタンを有効化

# モーター制御(絶対的な角度 +45度)
def move_motor_fow():
    move_motor_sub(45)

# モーター制御(絶対的な角度 0度)
def move_motor_zero():
    move_motor_sub(0)

# モーター制御(絶対的な角度 -45度)
def move_motor_back():
    move_motor_sub(-45)

# ウィンドウ終了時
def on_closing():
    try:
        if singlemotor.connected:
            singlemotor.disconnect()
    except:
        pass

    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title('SingleMotor(absolute position)')
root.geometry('320x320')

# Connect ボタン
connect_button = tk.Button(
    root,
    text='Connect',
    width=20,
    height=2,
    command=connect_motor
)
connect_button.pack(pady=10)

# モーター正転 ボタン
motor_fow_button = tk.Button(
    root,
    text='Plus 45deg.',
    width=20,
    height=2,
    command=move_motor_fow,
    state=tk.DISABLED # 初期状態では無効化
)
motor_fow_button.pack()

# モーター原点 ボタン
motor_zero_button = tk.Button(
    root,
    text='Zero deg.',
    width=20,
    height=2,
    command=move_motor_zero,
    state=tk.DISABLED # 初期状態では無効化
)
motor_zero_button.pack()

# モーター逆転 ボタン
motor_back_button = tk.Button(
    root,
    text='Minus 45deg.',
    width=20,
    height=2,
    command=move_motor_back,
    state=tk.DISABLED # 初期状態では無効化
)
motor_back_button.pack()

# 状態表示
status_label = tk.Label(root, text='Not Connected')
status_label.pack(pady=5)

# 表示
imu_text = tk.StringVar()
imu_text.set(' ')

imu_label = tk.Label(
    root,
    textvariable=imu_text,
    font=('Arial', 14)
)
imu_label.pack(pady=10)

# ウィンドウ終了処理
root.protocol('WM_DELETE_WINDOW', on_closing)

# 実行
root.mainloop()
