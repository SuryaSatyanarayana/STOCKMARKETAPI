import time

class TimeTracker:
    @staticmethod
    def remaining_time():
        current_time = time.localtime()
        minutes = current_time.tm_min
        seconds = current_time.tm_sec
        remaining_seconds = (5 - (minutes % 5)) * 60 - seconds
        return remaining_seconds

    @staticmethod
    def wait(seconds):
        print(f"WAITING FOR {seconds} SECONDS FOR THE NEXT 5 MINTUES CANDLE...")
        time.sleep(seconds)

    @staticmethod
    def print_current_time():
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print("Current time is:", current_time)

    @staticmethod
    def run():
        # Calculate the remaining time until the next 5-minute mark
        remaining_seconds = TimeTracker.remaining_time()

        # Wait for the remaining time
        TimeTracker.wait(remaining_seconds)

         # Print current time
        TimeTracker.print_current_time()