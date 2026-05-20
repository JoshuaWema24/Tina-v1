from memory.long_term import save_memory, get_memories


class MemoryManager:

    def __init__(self):
        pass

    # =====================================
    # STORE MEMORY
    # =====================================
    def remember(
        self,
        memory,
        category="general",
        importance=5
    ):
        """
        Save memory into long-term storage.
        """

        save_memory(
            memory=memory,
            category=category,
            importance=importance
        )

    # =====================================
    # RETRIEVE MEMORIES
    # =====================================
    def recall(self, limit=10):
        """
        Retrieve recent memories.
        """

        return get_memories(limit=limit)

    # =====================================
    # SIMPLE MEMORY DETECTION
    # =====================================
    def should_remember(self, text):
        """
        Determines whether something
        is important enough to remember.
        """

        keywords = [
            "exam",
            "meeting",
            "birthday",
            "study",
            "project",
            "walk",
            "appointment",
            "important",
            "remind",
            "tomorrow",
            "next week"
        ]

        text_lower = text.lower()

        return any(
            keyword in text_lower
            for keyword in keywords
        )

    # =====================================
    # AUTO PROCESS MEMORY
    # =====================================
    def process_input(self, user_input):
        """
        Automatically decides whether
        to store the user input.
        """

        if self.should_remember(user_input):

            self.remember(
                memory=user_input,
                category="personal",
                importance=7
            )

            return True

        return False