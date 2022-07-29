# TECo - Texto Em Contexto (Text in Context)
This system aims to, given a short-text input, adapt and select Portuguese expressions (e.g., proverbs and movie titles) in order to approximate them to the input, enhancing relatedness, originality and, possibly, funniness.

## Install
### Download & Install models
Files needed to put in folder 'models_db':
- To put in folder 'bert_pretrained_models', download <a href="https://github.com/google-research/bert">BERT MultiLingual Cased 'multi_cased_L-12_H-768_A-12'</a>
- To put in folder 'we_models', downloadable <a href="https://drive.google.com/drive/folders/1oCVCjoAED2DErrVCuk3yi0MFVvX3BO02?usp=sharing">here</a>

### Modify files from original repository
Change the following line in proverb_selector/file_manager.py `import pickle` by `from pickle5 import pickle`
## Build docker image

```
sh docker-build.sh
```

## Execute
```
docker run --rm -p 0.0.0.0:8866:8866 --name teco elg_teco:1.0
```
## Use

```
curl -X POST  http://0.0.0.0:8866/predict_json -H 'Content-Type: application/json' -d '{"type": "text", "content":"Bancos dizem que as condiçoes das linhas de crédito foram definidas pelo governo"}'
```



# Test
In the folder `test` you have the files for testing the API according to the ELG specifications.
It uses an API that acts as a proxy with your dockerized API that checks both the requests and the responses.
For this follow the instructions:
1) Configure the .env file with the data of the image and your API
2) Launch the test: `docker-compose up`
3) Make the requests, instead of to your API's endpoint, to the test's endpoint:
   ```
   curl -X POST  http://0.0.0.0:8866/processText/service -H 'Content-Type: application/json' -d '{"type": "text", "content":"Mourinho culpa-me por ter sido demitido do Chelsea. Esteve sempre contra mim"}'
   ```
4) If your request and the API's response is compliance with the ELG API, you will receive the response.
   1) If the request is incorrect: Probably you will don't have a response and the test tool will not show any message in logs.
   2) If the response is incorrect: You will see in the logs that the request is proxied to your API, that it answers, but the test tool does not accept that response. You must analyze the logs.


    
## Citations:
The original work of this tool is:
- Mendes, R., & Oliveira, H. G. (2020). TECo: Exploring Word Embeddings for Text Adaptation to a given Context. In ICCC (pp. 185-188).
- Mendes, R., & Oliveira, H. G. (2020, December). Amplifying the Range of News Stories with Creativity: Methods and their Evaluation, in Portuguese. In Proceedings of the 13th International Conference on Natural Language Generation (pp. 252-262).
- https://github.com/NLP-CISUC/TECo
