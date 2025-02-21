import mss
import cv2
import numpy as np
import win32gui

# 获取窗口的客户区坐标
def get_client_area(hwnd):
    """获取窗口的客户区坐标（去掉标题栏和边框）"""
    # 获取窗口客户区的宽高
    rect = win32gui.GetClientRect(hwnd)
    width, height = rect[2], rect[3]  # 宽度 & 高度

    # 确保游戏分辨率是 1600x900 或 1920x1080
    if (width, height) not in [(1600, 900), (1920, 1080)]:
        print(f"⚠️ 检测到异常分辨率: {width}x{height}，请检查游戏窗口是否全屏！")
        return None

    # 获取客户区的左上角在屏幕上的位置
    left, top = win32gui.ClientToScreen(hwnd, (0, 0))

    return {"left": left, "top": top, "width": width, "height": height}

# 游戏窗口标题
window_name = "PopKart Client"
hwnd = win32gui.FindWindow(None, window_name)

if hwnd:
    print(f"✅ 找到窗口: {window_name}，句柄: {hwnd}")

    # 获取游戏窗口的客户区（真实游戏画面区域）
    region = get_client_area(hwnd)
    
    if region:
        print(f"🎮 捕获区域: left={region['left']}, top={region['top']}, width={region['width']}, height={region['height']}")

        with mss.mss() as sct:
            while True:
                screenshot = sct.grab(region)  # 截取游戏画面
                frame = np.array(screenshot)  # 转换为 NumPy 数组
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # 转换颜色通道

                cv2.imshow("KartRider Capture", frame)

                # 按 'q' 退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
    else:
        print("⚠️ 无法获取游戏窗口的客户区域，请确认游戏是否处于窗口化或全屏窗口模式")
else:
    print("❌ 未找到游戏窗口，请确保游戏正在运行")
