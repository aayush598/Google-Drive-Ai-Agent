document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('categorize-form');
    const loadingMessage = document.getElementById('loading-message');
    const progressBar = document.getElementById('progress-bar');
    const progress = document.getElementById('progress');
    const successMessage = document.getElementById('success-message');
    const errorMessage = document.getElementById('error-message');
    const filesList = document.getElementById('files-list');
    const duplicateFilesList = document.getElementById('duplicate-files-list');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        loadingMessage.style.display = 'block';
        progressBar.style.display = 'block';
        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';
        progress.style.width = '0%';

        try {
            const response = await fetch('/categorize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();
            displayCategorizedFiles(result.categorized_data);
            displayDuplicateFiles(result.duplicates);

            let progressValue = 0;
            const interval = setInterval(() => {
                if (progressValue < 100) {
                    progressValue += 10;
                    progress.style.width = progressValue + '%';
                } else {
                    clearInterval(interval);
                }
            }, 500);

            setTimeout(() => {
                loadingMessage.style.display = 'none';
                successMessage.style.display = 'block';
            }, 3000);
        } catch (error) {
            loadingMessage.style.display = 'none';
            progressBar.style.display = 'none';
            errorMessage.style.display = 'block';
        }
    });

    function displayCategorizedFiles(data) {
        filesList.innerHTML = '';
        for (const [fileName, categories] of Object.entries(data)) {
            const fileDiv = document.createElement('div');
            fileDiv.classList.add('file');

            const fileNameElement = document.createElement('h3');
            fileNameElement.textContent = fileName;

            const categoriesDiv = document.createElement('div');
            categoriesDiv.classList.add('categories');
            categories.split(', ').forEach(category => {
                const categorySpan = document.createElement('span');
                categorySpan.classList.add('category');
                categorySpan.textContent = category;
                categoriesDiv.appendChild(categorySpan);
            });

            fileDiv.appendChild(fileNameElement);
            fileDiv.appendChild(categoriesDiv);
            filesList.appendChild(fileDiv);
        }
    }

    function displayDuplicateFiles(duplicates) {
        duplicateFilesList.innerHTML = '';
        if (Object.keys(duplicates).length === 0) {
            duplicateFilesList.innerHTML = "<p>No duplicate files found.</p>";
        } else {
            for (const [fileName, count] of Object.entries(duplicates)) {
                const duplicateDiv = document.createElement('div');
                duplicateDiv.classList.add('duplicate-file');
                duplicateDiv.textContent = `${fileName} - Found ${count} times`;
                duplicateFilesList.appendChild(duplicateDiv);
            }
        }
    }
});

document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let categoryInput = document.getElementById("search-category").value;

    console.log("Search query:", categoryInput); // Debugging Log

    fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category: categoryInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Search response:", data); // Debugging Log
        
        let resultsDiv = document.getElementById("search-results");
        resultsDiv.innerHTML = "<h3>Matching Files:</h3>";

        if (data.files.length > 0) {
            let list = "<ul>";
            data.files.forEach(file => {
                list += `<li>${file}</li>`;
            });
            list += "</ul>";
            resultsDiv.innerHTML += list;
        } else {
            resultsDiv.innerHTML += "<p>No matching files found.</p>";
        }
    })
    .catch(error => console.error("Error:", error));
});
