from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline


class RecommenderTrigger:
    def __init__(self):
        self.modelname = "bert-large-uncased-whole-word-masking-finetuned-squad"
        self.model = BertForQuestionAnswering.from_pretrained(self.modelname)
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelname)
        self.nlp = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer)
        self.context = [
            "hungry leh what to eat", 
            "hungry leh anything to eat", 
            "ah you got any food to intro", 
            "you feel like eating" ,
            "cuisine you want", 
            "can reco any food",
            "can intro any food place",
            "can recommend any food place",
            "makan hungry sia" 
        ]
        # self.context = "hungry leh what to eat anything to eat you got any food to intro feel like eating reco any food place recommend makan hungry sia"
# context = "Ever come across a time when you and your friend cannot decide on what to eat? Introducing our food recommender bot that provides recommendation of food by filtering the top 5 food places based on the cuisine selected and the location users provided. This would allow undecisive hungry users to pick a recommended place based off their cuisine. So no more indecisive hungry people anymore, use the bot now."

    def check_recommend_context(self, question):
        # question = "what to eat ah?"

        for c in self.context:
            nlp_result = self.nlp({
                'question': question,
                'context': c
            })
            if(nlp_result["score"] > 0.6):
                break

        # nlp_result = self.nlp({
        #     'question': question,
        #     'context': self.context
        # })

        print(nlp_result["score"])

        return nlp_result["score"]
