import random, uuid
from run import RunENV
from flask import *

app = Flask(__name__)

blacklist = open("blacklist.txt", "r").read().splitlines()

challenges = {
    1: { # diff 1
            "count010": {"out": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ''], "info": "<p>Write a script that will print <b>integers from 0 to 10</b></p>"},
            "sort_list": {"out": ['[4, 16, 42, 76, 129, 193, 532, 826]', ''], "info": '''<p>Write a script that will sort the following list:</p><div style="background-color: black; border-radius: 5px; padding: 2px; margin: 20px;">
<p style="color: white;">[16, 42, 826, 76, 193, 129, 4, 532]</p>
</div>'''}},
    2: { # diff 2
            "bank": {"in": None, "out": {"Bob": 3, "Jeffery": 7, "Alex": 4, "Joseph": 6}, "info": '''<p>Write a script that will give a dictionary of customers a value equal to the length of their name (ex. {"Jerry": 5})<p><div style="background-color: black; border-radius: 5px; padding: 2px; margin: 20px;">
<p style="color: white;">{"Bob": 0, "Jeffery": 0, "Alex": 0, "Joseph": 0}</p>'''},
        },
    3: { # diff 3
        }
}


def randomChallenge(diff: int = 1):
    "returns a random key from challenges based on diff"
    return random.choice(list(
        challenges[diff] # if an error appears in this line, check if diff is an integer
    ))

print(randomChallenge())

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/test")
def asdf():
    return render_template("test.html")

@app.route("/<level>/<challenge>", methods=["GET", "POST"])
def challenge(level, challenge):

    if request.method == "GET":
        return render_template("challenge.html", challenge=challenges[int(level)][challenge], diff=level, name=challenge, info=challenges[int(level)][challenge]["info"])
    else:
        instance = RunENV(request.form.get("code"))
        print(request.form.get("code"))
        check = instance.check()
        if check[0] == True:
            out = instance.run()
            print(int(request.form.get("diff")))
            if out[0] == True:
                if challenges[int(request.form.get("diff"))][request.form.get("name")]["out"] == out[1].split("\n"):
                    return {"result": "passed", "reason": out[1]}
                else:
                    return {"result": "failed", "reason": "incorrect submission"}
            else:
                return {"result": "failed", "reason": out[1]}
        else:
            return {"result": "failed", "reason": f"detected blacklisted keyword: {check[1]}"}

@app.route("/alt", methods=["POST"])
def challengealt():

    j = request.get_json(force=True) 
    print(j["code"])
    instance = RunENV(
        str(j["code"].replace(u"U+00A0", " "))
    )

    check = instance.check()

    if check[0] == True:
        out = instance.run()
        print(int(j["diff"]))
        if out[0] == True:
            if challenges[int(j.get("diff"))][j.get("name")]["out"] == out[1].split("\n"):
                return {"result": "passed", "reason": out[1]}
            else:
                return {"result": "failed", "reason": "Incorrect submission!"}
        else:
            return {"result": "failed", "reason": out[1]}
    else:
        return {"result": "failed", "reason": f"Blacklisted keyword: {check[1]}"}
if __name__ == "__main__":
    app.run(host="192.168.0.46", port=80)