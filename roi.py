import cv2
import numpy as np

# **读取游戏截图**
image_path = "./team/1.png"  
image = cv2.imread(image_path)

# **读取排名模板**
template_dict = {i: cv2.imread(f"./rank/{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(1, 9)}

# **读取玩家 ID 模板**
name_template_dict = {
    "CGL彡Yang": cv2.imread("./id/yang.png", cv2.IMREAD_GRAYSCALE),
    "Nans青染": cv2.imread("./id/qingran.png", cv2.IMREAD_GRAYSCALE),
    "老中医爷爷": cv2.imread("./id/zhong.png", cv2.IMREAD_GRAYSCALE),
    "南山乾坤": cv2.imread("./id/kun.png", cv2.IMREAD_GRAYSCALE),
    "心驰放火烧三": cv2.imread("./id/san.png", cv2.IMREAD_GRAYSCALE),
    "CGL彡熙祀Nay": cv2.imread("./id/c4.png", cv2.IMREAD_GRAYSCALE),
    "铁观音不好喝": cv2.imread("./id/tie.png", cv2.IMREAD_GRAYSCALE),
    "CGL彡Dr未来": cv2.imread("./id/weilai.png", cv2.IMREAD_GRAYSCALE),
}

# **转换游戏截图为灰度**
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# **自适应二值化（防止高亮影响）**
binary_image = cv2.adaptiveThreshold(
    gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10
)

# **对所有模板进行自适应二值化**
for key in template_dict:
    template_dict[key] = cv2.adaptiveThreshold(
        template_dict[key], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

for key in name_template_dict:
    name_template_dict[key] = cv2.adaptiveThreshold(
        name_template_dict[key], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

ranking_positions = {}  # **存储排名的 `y` 坐标**
player_positions = {}   # **存储玩家 ID 的 `y` 坐标**

threshold = 0.7  # **降低阈值，提高匹配宽容度**

# **检测排名**
for number, template in template_dict.items():
    res = cv2.matchTemplate(binary_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    for pt in zip(*loc[::-1]):
        ranking_positions[number] = pt[1]  # 存储 `y` 坐标
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

# **检测玩家名字**
for name, template in name_template_dict.items():
    res = cv2.matchTemplate(binary_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    for pt in zip(*loc[::-1]):
        player_positions[name] = pt[1]  # 存储 `y` 坐标
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

# **匹配排名和玩家**
player_scores = {}
score_table = {1: 10, 2: 8, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}  # **评分规则**

for rank, rank_y in ranking_positions.items():
    best_match = None
    min_distance = float("inf")

    for player, player_y in player_positions.items():
        distance = abs(rank_y - player_y)
        if distance < min_distance:  # 选择 `y` 轴最接近的玩家
            best_match = player
            min_distance = distance

    if best_match:
        player_scores[best_match] = score_table[rank]
        print(f"🏆 玩家 '{best_match}' 排名 {rank}，获得 {score_table[rank]} 分")

# **最终得分输出**
print("\n🎯 最终得分:")
for player, score in player_scores.items():
    print(f"⭐ {player}: {score} 分")

# **显示最终标记的图片**
cv2.imshow("Matched Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
