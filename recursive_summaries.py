import os
import json
import openai
from time import time, sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def get_next_chunk(filepath, name):
    numbers = filepath.replace('.txt', '').replace(name, '')
    number = int(numbers) + 1
    filename = f"{name}{number:04d}.txt"
    return open_file(f"chunks/{filename}")


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0,
                    stop=['<<END>>']):
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
        summaries = [i for i in os.listdir('summaries/') if name in i]
        outline = open_file('outlines/%s' % book)
        summary_chunks = []
        for summary in summaries:
            summary_chunks.append(open_file(f'summaries/{summary}'))  # append the summary chunk to the list
            if sum(len(chunk) for chunk in summary_chunks) > 1500:  # if the total length is too long, summarize
                print('summarizing the summaries...')
                prompt = open_file('prompt_summary.txt').replace('<<CHUNK>>', ' '.join(summary_chunks))
                prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
                summary_chunks = [gpt3_completion(prompt)]  # start a new list with the summarized chunk
            last_chunk = open_file(f'chunks/{summary}')
            next_chunk = get_next_chunk(summary, name)
            prompt = open_file('prompt_full.txt').replace('<<OUTLINE>>', outline).replace('<<SUMMARY>>',
                                                                                           ' '.join(
                                                                                               summary_chunks)).replace(
                '<<CHUNK>>', last_chunk)
            print(summary, len(prompt) + len(next_chunk))
            save_file(prompt, f'prompts/{summary}')
            save_file(next_chunk, f'completions/{summary}')
