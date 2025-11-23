# AI Journal 🤖

A personal journal to document the experience of building with AI.

## 🌟 Features

-   **Visual Feed**: A beautiful grid layout to browse entries.
-   **Markdown Support**: Write entries in simple Markdown.
-   **Custom Theme**: Slate Blue & Minty Green aesthetic.
-   **Lightweight**: Built with Vanilla JS and CSS.

## 🚀 How to Use

### Adding a New Entry

1.  **Create a Markdown File**:
    -   Go to the `journal/` folder.
    -   Create a new file, e.g., `my-new-entry.md`.
    -   Write your content using standard Markdown.

2.  **Register the Entry**:
    -   Open `js/entries.js`.
    -   Add a new object to the `journalEntries` array:
        ```javascript
        {
            id: 'my-new-entry',
            title: 'My New Entry Title',
            date: '2025-11-23',
            excerpt: 'A short summary of what this entry is about.',
            tags: ['Learning', 'React'],
            file: 'journal/my-new-entry.md',
            image: 'URL_TO_IMAGE' // Or use a local path in assets/
        },
        ```

3.  **Push Changes**:
    -   Use GitHub Desktop to commit and push your changes.
    -   If using GitHub Pages, your site will update automatically!

## 🎨 Customization

Edit `css/styles.css` to change the variables at the top of the file if you want to tweak the colors.

```css
:root {
    --accent-mint: #81e6d9; /* Change me! */
}
```

```

## 🤖 Automation

I've included a script to automatically update this journal based on your coding activity in other projects.

### Setup
1.  Open `scripts/config.json` and check the `target_repo_path` (it defaults to `../rpg_fitness_app`).
2.  (Optional) Add an API key if you want AI-generated summaries.

### Running the Watcher
To start the 15-minute background check, run:

```bash
./scripts/run_watch.sh
```

Keep this terminal window open to keep the watcher running.

## 🚀 Deployment & Daily Workflow

### Initial Setup
1.  Open **GitHub Desktop**.
2.  Go to **File** > **Add Local Repository**.
3.  Select this folder: `/Users/gabrielyeager/Applications/github_repo_ai_journal`.
4.  Click **Publish repository** to send it to GitHub.
5.  **Enable GitHub Pages**:
    -   Go to your new repository on GitHub.com.
    -   Settings > Pages.
    -   Select `main` branch and `/ (root)` folder.
    -   Save! Your journal is now live.

### Daily Routine (Agent-Assisted)
1.  **Code**: Work on your projects as usual.
2.  **Ask**: When you're ready for an update, just tell Antigravity: *"Check for updates and write a journal entry."*
3.  **Review**: I will generate a high-quality, social-media style post for you.
4.  **Push**: Open GitHub Desktop, commit, and push!

Enjoy building!
