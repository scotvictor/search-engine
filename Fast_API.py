# ============================================================
# FASTAPI
# ============================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from Search_Engine import search

app = FastAPI(
    title="Scotly Search Engine"
)


class SearchRequest(BaseModel):
    query: str


@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<title>Mini Search Engine</title>

<style>

body {
    font-family: Arial;
    max-width: 800px;
    margin: 80px auto;
}

h1 {
    font-size: 40px;
}

input {
    width: 70%;
    padding: 14px;
    font-size: 18px;
}

button {
    padding: 14px 20px;
    font-size: 18px;
}

.result {
    margin-top: 30px;
}

.result a {
    font-size: 22px;
    color: #1a0dab;
}

.url {
    color: green;
}

</style>

</head>

<body>

<h1>Mini Search</h1>

<form action="/search">

<input
    name="q"
    placeholder="Search the web..."
>

<button type="submit">
Search
</button>

</form>

</body>

</html>
"""


@app.get("/search", response_class=HTMLResponse)
def search_web(q: str = ""):

    results = search(q)

    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>Search: {q}</title>

<style>

body {{
    font-family: Arial;
    max-width: 900px;
    margin: 40px auto;
}}

input {{
    width: 70%;
    padding: 12px;
    font-size: 18px;
}}

button {{
    padding: 12px;
}}

.result {{
    margin-top: 30px;
}}

.result a {{
    font-size: 21px;
    color: #1a0dab;
}}

.url {{
    color: green;
    font-size: 14px;
}}

</style>

</head>

<body>

<form action="/search">

<input name="q" value="{q}">

<button>Search</button>

</form>
"""

    for result in results:

        html += f"""
<div class="result">

<a href="{result['url']}" target="_blank">
{result['title']}
</a>

<div class="url">
{result['url']}
</div>

<p>
{result['snippet']}
</p>

</div>
"""

    html += """

</body>
</html>
"""

    return html
