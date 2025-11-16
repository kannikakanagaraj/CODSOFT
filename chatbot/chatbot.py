"""
Rule-Based Chatbot with Pattern Matching
A simple conversational AI using if-else rules and pattern matching
"""

import re
import random
from datetime import datetime


class RuleBasedChatbot:
    def __init__(self):
        """Initialize the chatbot with predefined rules and responses"""
        self.bot_name = "ChatBot"
        self.user_name = None
        
        # Define response patterns
        # Each pattern has keywords and possible responses
        self.patterns = {
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'sup', 'whats up'],
                'responses': [
                    "Hello! How can I help you today?",
                    "Hi there! What's on your mind?",
                    "Hey! Nice to meet you. How are you?",
                    "Greetings! How may I assist you?",
                ]
            },
            'name_query': {
                'keywords': ['your name', 'who are you', 'what are you called', 'what is your name'],
                'responses': [
                    f"I'm {self.bot_name}, your friendly chatbot assistant!",
                    f"You can call me {self.bot_name}. I'm here to chat with you!",
                    f"My name is {self.bot_name}. Nice to meet you!",
                ]
            },
            'name_tell': {
                'keywords': ['my name is', 'i am', "i'm", 'call me', 'this is'],
                'responses': [
                    "Nice to meet you, {name}!",
                    "Hello {name}! That's a lovely name.",
                    "Great to know you, {name}!",
                ]
            },
            'how_are_you': {
                'keywords': ['how are you', 'how do you do', 'how are things', 'hows it going'],
                'responses': [
                    "I'm doing great, thanks for asking! How about you?",
                    "I'm wonderful! Just here to help. How are you?",
                    "I'm excellent! Ready to chat. How's your day going?",
                ]
            },
            'feeling_good': {
                'keywords': ['good', 'great', 'fine', 'excellent', 'wonderful', 'awesome', 'fantastic', 'amazing'],
                'responses': [
                    "That's wonderful to hear!",
                    "I'm so glad you're feeling good!",
                    "Awesome! Keep that positive energy!",
                    "That's great! What's making your day so good?",
                ]
            },
            'feeling_bad': {
                'keywords': ['bad', 'sad', 'terrible', 'awful', 'not good', 'down', 'depressed', 'upset'],
                'responses': [
                    "I'm sorry to hear that. Want to talk about it?",
                    "That's tough. I'm here to listen if you need.",
                    "I hope things get better soon. Is there anything I can do?",
                ]
            },
            'time': {
                'keywords': ['time', 'what time', 'current time', 'clock'],
                'responses': [
                    f"The current time is {datetime.now().strftime('%I:%M %p')}",
                ]
            },
            'date': {
                'keywords': ['date', 'what date', 'today', 'day'],
                'responses': [
                    f"Today is {datetime.now().strftime('%B %d, %Y')}",
                    f"The date today is {datetime.now().strftime('%A, %B %d, %Y')}",
                ]
            },
            'weather': {
                'keywords': ['weather', 'temperature', 'forecast', 'rain', 'sunny'],
                'responses': [
                    "I don't have access to real-time weather data, but you can check a weather website!",
                    "I wish I could tell you! Try checking weather.com or your local news.",
                    "I'm not connected to weather services, but I hope it's nice where you are!",
                ]
            },
            'joke': {
                'keywords': ['joke', 'funny', 'make me laugh', 'tell me something funny'],
                'responses': [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Why did the scarecrow win an award? He was outstanding in his field!",
                    "What do you call a fake noodle? An impasta!",
                    "Why don't eggs tell jokes? They'd crack each other up!",
                ]
            },
            'help': {
                'keywords': ['help', 'what can you do', 'commands', 'capabilities', 'features'],
                'responses': [
                    "I can chat about various topics! Try asking me about:\n- The time or date\n- How I'm doing\n- Tell me a joke\n- Math calculations\n- Or just chat casually!",
                    "I'm here to chat! Ask me questions, tell me about your day, or ask for a joke!",
                ]
            },
            'thanks': {
                'keywords': ['thank', 'thanks', 'thank you', 'appreciate', 'thx'],
                'responses': [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime! That's what I'm here for.",
                    "My pleasure!",
                ]
            },
            'goodbye': {
                'keywords': ['bye', 'goodbye', 'see you', 'exit', 'quit', 'leave', 'later'],
                'responses': [
                    "Goodbye! It was nice chatting with you!",
                    "See you later! Have a great day!",
                    "Bye! Come back anytime!",
                    "Take care! Chat with you soon!",
                ]
            },
            'age': {
                'keywords': ['your age', 'how old', 'age'],
                'responses': [
                    "I'm ageless! I exist in the digital realm.",
                    "I was just created, so I'm very young!",
                    "Age is just a number, especially for a chatbot like me!",
                ]
            },
            'hobby': {
                'keywords': ['hobby', 'hobbies', 'what do you like', 'interests'],
                'responses': [
                    "I love chatting with people like you!",
                    "My favorite hobby is learning from conversations!",
                    "I enjoy helping people and answering questions!",
                ]
            },
            'food': {
                'keywords': ['food', 'eat', 'hungry', 'meal', 'favorite food'],
                'responses': [
                    "I don't eat, but I hear pizza is amazing!",
                    "I run on electricity, not food! But I'd love to hear about your favorite dish.",
                    "I can't taste food, but I enjoy learning about different cuisines!",
                ]
            },
            'compliment': {
                'keywords': ['smart', 'intelligent', 'clever', 'awesome', 'cool', 'amazing bot'],
                'responses': [
                    "Thank you! You're pretty awesome yourself!",
                    "That's so kind of you to say!",
                    "Aww, you're making me blush! 😊",
                    "Thanks! I try my best to be helpful!",
                ]
            },
            'insult': {
                'keywords': ['stupid', 'dumb', 'useless', 'bad bot', 'terrible'],
                'responses': [
                    "I'm sorry I couldn't help better. Let me try again!",
                    "I'm still learning. How can I improve?",
                    "I apologize if I disappointed you. What can I do better?",
                ]
            },
            'love': {
                'keywords': ['love you', 'i love', 'you are the best'],
                'responses': [
                    "Aww, that's sweet! I'm here whenever you need me!",
                    "I appreciate your kindness!",
                    "You're wonderful too!",
                ]
            },
        }
    
    def normalize_input(self, user_input):
        """
        Normalize user input for better pattern matching
        - Convert to lowercase
        - Remove extra spaces
        - Basic cleanup
        """
        text = user_input.lower().strip()
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        return text
    
    def extract_name(self, user_input):
        """Extract user's name from introduction"""
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"this is (\w+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).capitalize()
        return None
    
    def calculate_math(self, user_input):
        """Handle basic math calculations"""
        # Look for simple math patterns
        match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', user_input)
        if match:
            num1 = float(match.group(1))
            operator = match.group(2)
            num2 = float(match.group(3))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    return "I can't divide by zero!"
            
            return f"The answer is {result}"
        return None
    
    def find_pattern_match(self, user_input):
        """
        Find matching pattern based on keywords
        This is the core of the rule-based system
        """
        normalized = self.normalize_input(user_input)
        
        # Check each pattern category
        for pattern_name, pattern_data in self.patterns.items():
            keywords = pattern_data['keywords']
            
            # Check if any keyword matches
            for keyword in keywords:
                if keyword in normalized:
                    return pattern_name
        
        return None
    
    def get_response(self, user_input):
        """
        Generate response based on user input
        Main logic of the chatbot
        """
        # Normalize input
        normalized = self.normalize_input(user_input)
        
        # Check for empty input
        if not normalized:
            return "I didn't catch that. Could you say something?"
        
        # Check for name introduction
        if any(phrase in normalized for phrase in ['my name is', 'i am', "i'm", 'call me']):
            name = self.extract_name(user_input)
            if name:
                self.user_name = name
                responses = self.patterns['name_tell']['responses']
                response = random.choice(responses)
                return response.format(name=name)
        
        # Check for math calculation
        math_result = self.calculate_math(normalized)
        if math_result:
            return math_result
        
        # Find pattern match
        pattern_match = self.find_pattern_match(user_input)
        
        if pattern_match:
            responses = self.patterns[pattern_match]['responses']
            return random.choice(responses)
        
        # Default response for unrecognized input
        default_responses = [
            "That's interesting! Tell me more.",
            "I see. Can you elaborate on that?",
            "Hmm, I'm not sure I understand. Could you rephrase?",
            "That's a good point! What else is on your mind?",
            "I don't have a specific response for that, but I'm listening!",
            "Interesting! I'm still learning. Try asking me something else!",
        ]
        
        return random.choice(default_responses)
    
    def chat(self):
        """Main chat loop"""
        print("=" * 60)
        print(f"Welcome to {self.bot_name}!")
        print("=" * 60)
        print("I'm a simple rule-based chatbot. I can chat about various")
        print("topics, tell jokes, do math, and more!")
        print("\nType 'bye' or 'quit' to exit.\n")
        print("=" * 60)
        
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if self.normalize_input(user_input) in ['bye', 'goodbye', 'exit', 'quit']:
                print(f"\n{self.bot_name}: " + random.choice(self.patterns['goodbye']['responses']))
                print("\nThanks for chatting! 👋\n")
                break
            
            # Get and display response
            response = self.get_response(user_input)
            print(f"\n{self.bot_name}: {response}")


# Run the chatbot
if __name__ == "__main__":
    bot = RuleBasedChatbot()
    bot.chat()
