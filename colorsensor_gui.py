# カラーセンサー
# (1)電源を入れる。
# (2)接続カードを読み込む。
# (3)ボタンを押して接続待機状態にする（ボタンが点滅）。
import tkinter as tk
from tkinter import messagebox
import legoeducation as le

# 接続カードの情報を設定
card_color = le.LEGO_COLOR_RED  # 動作環境に合わせて修正
card_serial = '1309'            # 動作環境に合わせて修正

# Color Sensor
colorsensor = le.ColorSensor()
connected = False

# Connect 処理
def connect_sensor():
    global connected

    try:
        # Connect ボタンを無効化
        connect_button.config(state=tk.DISABLED)

        status_label.config(text='Connecting...')
        root.update()

        colorsensor.connect(
            card_color=card_color,
            card_serial=card_serial
        )

        if colorsensor.connected:
            connected = True
            status_label.config(text='Connected')

            # Read Sensor ボタンを有効化
            read_button.config(state=tk.NORMAL)

#            messagebox.showinfo('Success', 'カラーセンサーに接続しました。')
        else:
            connected = False
            status_label.config(text='Connection Failed')
            messagebox.showerror('Error', 'カラーセンサーに接続できませんでした。')

            # Connect ボタンを有効化
            connect_button.config(state=tk.NORMAL)

    except Exception as e:
        connected = False
        status_label.config(text='Error')
        messagebox.showerror('Error', str(e))


# カラーセンサー読み取り
def read_sensor():
    if not connected:
        messagebox.showwarning('Warning', '先に Connect ボタンを押してください。')
        return

    try:
        #color
        #reflection
        #rawRed
        #rawGreen
        #rawBlue
        #hue
        #saturation
        #value

        # RGB値取得
        R = colorsensor.sensor.rawRed
        G = colorsensor.sensor.rawGreen
        B = colorsensor.sensor.rawBlue

        # 0~255 に制限
        R = max(0, min(255, int(R)))
        G = max(0, min(255, int(G)))
        B = max(0, min(255, int(B)))

        rgb_text.set(f'RGB: ({R}, {G}, {B})')

        # Tkinter 用カラーコード
        color_hex = f'#{R:02x}{G:02x}{B:02x}'

        # 四角形の色変更
        canvas.itemconfig(color_rect, fill=color_hex)

    except Exception as e:
        messagebox.showerror('Error', str(e))


# ウィンドウ終了時
def on_closing():
    try:
        if colorsensor.connected:
            colorsensor.disconnect()
    except:
        pass

    root.destroy()


# Tkinter GUI
root = tk.Tk()
root.title('Color Sensor Viewer')
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

# Read Sensor ボタン
# 初期状態では無効化
read_button = tk.Button(
    root,
    text='Read Sensor',
    width=20,
    height=2,
    command=read_sensor,
    state=tk.DISABLED
)
read_button.pack(pady=10)

# 状態表示
status_label = tk.Label(root, text='Not Connected')
status_label.pack(pady=5)

# RGB値表示
rgb_text = tk.StringVar()
rgb_text.set('RGB: (0, 0, 0)')

rgb_label = tk.Label(
    root,
    textvariable=rgb_text,
    font=('Arial', 14)
)
rgb_label.pack(pady=10)

# 色表示キャンバス
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack(pady=10)

# 初期色（黒）
color_rect = canvas.create_rectangle(
    0,
    0,
    200,
    200,
    fill='black'
)

# ウィンドウ終了処理
root.protocol('WM_DELETE_WINDOW', on_closing)

# 実行
root.mainloop()
