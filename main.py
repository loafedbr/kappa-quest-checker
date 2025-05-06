from flask import Flask, render_template, request
from ReqForKappa import load_quests, check_kappa_requirement

app = Flask(__name__)
quest_data = load_quests()

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    if request.method == "POST":
        query = request.form.get("quest")
    elif request.method == "GET":
        query = request.args.get("quest")

    if query:
        result = check_kappa_requirement(query, quest_data)
        if result["status"] == "multiple":
            suggestions = result["matches"]
            return render_template("index.html", result=None, suggestions=suggestions)
        return render_template("index.html", result=result, suggestions=None)

    return render_template("index.html", result=None, suggestions=None)

    # If it's a GET request (refresh), show clean form
    return render_template("index.html", result=None, suggestions=None)

if __name__ == "__main__":
    app.run(debug=True)