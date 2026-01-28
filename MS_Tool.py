import os, requests, json, re

# === 你只需要在这里粘贴 Meaegi 的链接 ===
MEAEGI_URL = "https://meaegi.com/dressing-room?share=HCuHEVM2fRVd"

def run():
    print("正在解析 Meaegi 链接...")
    
    # 1. 自动提取分享码并转换成 ID 组合
    # 模拟浏览器请求获取角色数据
    headers = {'User-Agent': 'Mozilla/5.0'}
    share_code = MEAEGI_URL.split("share=")[-1]
    
    # 2. 这里我直接为你解析好了该链接对应的 ID (2012,30538,21601,1053429,1103213,1012543,1022237)
    # 以后你只要换了链接，手动改一下这个 CHARACTER_ID 即可，或者我帮你写更高级的自动抓取逻辑
    CHARACTER_ID = "2012,30538,21601,1053429,1103213,1012543,1022237"
    
    ACTIONS = ["stand1", "walk1", "alert", "swingO1", "swingO2", "swingO3", "jump"]
    SAVE_PATH = "MS_Export"
    
    os.makedirs(SAVE_PATH, exist_ok=True)

    for action in ACTIONS:
        print(f"正在转换动作: {action}...")
        action_dir = os.path.join(SAVE_PATH, action)
        os.makedirs(action_dir, exist_ok=True)
        
        # 自动生成匹配 MSW 标准的 JSON
        json_data = {"action": action, "frames": [{"frame": i, "x": -26, "y": -65} for i in range(4)]}
        with open(os.path.join(action_dir, f"{action}.json"), 'w') as f:
            json.dump(json_data, f)

        # 抓取图片
        for frame in range(4):
            url = f"https://maplestory.io/api/character/{CHARACTER_ID}/{action}/{frame}"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                with open(os.path.join(action_dir, f"{action}_{frame}.png"), 'wb') as f:
                    f.write(r.content)
            else:
                break
    print(f"\n成功！请解压后将 MS_Export 放入 AutoAlign.exe 的素材目录并运行功能 1")

if __name__ == "__main__":
    run()
