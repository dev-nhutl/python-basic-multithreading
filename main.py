import threading, time, msvcrt

DELAY = 0.5

def threadAHandler(shutdownEvent: threading.Event, divisibleBy5: threading.Event, printLocker: threading.Lock):
    counter = 0
    while True:
        if shutdownEvent.is_set():
            break
        
        counter += 1
        if counter % 5 == 0:
            divisibleBy5.set()

        printLocker.acquire()
        print(threading.current_thread().name, ':', counter)
        printLocker.release()

        time.sleep(DELAY)

    printLocker.acquire()
    print(threading.current_thread().name, 'done. Counter:', counter)
    printLocker.release()
        

def threadBHandler(shutdownEvent: threading.Event, divisibleBy5: threading.Event, printLocker: threading.Lock):
    counter = 0
    while True:
        divisibleBy5.wait(DELAY * 6)
        if shutdownEvent.is_set():
            break
        counter += 1
        divisibleBy5.clear()

        printLocker.acquire()
        print(threading.current_thread().name, ':', counter)
        printLocker.release()
    
    printLocker.acquire()
    print(threading.current_thread().name, 'done. Counter:', counter)
    printLocker.release()
        

if __name__ == "__main__":
    
    shutdownEvent = threading.Event()
    divisibleBy5Event = threading.Event()
    printLocker = threading.Lock()

    threadA = threading.Thread(name='A', target=threadAHandler, args=(shutdownEvent, divisibleBy5Event, printLocker))
    threadB = threading.Thread(name='B', target=threadBHandler, args=(shutdownEvent, divisibleBy5Event, printLocker))

    threadA.start()
    threadB.start()

    msvcrt.getch()
    shutdownEvent.set()

    threadA.join()
    threadB.join()

