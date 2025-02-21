import cv2
import numpy as np

# 读取游戏截图
image_path = "./team/1.png"
image = cv2.imread(image_path)

if image is None:
    print("❌ 无法读取图片，请检查路径是否正确！")
    exit()

# 转换为HSV颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 蓝色队伍的颜色范围 (HSV)
blue_lower = np.array([90, 50, 50])  # 蓝色下界
blue_upper = np.array([150, 255, 255])  # 蓝色上界

# 红色队伍的颜色范围 (HSV)
red_lower1 = np.array([0, 50, 50])    # 红色（低区间）
red_upper1 = np.array([10, 255, 255])

red_lower2 = np.array([160, 50, 50])  # 红色（高区间）
red_upper2 = np.array([180, 255, 255])

# 创建掩码（分别检测蓝色 & 红色）
blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)

# 合并两个红色区域
red_mask = cv2.bitwise_or(red_mask1, red_mask2)

# 寻找蓝色和红色区域的轮廓
contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 用于存储玩家的行区域
player_rows = []

# 提取玩家信息（基于位置）
def extract_players_from_contours(contours, color):
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        player_img = image[y:y+h, x:x+w]
        
        # 这里简单地返回 y 和 x 坐标范围，用于排序和进一步处理
        player_rows.append((y, x, w, h, color))

# 处理蓝色队伍
extract_players_from_contours(contours_blue, "blue")

# 处理红色队伍
extract_players_from_contours(contours_red, "red")

# 按照 y 坐标排序，确保从上到下
player_rows.sort()

# 假设前4个为蓝队，后4个为红队（根据实际游戏截图调整）
blue_team_players = player_rows[:4]
red_team_players = player_rows[4:]

# 输出排序和识别的玩家信息
print("🎯 蓝队玩家: ", blue_team_players)
print("🎯 红队玩家: ", red_team_players)

# 计算得分
scores = {player[4]: 0 for player in player_rows}

for idx, (y, x, w, h, color) in enumerate(blue_team_players):
    scores[color] += 10 - idx  # 蓝队得分计算
for idx, (y, x, w, h, color) in enumerate(red_team_players):
    scores[color] += 10 - idx  # 红队得分计算

# 打印得分
for color, score in scores.items():
    print(f"🏆 {color} 队得分: {score} 分")

# 可视化检测结果
cv2.imshow("Blue Mask", blue_mask)
cv2.imshow("Red Mask", red_mask)
cv2.imshow("Detected Players", image)
cv2.waitKey(0)
cv2.destroyAllWindows()