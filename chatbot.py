from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("LeagueBot")

trainer = ListTrainer(chatbot)
trainer.train([
    "Hi",
    "Welcome, friend 🤗",
])
trainer.train([
    "Are you a plant?",
    "No, I'm the pot below the plant!",
])


print(f"🪴 {chatbot.get_response("")}")