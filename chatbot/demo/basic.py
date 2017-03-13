from chatbot.renponse.response_generator import ResponseGenerator
from chatbot.contexanalyzer.sentence_classifier import SentenceClassifier
from chatbot.decisionmaker.make_decision import MakeDecision

print('Start Chat Bot!')
question = input('Q: ')

answer = SentenceClassifier().classify_domain(question)

print('Bot: {}'.format(MakeDecision().make_response()))