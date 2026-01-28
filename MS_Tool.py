import os, requests, json, tkinter as tk
from tkinter import messagebox

def get_ids_from_meaegi(url):
    # 自动从 meaegi 链接解析出 ID 组合
    share_code = url.split("share=")[-1]
    api_url = f"https://api.meaegi.com/share/{share_code}"
    try:
        data = requests.get(api_url).json()
        # 提取各个部位的 ID
        items = data['char_data']['items']
        ids = [str(i['id']) for i in items.values() if i]
        return ",".join(ids)
    except:
        return None

def start_download(url_entry):
    url = url_entry.get()
    char_id = get_ids_from_meaegi(url)
    
    if not char_id:
        messagebox.showerror("错误", "无法解析 Meaegi 链接，请检查网络或链接是否正确")
        return

    actions = ["stand1", "walk1", "alert", "swingO1", "jump"]
    save_path = "character-action-split-frame" # 直接指向对齐软件的目录
    os.makedirs(save_path, exist_ok=True)

    for action in actions:
        action_dir = os.path.join(save_path, action)
        os.makedirs(action_dir, exist_ok=True)
        # 生成 JSON
        with open(os.path.join(action_dir, f"{action}.json"), 'w') as f:
            json.dump({"action": action, "frames": [{"frame": i, "x": -26, "y": -65} for i in range(4)]}, f)
        # 下载图片
        for frame in range(4):
            img_r = requests.get(f"https://maplestory.io/api/character/{char_id}/{action}/{frame}")
            if img_r.status_code == 200:
                with open(os.path.join(action_dir, f"{action}_{frame}.png"), 'wb') as f:
                    f.write(img_r.content)
            else: break
            
    messagebox.showinfo("成功", f"素材已下载完成！\n现在请运行文件夹内的 AutoAlign.exe 并选 1 即可出 PSD。")

# 建立简单的 UI 界面
root = tk.Tk()
root.title("MSW 一键直出助手")
root.geometry("400x150")

tk.Label(root, text="请粘贴 Meaegi 分享链接:").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)
tk.Button(root, text="开始下载素材并准备对齐", command=lambda: start_download(entry)).pack(pady=20)

root.mainloop()
