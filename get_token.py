import json
from gpm import Gpm
from profiles import Profile

gpm = Gpm(port=16911)
for profile in gpm.profiles:
    try:
        temp = Profile(id=gpm.profiles[0]["id"])
        temp.open_url("https://web.telegram.org/k/#@Tomarket_ai_bot")
        temp.click("//div[@class='new-message-bot-commands is-view']")
        temp.click("//button[@class='popup-button btn primary rp']")
        iframe = temp.wait_element("//iframe")
        temp.driver.switch_to.frame(iframe)
        token = temp.run_script("return window.localStorage.getItem('token');")
        if token:
            print(f"{temp.detail['name']} | {token}")
            with open("token.txt", "a") as f:
                f.write(f"{temp.detail['name']} | {token}\n")
    except Exception as e:
        print(e)
        continue
