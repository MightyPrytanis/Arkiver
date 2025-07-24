
import json
import re
from collections import defaultdict

def load_keywords():
    """Load keywords and their associated projects from the text file."""
    with open('attached_assets/Projexts and Keywords_1753336389930.txt', 'r') as f:
        content = f.read()
    
    # Parse the JSON-like structure
    keywords_data = eval(content)  # Note: eval is used here for simplicity with the given format
    
    # Create a mapping from keywords to projects
    keyword_to_project = {}
    for project, keywords in keywords_data.items():
        for keyword in keywords:
            keyword_to_project[keyword.lower()] = project
    
    return keyword_to_project

def extract_text_from_message(message_data):
    """Extract text content from a message."""
    if not message_data or not message_data.get('message'):
        return ""
    
    content = message_data['message'].get('content', {})
    if content.get('content_type') == 'text':
        parts = content.get('parts', [])
        return ' '.join(str(part) for part in parts if part)
    
    return ""

def search_keywords_in_text(text, keyword_to_project):
    """Search for keywords in text and return matching projects."""
    text_lower = text.lower()
    found_projects = set()
    
    for keyword, project in keyword_to_project.items():
        if keyword in text_lower:
            found_projects.add(project)
    
    return found_projects

def parse_conversations():
    """Parse the conversations JSON file and categorize by keywords."""
    # Load keywords
    keyword_to_project = load_keywords()
    
    # Load conversations
    with open('attached_assets/reformatted_conversations_1753336339888.json', 'r') as f:
        conversations = json.load(f)
    
    # Results storage
    categorized_conversations = defaultdict(list)
    uncategorized_conversations = []
    
    print(f"Loaded {len(keyword_to_project)} keywords across {len(set(keyword_to_project.values()))} projects")
    print(f"Processing {len(conversations)} conversations...\n")
    
    for conversation in conversations:
        title = conversation.get('title', 'Untitled')
        mapping = conversation.get('mapping', {})
        
        # Extract all text from the conversation
        all_text = []
        for node_id, node_data in mapping.items():
            text = extract_text_from_message(node_data)
            if text.strip():
                all_text.append(text)
        
        conversation_text = ' '.join(all_text)
        
        # Search for keywords
        found_projects = search_keywords_in_text(conversation_text, keyword_to_project)
        
        conversation_info = {
            'title': title,
            'create_time': conversation.get('create_time'),
            'update_time': conversation.get('update_time'),
            'text_preview': conversation_text[:200] + '...' if len(conversation_text) > 200 else conversation_text
        }
        
        if found_projects:
            for project in found_projects:
                categorized_conversations[project].append(conversation_info)
        else:
            uncategorized_conversations.append(conversation_info)
    
    # Print results
    print("=== CATEGORIZED CONVERSATIONS ===")
    for project in sorted(categorized_conversations.keys()):
        conversations_list = categorized_conversations[project]
        print(f"\n{project.upper()} ({len(conversations_list)} conversations):")
        for conv in conversations_list:
            print(f"  - {conv['title']}")
            if conv['text_preview'].strip():
                print(f"    Preview: {conv['text_preview']}")
    
    print(f"\n=== UNCATEGORIZED CONVERSATIONS ===")
    print(f"Found {len(uncategorized_conversations)} conversations without matching keywords:")
    for conv in uncategorized_conversations[:10]:  # Show first 10
        print(f"  - {conv['title']}")
    
    if len(uncategorized_conversations) > 10:
        print(f"  ... and {len(uncategorized_conversations) - 10} more")
    
    # Summary
    total_categorized = sum(len(convs) for convs in categorized_conversations.values())
    print(f"\n=== SUMMARY ===")
    print(f"Total conversations: {len(conversations)}")
    print(f"Categorized: {total_categorized}")
    print(f"Uncategorized: {len(uncategorized_conversations)}")
    
    return categorized_conversations, uncategorized_conversations

if __name__ == "__main__":
    try:
        categorized, uncategorized = parse_conversations()
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error: {e}")
