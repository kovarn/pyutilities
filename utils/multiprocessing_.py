# noinspection PyProtectedMember
def async_progress(res, desc=None, wait_time=0.5):
    import time
    from tqdm import tqdm
    from .itertools_ import consume

    total = res._number_left

    # noinspection PyProtectedMember
    def progress():
        prev = res._number_left
        while True:
            while res._number_left == prev and not res.ready():
                time.sleep(0.5)
            prev -= 1
            yield prev
            if prev <= 0:
                break

    consume(tqdm(progress(), total=total, desc=desc), None)
