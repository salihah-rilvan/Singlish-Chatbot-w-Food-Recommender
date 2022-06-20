from transformers import (
    BlenderbotSmallForConditionalGeneration,
    BlenderbotSmallTokenizer,
)
import torch

class ChatModel:
    def __init__(self, model_path):
        self.tokenizer = BlenderbotSmallTokenizer.from_pretrained(model_path)
        self.model = BlenderbotSmallForConditionalGeneration.from_pretrained(model_path)
        self.chat_history_ids = None
        self.max_len = 1024    #self.tokenizer.model_max_length
        self.contexts = []

    def generate_response(self, user_input):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        # new_user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        self.contexts.append(user_input)
        # while(len(self.contexts) > 7):
        #     self.contexts.pop(0)        
    
        # input_ids = []
        # attention_masks = []
        # for text in self.contexts:
        #     inputs = self.tokenizer([text], return_tensors='pt')
        #     input_ids.append(inputs['input_ids'])
        #     attention_masks.append(inputs['attention_mask'])

        # print(input_ids)
        # print(attention_masks)

        # input_ids = torch.cat(input_ids, dim = 0)
        # attention_masks = torch.cat(attention_masks, dim = 0)

        # print(input_ids)
        # print(attention_masks)


        # reply_ids = self.model.generate(input_ids = input_ids, max_length=1024, attention_mask = attention_masks)

        # response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

    

        ##########

        bot_input_ids = []
        
        length = 0
        for text in self.contexts:
            # self.tokenizer.eos_token
            input_ids = self.tokenizer.encode(text, return_tensors='pt')

            length += input_ids.shape[1]
            bot_input_ids.append(input_ids)
        if(length > 900):
            bot_input_ids.pop(0)
            self.contexts.pop(0)
        bot_input_ids = torch.cat(bot_input_ids, dim=1)

        print('botinputids:', bot_input_ids)

        # append the new user input tokens to the chat history
        # bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if isinstance(self.chat_history_ids, torch.Tensor) else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
    
        chat_history_ids = self.model.generate(
            bot_input_ids, max_length=self.max_len,
            pad_token_id=self.tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=0.8
        )

        print('chathistory:', chat_history_ids)
        response = self.tokenizer.batch_decode(chat_history_ids, skip_special_tokens=True)[0]
        
        # self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        self.contexts.append(response)

    ##############
        return response

if __name__ == "__main__":
    cm = ChatModel(model_path="./pytorch_model_v2")

    while True:
        text = input(">:")
        print(cm.generate_response(text))
    
    # print(cm.generate_response("Eh they jio me go Jurong. come lah"))
    # print(cm.generate_response("but i need to go Jurong first. you are not coming?"))