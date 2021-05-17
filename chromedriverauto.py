import requests, zipfile, io, os, subprocess


def chromedriverautodownload():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver = "chromedriver.exe"
    out = subprocess.getoutput(f"{chromedriver} -v")
    if "ChromeDriver" in out:
        print(f"{out} \nChromeDriver exists in path and is executable")
    else:
        url = "https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_win32.zip"
        try:
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
            chromedriver = f"{curr_dir}\chromedriver.exe"
            return chromedriver
        except Exception as e:
            print(f"Cannot download chromedriver\n {e}")
