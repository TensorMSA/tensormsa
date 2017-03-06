from chatterbot import ChatBot
#pip install chatterbot

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    silence_performance_warning=True
)

def chatbot_response():
    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")
    input_string = "Hello, how are you today?"
    # Get a response to an input statement
    print(input_string)
    print(chatbot.get_response(input_string))
    input_string = "Have you heard the news?"
    print(input_string)
    print(chatbot.get_response(input_string))
    input_string = "Can I ask you a question?"
    print(input_string)
    print(chatbot.get_response(input_string))

chatbot_response()