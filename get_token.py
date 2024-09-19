import json
import concurrent.futures
from profiles import Profile, gpm
from conf import number_of_concurrent_tasks

with open("token.txt", "w"):
    pass


def get_token(i):
    temp = Profile(id=gpm.profiles[i - 1]["id"])
    try:
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
        pass
    temp.close()


def run_concurrent_tasks(task_function, num_threads, repeat_tasks, start, end):
    tasks = list(range(start, end + 1))

    if repeat_tasks:
        tasks *= num_threads

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_task = {executor.submit(task_function, task): task for task in tasks}

        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            print(f"Running task {task}...")
            try:
                result = future.result()
            except Exception as exc:
                print(f"Err: {exc}")


run_concurrent_tasks(get_token, number_of_concurrent_tasks, False, 1, len(gpm.profiles))
