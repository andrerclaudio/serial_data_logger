# Build-in modules
import logging
import time
from datetime import timedelta
from threading import ThreadError, Thread
# from math import sin, radians
# from matplotlib.animation import FuncAnimation
from pytictoc import TicToc
import sqlite3
# import matplotlib.pyplot as plt


# Print in software terminal
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(process)d | %(name)s | %(levelname)s:  %(message)s',
                    datefmt='%d/%b/%Y - %H:%M:%S')

logger = logging.getLogger(__name__)


HEX_COLOR_TABLE = [('Red', 0xFF0000),
                   ('Lime', 0x00FF00),
                   ('Blue', 0x0000FF),
                   ('Yellow', 0xFFFF00),
                   ('Cyan', 0x00FFFF),
                   ('Magenta', 0xFF00FF)]

COLOR_NAME_INDEX = 0
COLOR_VALUE_INDEX = 1


class ElapsedTime(object):
    """
    Measure the elapsed time between Tic and Toc
    """
    def __init__(self):
        self.t = TicToc()
        self.t.tic()

    def elapsed(self):
        _elapsed = self.t.tocvalue()
        d = timedelta(seconds=_elapsed)
        logger.info('< {} >'.format(d))


class ThreadingProcessQueue(object):
    """
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval):
        """
        Constructor
        """
        self.interval = interval

        thread = Thread(target=run, args=(self.interval,), name='Thread_name')
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


def run(interval):
    """ Method that runs forever """
    while True:
        try:
            time.sleep(interval)

        except ThreadError as e:
            logger.exception('{}'.format(e))

        finally:
            pass


def animate(i, xs, ys, ax):
    """This function is called periodically from FuncAnimation"""

    # Add x and y to lists
    # xs.append(datetime.now().strftime('%H:%M:%S'))
    xs.append(i)
    ys.append(sin(radians(i)))

    # Limit x and y lists to 20 items
    xs = xs[-360:]
    ys = ys[-360:]

    # Draw x and y lists
    ax.clear()
    ax.scatter(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Signal')
    plt.ylabel('Value')


def application():
    """" All application has its initialization from here """   

    # Create figure for plotting
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)

    # xs = []
    # ys = []

    # Set up plot to call animate() function periodically
    # ani = FuncAnimation(fig, animate, fargs=(xs, ys, ax), cache_frame_data=False, interval=1,)
    # plt.show()

    conn = sqlite3.connect('log.db')

    table_name = 'eval_{}'.format(int(time.time()))

    conn.execute('''
        CREATE TABLE "{}" (
        "timestamp"	INTEGER NOT NULL,
        "channel"	INTEGER NOT NULL,
        "value"	INTEGER NOT NULL,
        "color"	INTEGER NOT NULL,
        "state"	TEXT NOT NULL);
    '''.format(table_name))

    channel_info = {'channel_length': 0,
                    'channel_qty': 0}

    c = conn.cursor()
    
    # length = int(input('Enter with the data length in bytes (e.g.: 2 bytes): '))
    # channel_info['channel_length'] = length
    
    # qty = int(input('Enter with the number of channels (max. 6 channels): '))

    # if qty <= len(HEX_COLOR_TABLE):
    #     channel_info['channel_qty'] = qty            
    #     for ch in range(channel_info['channel_qty']):
    #         channel_info['ch_{}'.format(ch)] = HEX_COLOR_TABLE[ch][COLOR_VALUE_INDEX]

    
    param = """INSERT INTO {} (timestamp, channel, value, color, state) VALUES (?, ?, ?, ?, ?);""".format(table_name)
    data_tuple = (int(time.time()), 1, 32135, 255, 'D')
    c.execute(param, data_tuple)

    conn.commit()
    conn.close()


def main():
    application()
    return None


if __name__ == "__main__":
    # Run the main function.
    main()
