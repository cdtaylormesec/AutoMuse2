import requests
import openai
from pprint import pprint

with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    pprint(resp)
    return resp

def file_list():
    resp = openai.File.list()
    pprint(resp)

def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    pprint(resp.json())

def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    pprint(resp.json())

def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)    
    pprint(resp.json())

def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)    
    pprint(resp.json())

# Upload the training file
resp = file_upload('novel.jsonl')

# Fine-tune the model with the training data
finetune_model(resp['id'], 'davinci-buddy-creative-writing-001', 'davinci')

# List all fine-tuned models
finetune_list()

# Cancel a fine-tuning job
# openai.FineTune.cancel("ft-2ZxHjUVe5DpqK2EsYyA0YtKz")
