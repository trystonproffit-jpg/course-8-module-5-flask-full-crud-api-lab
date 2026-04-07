from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    title = data.get("title")

    # Create new ID (increment based on current max)
    new_id = max([event.id for event in events], default=0) + 1

    new_event = Event(new_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    title = data.get("title")

    for event in events:
        if event.id == event_id:
            event.title = title
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)