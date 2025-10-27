class AIAgentSimulator:
    def __init__(self):
        self.categories = {
            "greeting": ["hello", "hi", "hey"],
            "goodbye": ["bye", "goodbye", "see you"],
            "thanks": ["thank you", "thanks"],
            "questions": ["what", "how", "why", "when", "who"]
        }

    def categorize_input(self, user_input):
        """Categorizes the user input into predefined categories."""
        for category, keywords in self.categories.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return category
        return "unknown"

    def generate_response(self, category):
        """Generates a response based on the categorized input."""
        responses = {
            "greeting": "Hello! How can I assist you today?",
            "goodbye": "Goodbye! Have a great day!",
            "thanks": "You're welcome! If you have any more questions, feel free to ask.",
            "questions": "That's an interesting question! Can you elaborate?",
            "unknown": "I'm sorry, I didn't quite understand that."
        }
        return responses.get(category, responses["unknown"])

    def handle_input(self, user_input):
        """Handles user input by categorizing it and generating a response."""
        category = self.categorize_input(user_input)
        response = self.generate_response(category)
        return response
