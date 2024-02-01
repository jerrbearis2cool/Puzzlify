import subprocess
import os, threading, traceback

class RunENV():
    def __init__(self, code):
        self.code = code
        self.blacklist = open("blacklist.txt", "r").read().splitlines()
        self.timeout = 1

    def check(self):
        """Check for blacklisted keywords."""
        output = ""
        error_keyword = None

        for line in self.code.splitlines():
            for keyword in self.blacklist:
                if keyword in line:
                    error_keyword = keyword
                    break

        return not error_keyword, error_keyword, output


    def timer(self):
        self.proc.terminate()

    def run(self):
        #threading.Timer(1, self.timer).start()
        
        try:
            try:
                result = subprocess.run(['python', '-c', self.code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=0.5)
                self.out = result.stdout
                self.err = result.stderr

                if self.err == None or self.err == "":
                    return True, self.out
                else:
                    return False, self.err

            except subprocess.TimeoutExpired:
                return False, 'Runtime took too long!'
            except Exception as e:
                return False, str(traceback.format_exc()), None

        except Exception as e:
            return False, str(e), None

        self.proc.terminate()

run = RunENV(
"""
for i in range(0, 10):
    print(i)
""")
print(run.run()[1].split("\n"))