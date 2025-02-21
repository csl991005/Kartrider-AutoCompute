import cv2
import numpy as np
import pytesseract
import os

# 配置 Tesseract-OCR 路径（Windows 用户）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 读取游戏截图
image_path = "./singer/processed_3.png"  # 之前保存的红色背景处理后的图片
image = cv2.imread(image_path)

if image is None:
    print("❌ 无法读取图片，请检查路径是否正确！")
    exit()

# **1️⃣ 左右裁切**
height, width, _ = image.shape

# 左侧排名区域 (大概 0% ~ 25% 的宽度)
left_rank = image[:, :int(width * 0.12)]

# 右侧玩家 ID 区域 (大概 25% ~ 100% 的宽度)
right_players = image[:, int(width * 0.10):]

# **2️⃣ 识别左侧排名**
gray_rank = cv2.cvtColor(left_rank, cv2.COLOR_BGR2GRAY)
_, binary_rank = cv2.threshold(gray_rank, 128, 255, cv2.THRESH_BINARY_INV)

# OCR 读取排名数字
custom_config = "--psm 6 digits"
rank_text = pytesseract.image_to_string(binary_rank, config=custom_config)
rank_list = [int(r) for r in rank_text.split() if r.isdigit()]

print("🎯 识别出的排名列表:", rank_list)

# **3️⃣ 与本地存储的 1-8 模板进行匹配**
template_dir = "./rank/"  # 你的本地模板存储路径
templates = {str(i): cv2.imread(os.path.join(template_dir, f"{i}.png"), 0) for i in range(1, 9)}

matched_ranks = []

for number, template in templates.items():
    if template is None:
        continue

    # **检查模板大小**
    if template.shape[0] > binary_rank.shape[0] or template.shape[1] > binary_rank.shape[1]:
        print(f"⚠️ 模板 {number} 太大，自动缩小！")
        scale_x = binary_rank.shape[1] / template.shape[1] * 0.8  # 缩小 80%
        scale_y = binary_rank.shape[0] / template.shape[0] * 0.8  # 缩小 80%
        template = cv2.resize(template, (0, 0), fx=scale_x, fy=scale_y)

    # 进行模板匹配
    res = cv2.matchTemplate(binary_rank, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    if max_val > 0.8:
        matched_ranks.append(int(number))


print("✅ 通过模板匹配出的排名:", matched_ranks)

# **4️⃣ 识别右侧玩家 ID**
gray_players = cv2.cvtColor(right_players, cv2.COLOR_BGR2GRAY)
_, binary_players = cv2.threshold(gray_players, 128, 255, cv2.THRESH_BINARY_INV)

player_text = pytesseract.image_to_string(binary_players, config="--psm 6")
player_names = [p.strip() for p in player_text.split("\n") if p.strip()]

print("🏆 识别出的玩家 ID:", player_names)

# **5️⃣ 关联排名和玩家**
if len(matched_ranks) == len(player_names):
    final_result = list(zip(matched_ranks, player_names))
    final_result.sort()
    print("\n🎯 最终排名结果:")
    for rank, player in final_result:
        print(f"{rank} 名: {player}")
else:
    print("❌ 识别出的排名和玩家数量不匹配，请调整阈值或检查图像质量！")

# 显示裁剪后的图像
cv2.imshow("Rank Area", left_rank)
cv2.imshow("Player ID Area", right_players)
cv2.waitKey(0)
cv2.destroyAllWindows()
