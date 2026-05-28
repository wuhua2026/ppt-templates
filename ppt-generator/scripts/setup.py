"""
PPT模板库自动安装脚本

自动克隆/更新模板仓库并安装依赖。
用法: python setup.py
"""
import subprocess
import sys
import os

REPO_URL = "https://github.com/wuhua2026/ppt-templates.git"
INSTALL_DIR = os.path.join(os.path.expanduser("~"), ".ppt-templates")


def run(cmd, check=True):
    """执行命令并返回结果"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [ERROR] {result.stderr.strip()}")
    return result


def setup():
    """安装/更新模板库"""
    print("=" * 50)
    print("  PPT模板库 安装程序")
    print("=" * 50)

    # 检查是否已安装
    if os.path.exists(INSTALL_DIR):
        print(f"\n已检测到模板库: {INSTALL_DIR}")
        print("正在更新...")
        run(f'cd "{INSTALL_DIR}" && git pull')
        print("更新完成!")
    else:
        print(f"\n正在克隆模板库到: {INSTALL_DIR}")
        run(f'git clone {REPO_URL} "{INSTALL_DIR}"')
        print("克隆完成!")

    # 安装Python依赖
    print("\n安装Python依赖...")
    run(f"{sys.executable} -m pip install python-pptx Pillow lxml -q")

    # 安装JS依赖（如果Node.js可用）
    js_dir = os.path.join(INSTALL_DIR, "js")
    if os.path.exists(js_dir):
        result = run("node --version", check=False)
        if result.returncode == 0:
            print("安装JavaScript依赖...")
            run(f'cd "{js_dir}" && npm install --silent', check=False)

    print("\n" + "=" * 50)
    print("  安装完成!")
    print(f"  模板库位置: {INSTALL_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    setup()
