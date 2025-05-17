## Cách chạy "live server" khi fix code Python (PyQt)

### 1. Sử dụng chế độ tự động reload với `watchdog` hoặc `entr`
- **Cài đặt:**  
  ```
  pip install watchdog
  ```
- **Chạy app với tự động reload khi code thay đổi:**  
  ```
  watchmedo auto-restart --pattern="*.py" --recursive -- python gui_app/app_gui.py
  ```
  Hoặc nếu dùng Linux/macOS:
  ```
  find . -name "*.py" | entr -r python gui_app/app_gui.py
  ```

### 2. Sử dụng VSCode "Run on Save"
- Cài extension [Run on Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave).
- Cấu hình `.vscode/settings.json`:
  ```json
  {
    "emeraldwalk.runonsave": {
      "commands": [
        {
          "match": ".*\\.py$",
          "cmd": "python gui_app/app_gui.py"
        }
      ]
    }
  }
  ```
- Mỗi lần lưu file, VSCode sẽ tự chạy lại app.

### 3. Tự viết script Python tự restart khi code thay đổi
- Tạo file `dev_server.py`:
  ```python
  import subprocess, time, os

  def run():
      proc = subprocess.Popen(["python", "gui_app/app_gui.py"])
      return proc

  def watch(paths):
      mtimes = {f: os.path.getmtime(f) for f in paths}
      while True:
          time.sleep(1)
          for f in paths:
              if os.path.getmtime(f) != mtimes[f]:
                  return True
          return False

  if __name__ == "__main__":
      import glob
      py_files = glob.glob("**/*.py", recursive=True)
      while True:
          p = run()
          while True:
              if watch(py_files):
                  p.terminate()
                  break
  ```
- Chạy:  
  ```
  python dev_server.py
  ```

---

**Lưu ý:**  
- Nếu dùng PyQt, mỗi lần reload sẽ đóng app cũ và mở app mới.
- Không dùng được hot reload như web, nhưng sẽ tự động restart app khi sửa code.
