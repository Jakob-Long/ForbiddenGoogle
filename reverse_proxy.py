import httpx
from flask import Flask, request, Response, render_template
from urllib.parse import quote  # Use urllib.parse.quote instead of werkzeug.urls.url_quote

app = Flask(__name__, static_folder='static')

external_url = "https://www.google.com"

async def fetch_content(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content, response.status_code

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/proxy")
async def proxy():
    try:
        search_query = request.args.get("query")
        full_url = f"{external_url}/search?q={quote(search_query)}"  # Use quote to encode the search_query
        content, status_code = await fetch_content(full_url)

        # Attempt to decode the content as UTF-8
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            # If decoding as UTF-8 fails, try 'ISO-8859-1' (latin1)
            content = content.decode('ISO-8859-1')

        # Include JavaScript to enhance the search results
        js_code = """
        <script>
            // Add click event listeners to the links
            document.querySelectorAll('a').forEach(function(link) {
                link.addEventListener('click', function(event) {
                    event.preventDefault();

                    const linkURL = link.href;

                    // Remove the prefix from the clicked URL
                   const cleanURL = link.href.replace('https://www.google.com/search?q=', '');

                    const newTab = window.open("about:blank");
                    newTab.document.open();
                    newTab.document.write(decodeURIComponent(cleanURL));
                    newTab.document.close();

                    setTimeout(function() {
                        newTab.document.title = "Classroom";
                    }, 1000);

                });
            });
        </script>
        """

        # Inject the JavaScript code into the content
        content = content.replace('</body>', f'{js_code}</body>', 1)

        # Encode the content as UTF-8 bytes before returning it
        content_bytes = content.encode('utf-8')

        return Response(content_bytes, content_type="text/html", status=status_code)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)

