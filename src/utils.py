from multiprocessing import cpu_count

def auto_delay() -> float:
    """
    Returns a appropriate delay for the current CPU count.
    """
    cores = cpu_count()
    if cores in range(2,5):
        delay = 1.0
    else:
        delay = 0.1
    
    return delay