# Lessons Learned: Automating the Workflow

**Date:** November 22, 2025  
**Category:** Engineering ⚙️

## The Problem with Manual Journals
Consistency is the enemy of documentation. When you're in the "flow" of coding, the last thing you want to do is stop and write a journal entry about what you just did.

## The Solution: The "Watcher" Pattern
To solve this, we built a background automation system.

### How it Works
1.  **The Watcher**: A simple shell script (`run_watch.sh`) that wakes up every 15 minutes.
2.  **The Brain**: A Python script (`auto_journal.py`) that checks the `git log` of my active project (`rpg_fitness_app`).
3.  **The Output**: If changes are detected, it automatically generates a new Markdown entry and pushes it to this journal.

### Key Takeaways
-   **Automation frees up mental energy**: I can focus on building, knowing the history is being recorded.
-   **Git as a Source of Truth**: Using commit logs ensures the journal is always accurate to the code.
-   **Next Steps**: Connecting an LLM (Large Language Model) to write *better* summaries than just commit messages.

> "The best documentation is the documentation you don't have to write."
