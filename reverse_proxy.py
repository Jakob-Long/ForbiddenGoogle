import httpx
from flask import Flask, request, Response, render_template

app = Flask(__name__, static_folder='static')

external_url = "https://www.google.com"

async def fetch_content(query):
    async with httpx.AsyncClient() as client:
        full_url = external_url + "/search?q=" + query
        response = await client.get(full_url)
        return response.content, response.status_code

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/proxy")
async def proxy():
    try:
        search_query = request.args.get("query")
        content, status_code = await fetch_content(search_query)
        return Response(content, content_type="text/html", status=status_code)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
