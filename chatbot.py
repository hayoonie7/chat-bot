from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement

chatbot = ChatBot("TalkLeauge")

trainer = ListTrainer(chatbot)
trainer.train([
    "Good job!",
    "Nice try",
])
trainer.train([
    "GG EZ gitgud",
    "No, I'm the pot below the plant!",
])


print(f"🪴 {chatbot.get_response("")}")