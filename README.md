# temp.py 🔥

### A python CPU temperature monitor for Linux,

Run timed tests on your CPU temperature and fan speed, optionally, apply a full load on your CPU in order to gauge you thermal performance.

---

## 💻 Usage

```
python3 temp.py [-h] [-t TIME] [-v] [-s]


optional arguments:
  -h, --help            show this help message and exit

  -t TIME, --time TIME  Define how long the test should go on for in seconds,
                        default is 60 seconds

  -v, --verbose         Show the list of recorded readings of the current test

  -s, --stress          Apply stress test to the CPU while the test is running

```
