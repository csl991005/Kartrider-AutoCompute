import cv2
import numpy as np
import pytesseract
import re
import os

# 配置 Tesseract-OCR 路径（Windows 用户）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 读取游戏截图
image_path = "./singer/3.png"
output_path = "./singer/processed_3.png"  # 处理后的图片保存路径

image = cv2.imread(image_path)

if image is None:
    print("❌ 无法读取图片，请检查路径是否正确！")
    exit()

# 1️⃣ **提取排名区域**
roi_x, roi_y, roi_w, roi_h = 10, 80, 300, 520  # 需要根据不同截图微调
rank_table = image[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

# 2️⃣ **转换为 HSV 颜色空间**
hsv = cv2.cvtColor(rank_table, cv2.COLOR_BGR2HSV)

# 3️⃣ **提取白色和绿色高亮的文字**
# 白色文字的 HSV 范围
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 50, 255])

# 绿色高亮的 HSV 范围
lower_green = np.array([35, 80, 80])
upper_green = np.array([85, 255, 255])

# 创建掩码
mask_white = cv2.inRange(hsv, lower_white, upper_white)
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# 合并掩码（获取白色和绿色的区域）
mask = cv2.bitwise_or(mask_white, mask_green)

# 4️⃣ **创建红色背景图**
red_background = np.full(rank_table.shape, (0, 0, 255), dtype=np.uint8)  # 纯红色背景 (BGR)

# 5️⃣ **将文字区域覆盖到红色背景上**
filtered_text_image = cv2.bitwise_and(rank_table, rank_table, mask=mask)
red_bg_with_text = cv2.addWeighted(filtered_text_image, 1, red_background, 0.5, 0)

# **📝 保存处理后的图像**
cv2.imwrite(output_path, red_bg_with_text)
print(f"✅ 处理后的图片已保存: {output_path}")

# 6️⃣ **OCR 识别**
custom_config = "--psm 6"
text = pytesseract.image_to_string(red_bg_with_text, config=custom_config)

print("🏆 识别的文本：")
print(text)

# 7️⃣ **解析排名和玩家 ID**
player_data = []
lines = text.split("\n")

for line in lines:
    match = re.search(r"(\d+)\s+([\w\s]+)", line)  # 匹配排名 + 玩家 ID
    if match:
        rank = int(match.group(1))
        player_id = match.group(2).strip()
        player_data.append((rank, player_id))

# 8️⃣ **按排名排序并输出**
player_data.sort()

print("\n🎯 解析出的排名信息：")
for rank, player_id in player_data:
    print(f"{rank} 名: {player_id}")

# 显示处理后的图像
cv2.imshow("Filtered Text on Red BG", red_bg_with_text)
cv2.waitKey(0)
cv2.destroyAllWindows()
