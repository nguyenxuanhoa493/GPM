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


def test(i):
    print(i)


run_concurrent_tasks(test, 10, True, 0, 10)
