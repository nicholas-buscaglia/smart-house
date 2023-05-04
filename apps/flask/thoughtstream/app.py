from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from enum import Enum
import os
mongo_url = os.environ.get('MYMONGO')

app = Flask(__thoughtstream__)
client = MongoClient(mongo_url)
db = client.thoughtstream
collection = db.thoughts

class Categories(Enum):
    THOUGHT = 'Thought'
    IDEA = 'Idea'
    MEMORY = 'Memory'
    TASK = 'Task'
    REFLECTION = 'Reflection'

@app.route('/thoughts', methods=['POST'])
def create_thought_route():
    data = request.get_json()
    text = data.get('text', None)
    audiouri = data.get('audioUri', None)
    tags = data.get('tags', None)
    category = data.get('category', None)
    title = data.get('title', None)
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    create_thought(text, audiouri, tags, category, title)
    return jsonify({'success': True}), 200

@app.route('/thoughts', methods=['GET'])
def get_thoughts_route():
    thoughts = get_thoughts()
    return jsonify(thoughts), 200

@app.route('/thoughts/<refid>', methods=['PATCH'])
def update_thought_route(refid):
    data = request.get_json()
    text = data.get('text', None)
    audiouri = data.get('audioUri', None)
    tags = data.get('tags', None)
    category = data.get('category', None)
    title = data.get('title', None)
    iscomplete = data.get('isComplete', None)
    isarchived = data.get('isArchived', None)
    chatthreads = data.get('chatThreads', None)
    if not any([text, audiouri, tags, category, title, iscomplete, isarchived, chatthreads]):
        return jsonify({'error': 'At least one field is required'}), 400
    update_thought(refid, text, audiouri, tags, category, title, iscomplete, isarchived, chatthreads)
    return jsonify({'success': True}), 200

@app.route('/thoughts/<refid>/chat', methods=['POST'])
def add_chat_thread_route(refid):
    data = request.get_json()
    role = data.get('role')
    content = data.get('content')
    if not role or not content:
        return jsonify({'error': 'Role and content are required'}), 400
    add_chat_thread(refid, role, content)
    return jsonify({'success': True}), 200

def create_thought(text, audiouri, tags, category, title):
    thought = {
        "refId": str(collection.count_documents({}) + 1),
        "text": text,
        "audioUri": audiouri,
        "tags": tags,
        "category": category,
        "title": title,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": None,
        "isComplete": False,
        "isArchived": False,
        "chatThreads": {}
    }
    result = collection.insert_one(thought)
    print("Created thought with ID:", result.inserted_id)

#create_thought("This is a test thought", Categories.THOUGHT.value)

def get_thoughts():
    thoughts = collection.find({"isArchived": False})
    return list(thoughts)

def update_thought(refid, text=None, audiouri=None, tags=None, category=None, title=None,
                   iscomplete=None, isarchived=None, chatthreads=None):
    update_dict = {}
    if text is not None:
        update_dict["text"] = text
    if audiouri is not None:
        update_dict["audioUri"] = audiouri
    if tags is not None:
        update_dict["tags"] = tags
    if category is not None:
        update_dict["category"] = category
    if title is not None:
        update_dict["title"] = title
    if iscomplete is not None:
        update_dict["isComplete"] = iscomplete
    if isarchived is not None:
        update_dict["isArchived"] = isarchived
    if chatthreads is not None:
        update_dict["chatThreads"] = chatthreads
    now = datetime.utcnow().isoformat()
    update_dict["updatedAt"] = now
    result = collection.update_one(
        {"refId": refid},
        {"$set": update_dict}
    )
    if result.modified_count == 1:
        print(f"Updated thought with ID: {refid}")
    else:
        print(f"Failed to update thought with ID: {refid}")

def add_chat_thread(refId, role, content):
    thought = collection.find_one({"refId": refId})
    if thought is None:
        print("Thought with refId", refId, "does not exist")
        return
    chat_threads = thought.get("chatThreads", [])
    new_chat_thread = {
        "refId": str(len(chat_threads) + 1),
        "role": role,
        "content": content,
        "createdAt": datetime.utcnow().isoformat()
    }
    chat_threads.append(new_chat_thread)
    result = collection.update_one({"refId": refId},
                                   {"$set": {"chatThreads": chat_threads, "updatedAt": datetime.utcnow()}})
    if result.modified_count > 0:
        print("Chat thread added to thought with refId:", refId)
    else:
        print("Failed to add chat thread to thought with refId:", refId)
