import os
from flask import Flask, render_template, request, redirect, url_for
from ReqForKappa import load_quests, check_kappa_requirement
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
quest_data = load_quests()

# Get 3 YouTube tutorials related to the query
def get_youtube_videos(query):
    api_key = os.environ.get("YOUTUBE_API_KEY") 

    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        q=f"{query} Tarkov",
        part="snippet",
        maxResults=3,
        type="video"
    )
    response = request.execute()


    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})

    return videos


#Check Quests Page For Required For Kappa
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("quest")
        return redirect(url_for("index", quest=query))  # Redirect after POST

    query = request.args.get("quest")
    if query:
        result = check_kappa_requirement(query, quest_data)
        youtube_results = get_youtube_videos(query)
        if result["status"] == "multiple":
            suggestions = result["matches"]
            return render_template("index.html", result=None, suggestions=suggestions, youtube_results=None)
        return render_template("index.html", result=result, suggestions=None, youtube_results=youtube_results)

    return render_template("index.html", result=None, suggestions=None, youtube_results=None)

if __name__ == "__main__":
    app.run(debug=True)