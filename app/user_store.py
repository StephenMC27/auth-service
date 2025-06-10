from typing import Dict

# Stores user objects as values with UUIDs as keys
user_store: Dict[str, dict] = {}

# Index UUIDs - key: email, value: UUID
email_to_user_id: Dict[str, str] = {}
