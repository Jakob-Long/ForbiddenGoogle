const form = document.getElementById("search-form");
const input = document.getElementById("search-query");
const resultsDiv = document.getElementById("search-results");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const query = input.value;
    if (query.trim() !== "") {
        searchDuckDuckGo(query);
    }
});

function searchDuckDuckGo(query) {
    const apiUrl = `https://api.duckduckgo.com/?q=${query}&format=json`;

    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => displayResults(data.Results))
        .catch((error) => console.error("Error:", error));
}

function displayResults(results) {
    resultsDiv.innerHTML = "";

    if (results && results.length > 0) {
        results.forEach((result) => {
            const link = document.createElement("a");
            link.href = result.FirstURL;
            link.textContent = result.Text;
            link.target = "_blank";

            const resultItem = document.createElement("div");
            resultItem.classList.add("result-item");
            resultItem.appendChild(link);

            resultsDiv.appendChild(resultItem);
        });
    } else {
        resultsDiv.textContent = "No results found.";
    }
}
