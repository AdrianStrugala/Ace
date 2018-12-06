import threading
import communication
import time


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=0.5):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            if (len(communication.list_to_say) != 0):
                print(communication.list_to_say[0])
                del communication.list_to_say[0]

            time.sleep(self.interval)


# time.sleep(3)
# print('Checkpoint')
# time.sleep(2)
# print('Bye')