import time
import threading

class TimedList:
    def __init__(self, expiration_seconds=86400):  # 86400 seconds = 24 hours
        self.items = []
        self.expiration_seconds = expiration_seconds
        self.lock = threading.Lock()
        self._start_cleanup_thread()

    def add(self, item):
        with self.lock:
            timestamp = time.time()
            self.items.append((item, timestamp))

    def get_items(self):
        with self.lock:
            return [item for item, timestamp in self.items]

    def contains(self, item):
        """Check if an item is in the list and not expired."""
        current_time = time.time()
        with self.lock:
            for existing_item, timestamp in self.items:
                if existing_item == item and (current_time - timestamp < self.expiration_seconds):
                    return True
            return False

    def _remove_expired(self):
        current_time = time.time()
        with self.lock:
            self.items = [(item, timestamp) for item, timestamp in self.items if current_time - timestamp < self.expiration_seconds]

    def _start_cleanup_thread(self):
        def cleanup_loop():
            while True:
                self._remove_expired()
                time.sleep(60)  # check every 60 seconds

        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()