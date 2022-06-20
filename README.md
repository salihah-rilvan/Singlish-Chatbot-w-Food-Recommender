# Potato Master 

## About The Project

We aim to create a Telegram chatbot which can communicate in a way which is as human-like as possible and with the ability to talk in Singlish as well as most SMU students are Singaporeans. Also, together with the integration of  the food recommendation function which will be utilised if the user wants some ideas of what to eat and where to find them. 


## Installation

Install the dependencies: pip install -r requirements.txt

## Data Sources

Under the ./potato-master directory, we have some data sources<br>
./data/*.geojson: they are the files for SG master planning areas mapping.<br>
./data/cuisines*.txt: for the cuisine options generation.<br>
./data/restaurants.csv: the file containing all restaurants’ information.<br>
./data/{train, validate}_combine_df.csv: sampled training files from combined sources.<br>
./data/{train, validate}_df.csv: sampled training files from NUS SMS corpus only.<br>
If you want to see the full datasets, download and put them in the ./data directory<br>
Reddit Singapore: https://drive.google.com/drive/folders/1-DoqlzULEmQdC5VaEwL16pglRhWiOZAu?usp=sharing<br>
HardwareZone: https://drive.google.com/drive/folders/1fFbF83DA64tWSC2YRIKjqLh5LDTcuqtC?usp=sharing

## Finetuned Models

- DialoGPT on NUS SMS: https://drive.google.com/drive/folders/1-bavGb5pYdHOrQ8kAQQGdXydgRRqFIWm?usp=sharing
- DialoGPT on combined datasets: https://drive.google.com/drive/folders/1-0zDz3RogUoukJkeWekVeWGTK9ZyNgSO?usp=sharing
- Blenderbot on NUS SMS: https://drive.google.com/drive/folders/1jYrEl-bodMcNygWtJF0g_hhON5mkmuDf?usp=sharing
- Blenderbot on combined datasets: https://drive.google.com/drive/folders/17sWgvXctnDGBTU91TN2ob0XW_fthKZXR?usp=sharing

## Process Files

./potato-master/data_scrape_preprocess: the directory contains the notebooks to scrape the Singlish conversations from HardwareZone and Reddit Singapore.<br>
./potato-master/data_scrape_preprocess/data_combine.ipynb: combine data from different sources and do sampling.<br>
./potato-master/fine-tune: the directory contains the notebooks to fine-tune the Blenderbot and DialoGPT. After the process, put the checkpoint directory and change the model path in the bot.py.<br>
./potato-master/bot.py: Running this code will activate the bot in telegram.


## Reference for Fine-Tuning
https://github.com/chuachinhon/practical_nlp/tree/master/notebooks



