# コントローラー
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

# Controller
controller = le.Controller()
connected = False

# Connect 処理
def connect_sensor():
    global connected

    try:
        # Connect ボタンを無効化
        connect_button.config(state=tk.DISABLED)

        status_label.config(text='Connecting...')
        root.update()

        controller.connect(
            card_color=card_color,
            card_serial=card_serial
        )

        if controller.connected:
            connected = True
            status_label.config(text='Connected')

            # Read Sensor ボタンを有効化
            read_button.config(state=tk.NORMAL)

#            messagebox.showinfo('Success', 'コントローラーに接続しました。')
        else:
            connected = False
            status_label.config(text='Connection Failed')
            messagebox.showerror('Error', 'コントローラーに接続できませんでした。')

            # Connect ボタンを有効化
            connect_button.config(state=tk.NORMAL)

    except Exception as e:
        connected = False
        status_label.config(text='Error')
        messagebox.showerror('Error', str(e))


# コントローラー読み取り
def read_controller():
    if not connected:
        messagebox.showwarning('Warning', '先に Connect ボタンを押してください。')
        return

    try:
        # レバーの位置取得
        percent_l = controller.sensor.leftPercent
        percent_r = controller.sensor.rightPercent
        angle_l = int(controller.sensor.leftAngle /100)
        angle_r = int(controller.sensor.rightAngle /100)

        percent_text.set(f'L:{percent_l}({angle_l}) / R:{percent_r}({angle_r})')

        canvas.create_rectangle(0, 0, 300, 200, fill="white")

        r = 14  # 半径
        x1 = 50
        y1 = 100
        canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="blue")
        rad = math.radians(-percent_l * 45 / 100)
        x2 = x1 + math.cos(rad) * 50
        y2 = y1 + math.sin(rad) * 50
        canvas.create_line(x1, y1, x2, y2, fill="magenta", width=4)

        x1 = 200
        y1 = 100
        canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="blue")
        rad = math.radians(-percent_r * 45 / 100)
        x2 = x1 + math.cos(rad) * 50
        y2 = y1 + math.sin(rad) * 50
        canvas.create_line(x1, y1, x2, y2, fill="magenta", width=4)

    except Exception as e:
        messagebox.showerror('Error', str(e))

# ウィンドウ終了時
def on_closing():
    try:
        if controller.connected:
            controller.disconnect()
    except:
        pass

    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title('Controller Viewer')
root.geometry('320x420')

# Connect ボタン
connect_button = tk.Button(
    root,
    text='Connect',
    width=20,
    height=2,
    command=connect_sensor
)
connect_button.pack(pady=10)

# Read Controller ボタン
# 初期状態では無効化
read_button = tk.Button(
    root,
    text='Read Controller',
    width=20,
    height=2,
    command=read_controller,
    state=tk.DISABLED
)
read_button.pack(pady=10)

# 状態表示
status_label = tk.Label(root, text='Not Connected')
status_label.pack(pady=5)

# パーセント表示
percent_text = tk.StringVar()
percent_text.set('left:___ / right:___')

percent_label = tk.Label(
    root,
    textvariable=percent_text,
    font=('Arial', 14)
)
percent_label.pack(pady=10)

# キャンバス
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack(pady=10)

# ウィンドウ終了処理
root.protocol('WM_DELETE_WINDOW', on_closing)

# 実行
root.mainloop()
