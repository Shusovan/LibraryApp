def notify_librarian(user_id, email):
    """
    Simulates sending a notification to the librarian.
    In real-world apps, this can be replaced with WebSockets, Email, or a Notification Service.
    """
    print(f"🔔 Notification: A new user ({email}) is waiting for approval. User ID: {user_id}")
