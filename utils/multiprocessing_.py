from tqdm import tqdm
from multiprocessing import pool


# noinspection PyProtectedMember
def async_progress(res: pool.MapResult, desc: str = None, wait_time: float = 0.5):
    total = res._number_left
    tq = tqdm(desc=desc, total=total)

    prev = res._number_left
    while not res.ready():
        if res._number_left < prev:
            tq.update(prev - res._number_left)
        prev = res._number_left
        # time.sleep(wait_time)
        res.wait(wait_time)
    tq.update(prev - res._number_left)
    tq.close()
