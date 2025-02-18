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
    
    // Show status indicators
    loadingMessage.style.display = 'block';
    progressBar.style.display = 'block';
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';
    progress.style.width = '0%';

    try {
        const response = await fetch('/categorize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        const categorizedData = result.categorized_data;
        const duplicates = result.duplicates;

        // Simulate progress
        let progressValue = 0;
        const interval = setInterval(() => {
            if (progressValue < 100) {
                progressValue += 10;
                progress.style.width = progressValue + '%';
            } else {
                clearInterval(interval);
            }
        }, 500);

        // Hide the loading message and show success message
        setTimeout(() => {
            loadingMessage.style.display = 'none';
            successMessage.style.display = 'block';
            displayCategorizedFiles(categorizedData);
            displayDuplicateFiles(duplicates);
        }, 3000); // Simulate delay after completion

    } catch (error) {
        loadingMessage.style.display = 'none';
        progressBar.style.display = 'none';
        errorMessage.style.display = 'block';
    }
});

function displayCategorizedFiles(data) {
    filesList.innerHTML = ''; // Clear previous data

    // Iterate through the categorized data and display each file
    for (const [fileName, categories] of Object.entries(data)) {
        if (fileName && categories) {
            const fileDiv = document.createElement('div');
            fileDiv.classList.add('file');

            const fileNameElement = document.createElement('h3');
            fileNameElement.textContent = fileName;

            const categoriesDiv = document.createElement('div');
            categoriesDiv.classList.add('categories');
            const categoryArray = categories.split(', ');
            categoryArray.forEach(category => {
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
}

function displayDuplicateFiles(duplicates) {
    duplicateFilesList.innerHTML = ''; // Clear previous data

    if (Object.keys(duplicates).length === 0) {
        duplicateFilesList.innerHTML = "<p>No duplicate files found.</p>";
    } else {
        // Iterate through the duplicates and display each
        for (const [fileName, count] of Object.entries(duplicates)) {
            const duplicateDiv = document.createElement('div');
            duplicateDiv.classList.add('duplicate-file');
            duplicateDiv.textContent = `${fileName} - Found ${count} times`;
            duplicateFilesList.appendChild(duplicateDiv);
        }
    }
}
