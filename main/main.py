import subprocess

# 建立三個子程式的命令列表
commands = [
    ["python", "main/回覆.py"],
    ["python", "main/回覆++.py"],
    ["python", "main/回覆--.py"],
    ["python", "main/回覆List.py"],
    ["python", "main/屁眼回覆.py"]
]

# 建立一個子程式列表，並逐一執行每個子程式
processes = []
for command in commands:
    # 使用 Popen 函數建立一個子程式，並將 stdout 和 stderr 設置為 PIPE
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 將每個子程式加入到子程式列表中
    processes.append(proc)

# 監控每個子程式的輸出
for proc in processes:
    # 使用 communicate 函數獲取子程式的輸出
    stdout, stderr = proc.communicate()
    # 將輸出印出到控制台
    print(stdout.decode())
    print(stderr.decode())
