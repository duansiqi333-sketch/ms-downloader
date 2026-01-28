import os, requests, json, re, tkinter as tk
from tkinter import messagebox

def get_ids_from_meaegi(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://meaegi.com/'
    }
    
    try:
        # 1. 提取分享码
        share_code = url.split("share=")[-1].split("&")[0]
        # 2. 访问 Meaegi 的内部 API 接口
        api_url = f"https://api.meaegi.com/share/{share_code}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            return None
            
        data = response.json()
        # 3. 解析物品列表
        items = data.get('char_data', {}).get('items', {})
        id_list = []
        
        # 提取身体/肤色 ID (通常是 2000, 2010 等)
        body_id = data.get('char_data', {}).get('body', 2012)
        id_list.append(str(body_id))
        
        # 提取其他所有穿着的部件 ID
        for slot, item_data in items.items():
            if item_data and 'id' in item_data:
                id_list.append(str(item_data['id']))
        
        return ",".join(id_list)
    except Exception as e:
        print(f"Detail Error: {e}")
        return None

def start_download(url_entry):
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("警告", "请输入链接")
        return

    print("正在连接 Meaegi 服务器...")
    char_id = get_ids_from_meaegi(url)
    
    if not char_id:
        messagebox.showerror("解析失败", "无法从该链接提取角色数据。\n请确保链接格式正确，或者 Meaegi 服务器当前可访问。")
        return

    print(f"提取到 ID 组合: {char_id}")
    actions = ["stand1", "walk1", "alert", "swingO1", "swingO2", "swingO3", "jump"]
    save_path = "character-action-split-frame" 
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://maplestory.io/'}

    for action in actions:
        action_dir = os.path.join(save_path, action)
        os.makedirs(action_dir, exist_ok=True)
        # 生成 JSON (MSW 格式)
        with open(os.path.join(action_dir, f"{action}.json"), 'w') as f:
            json.dump({"action": action, "frames": [{"frame": i, "x": -26, "y": -65} for i in range(4)]}, f)
        
        # 下载图片
        for frame in range(4):
            img_url = f"https://maplestory.io/api/character/{char_id}/{action}/{frame}?showears=false"
            try:
                img_r = requests.get(img_url, headers=headers, timeout=5)
                if img_r.status_code == 200:
                    with open(os.path.join(action_dir, f"{action}_{frame}.png"), 'wb') as f:
                        f.write(img_r.content)
                else: break
            except: break
            
    messagebox.showinfo("成功", "素材下载完成！\n请现在运行 AutoAlign.exe 并选 1。")

# UI 设置
root = tk.Tk()
root.title("MSW 一键素材助手 (修复版)")
root.geometry("450x180")

tk.Label(root, text="粘贴 Meaegi 链接 (例如: https://meaegi.com/dressing-room?share=...)").pack(pady=10)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)
tk.Button(root, text="提取素材并准备对齐", command=lambda: start_download(entry), bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
