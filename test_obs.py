import os
import time
from obswebsocket import obsws, requests

folder_name = "obs_screenshots"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    print(f"文件夹 '{folder_name}' 创建成功。")
else:
    print(f"文件夹 '{folder_name}' 已存在，跳过创建。")

# 连接到 OBS WebSocket
ws = obsws("localhost", 4455, "dX1dM9OhpGcxA7iK")
ws.connect()

screenshot_path = "E:/KartRider-AutoCompute/obs_screenshots"  # 指定 OBS 截图保存的路径（确保 OBS 有写入权限）

def save_screenshot():
    """ 让 OBS 直接保存截图到本地 """
    filename = f"{screenshot_path}/obs_capture_{int(time.time())}.png"
    response = ws.call(requests.SaveSourceScreenshot(
        sourceName="跑跑卡丁车", imageFormat="png", imageFilePath=filename,imageCompressionQuality=50))
    
    if response.status:
        print(f"截图已保存: {filename}")
    else:
        print("截图保存失败！")

try:
    while True:
        save_screenshot()  # 让 OBS 直接截图
        time.sleep(3)  # 每秒截图一次
except KeyboardInterrupt:
    print("程序终止")
    ws.disconnect()
