document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('journal-grid');
    const modal = document.getElementById('entry-modal');
    const modalBody = document.getElementById('modal-body');

    // Render Grid
    journalEntries.forEach(entry => {
        const card = document.createElement('div');
        card.className = 'entry-card';
        card.innerHTML = `
            <div class="card-image" style="background-image: url('${entry.image}')"></div>
            <div class="card-content">
                <div class="card-date">${formatDate(entry.date)}</div>
                <h2 class="card-title">${entry.title}</h2>
                <div class="card-tags">
                    ${entry.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <p class="card-excerpt">${entry.excerpt}</p>
                <a href="#" class="read-more" onclick="openEntry('${entry.file}', event)">Read Entry →</a>
            </div>
        `;
        grid.appendChild(card);
    });
});

// Format Date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Open Entry
async function openEntry(filePath, event) {
    if (event) event.preventDefault();

    const modal = document.getElementById('entry-modal');
    const modalBody = document.getElementById('modal-body');

    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error('Failed to load entry');

        const markdown = await response.text();
        modalBody.innerHTML = marked.parse(markdown);
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    } catch (error) {
        console.error(error);
        modalBody.innerHTML = '<p>Error loading entry. Please try again later.</p>';
        modal.classList.add('active');
    }
}

// Close Modal
function closeModal() {
    const modal = document.getElementById('entry-modal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Close on outside click
window.onclick = function (event) {
    const modal = document.getElementById('entry-modal');
    if (event.target == modal) {
        closeModal();
    }
}
