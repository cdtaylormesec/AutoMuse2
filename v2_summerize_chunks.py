import os
import openai
from time import time,sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def recursive_summarize(text, max_length):
    if len(text) <= max_length:
        return text

    # Summarize the text
    prompt = open_file('prompt_summary.txt').replace('<<CHUNK>>', text)
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
    summary = gpt3_completion(prompt)

    # Recursively summarize if the summary is still too long
    return recursive_summarize(summary, max_length)



def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=500, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    books = os.listdir('books/')
    for book in books:
        name = book.replace('.txt', '')
        chunks = [i for i in os.listdir('chunks/') if name in i]
        count = 0
        for chunk in chunks:
            count += 1
            text = open_file('chunks/%s' % chunk)
            text = text.encode(encoding='ASCII', errors='ignore').decode()

            # Replace this line with the recursive_summarize function
            summary = recursive_summarize(text, max_length=1000)  # You can adjust the max_length as needed

            print(name, chunk, summary)
            save_file(summary, 'summaries/%s' % chunk)
            if count >= 40:
                break
