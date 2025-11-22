import json
import os
import time
import datetime
import hashlib
from openai import OpenAI

# Load Config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

TARGET_REPO = config['target_repo_path']
JOURNAL_REPO = config['journal_repo_path']
FILE_STATE_PATH = os.path.join(os.path.dirname(__file__), 'file_state.json')
API_KEY = config.get('api_key')
AI_PROVIDER = config.get('ai_provider', 'openai')
MODEL_NAME = config.get('model_name', 'gpt-4o')

# Extensions to watch
WATCH_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.css', '.html', '.json', '.md'}
IGNORE_DIRS = {'node_modules', 'dist', '.git', 'coverage', '.gemini'}

def get_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except (IOError, OSError):
        return None

def scan_files(root_dir):
    """Scan directory and return a dict of {filepath: hash}."""
    file_state = {}
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in WATCH_EXTENSIONS):
                filepath = os.path.join(root, file)
                file_hash = get_file_hash(filepath)
                if file_hash:
                    # Store relative path
                    rel_path = os.path.relpath(filepath, root_dir)
                    file_state[rel_path] = file_hash
    return file_state

def load_previous_state():
    if os.path.exists(FILE_STATE_PATH):
        with open(FILE_STATE_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(FILE_STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)

def detect_changes(current_state, previous_state):
    new_files = []
    modified_files = []
    deleted_files = []

    # Check for new and modified
    for filepath, current_hash in current_state.items():
        if filepath not in previous_state:
            new_files.append(filepath)
        elif previous_state[filepath] != current_hash:
            modified_files.append(filepath)
    
    # Check for deleted
    for filepath in previous_state:
        if filepath not in current_state:
            deleted_files.append(filepath)
            
    return new_files, modified_files, deleted_files

def get_diff_context(root_dir, modified_files, new_files):
    """Read content of changed files to provide context to LLM."""
    context = ""
    
    # Limit context size
    max_chars = 12000
    current_chars = 0
    
    for f in modified_files[:5]: # Limit to top 5 modified
        try:
            with open(os.path.join(root_dir, f), 'r') as file:
                content = file.read()
                context += f"\n--- MODIFIED: {f} ---\n"
                context += content[:2000] # Truncate large files
                current_chars += len(content[:2000])
        except Exception:
            pass
            
    for f in new_files[:5]:
        try:
            with open(os.path.join(root_dir, f), 'r') as file:
                content = file.read()
                context += f"\n--- NEW: {f} ---\n"
                context += content[:2000]
                current_chars += len(content[:2000])
        except Exception:
            pass
            
    if current_chars >= max_chars:
        context += "\n...[Remaining changes truncated]..."
        
    return context

def generate_entry_content(new_files, modified_files, deleted_files, context):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Summary stats
    stats = []
    if new_files: stats.append(f"{len(new_files)} new files")
    if modified_files: stats.append(f"{len(modified_files)} modified files")
    if deleted_files: stats.append(f"{len(deleted_files)} deleted files")
    stats_str = ", ".join(stats)
    
    file_list = "\n".join([f"- {f} (Modified)" for f in modified_files[:10]])
    if len(modified_files) > 10: file_list += f"\n- ...and {len(modified_files)-10} more"
    
    file_list += "\n" + "\n".join([f"- {f} (New)" for f in new_files[:10]])
    
    basic_content = f"""# Update: {stats_str}

**Date:** {datetime.datetime.now().strftime('%B %d, %Y')}
**Time:** {datetime.datetime.now().strftime('%H:%M')}

## Activity Log
{file_list}
"""

    if not API_KEY or API_KEY == "INSERT_API_KEY_HERE":
        print("No API Key found. Using basic template.")
        return f"Update: {stats_str}", basic_content

    # LLM Generation
    try:
        client = OpenAI(api_key=API_KEY)
        
        system_prompt = """You are an expert software engineer keeping a personal journal about your coding projects. 
        Your tone is authentic, slightly technical but accessible, and enthusiastic. 
        You are writing a journal entry based on the recent file changes provided.
        Focus on the "why" and "how" of the changes based on the code context.
        Do not be overly formal. Use emojis sparingly.
        Format the output in Markdown.
        Include a title in the response (first line, # Title).
        """
        
        user_prompt = f"""Here are the recent changes in my project '{os.path.basename(TARGET_REPO)}'.
        
        Stats: {stats_str}
        
        Files Changed:
        {file_list}
        
        Code Context (Snippets of changed files):
        {context}
        
        Write a journal entry summarizing this work.
        """
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        generated_text = response.choices[0].message.content
        
        # Extract title if present
        lines = generated_text.split('\n')
        title = f"Update: {stats_str}" # Default
        if lines[0].startswith('# '):
            title = lines[0].replace('# ', '').strip()
            
        return title, generated_text

    except Exception as e:
        print(f"LLM Generation failed: {e}")
        return f"Update: {stats_str}", basic_content

def update_entries_js(entry_id, title, filename):
    entries_js_path = os.path.join(JOURNAL_REPO, 'js', 'entries.js')
    
    with open(entries_js_path, 'r') as f:
        content = f.read()
    
    escaped_title = title.replace("'", "\\'")
    new_entry_obj = f"""    {{
        id: '{entry_id}',
        title: '{escaped_title}',
        date: '{datetime.datetime.now().strftime('%Y-%m-%d')}',
        excerpt: 'Automated update powered by AI.',
        tags: ['Update', 'AI-Generated'],
        file: 'journal/{filename}',
        image: 'https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=1000&auto=format&fit=crop'
    }},"""
    
    insert_pos = content.find('[') + 1
    new_content = content[:insert_pos] + '\n' + new_entry_obj + content[insert_pos:]
    
    with open(entries_js_path, 'w') as f:
        f.write(new_content)

def main():
    print(f"Scanning for changes in {TARGET_REPO}...")
    
    if not os.path.exists(TARGET_REPO):
        print(f"Error: Target repo {TARGET_REPO} does not exist.")
        return

    current_state = scan_files(TARGET_REPO)
    previous_state = load_previous_state()
    
    if not previous_state:
        print("First run. Establishing baseline file state.")
        save_state(current_state)
        return

    new_files, modified_files, deleted_files = detect_changes(current_state, previous_state)
    
    if not new_files and not modified_files and not deleted_files:
        print("No changes detected.")
        return

    print(f"Changes detected: {len(new_files)} new, {len(modified_files)} modified, {len(deleted_files)} deleted.")
    
    context = get_diff_context(TARGET_REPO, modified_files, new_files)
    title, content = generate_entry_content(new_files, modified_files, deleted_files, context)
    
    current_time = datetime.datetime.now().timestamp()
    filename = f"update-{int(current_time)}.md"
    filepath = os.path.join(JOURNAL_REPO, 'journal', filename)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    update_entries_js(f"update-{int(current_time)}", title, filename)
    save_state(current_state)
    
    print(f"Created new entry: {filename}")

if __name__ == "__main__":
    main()


