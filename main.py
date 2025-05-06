from flask import Flask, render_template, request, redirect, url_for
from ReqForKappa import load_quests, check_kappa_requirement

app = Flask(__name__)
quest_data = load_quests()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("quest")
        return redirect(url_for("index", quest=query))  # Redirect after POST

    query = request.args.get("quest")
    if query:
        result = check_kappa_requirement(query, quest_data)
        if result["status"] == "multiple":
            suggestions = result["matches"]
            return render_template("index.html", result=None, suggestions=suggestions)
        return render_template("index.html", result=result, suggestions=None)

    return render_template("index.html", result=None, suggestions=None)

if __name__ == "__main__":
    app.run(debug=True)