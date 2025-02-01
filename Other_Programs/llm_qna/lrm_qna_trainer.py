
import os
import re
import time
import json
import torch
import random

from halo import Halo

from rich import print

from transformers import pipeline

spinner = Halo(text='Loading', spinner='dots', color='green')

model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

print(f"Loading `{model}`...")
pipe = pipeline("text-generation", model, torch_dtype=torch.bfloat16, device_map="auto")
print(f"Loaded `{model}`")

system_prompt = "Please keep messsages (to 15 words or less) and thinking short to save tokens."
system_message = {"role": "system", "content": system_prompt}
demo_user_message = {"role": "user", "content": "Hey, can you tell me any fun things to do in New York?"}

questions = []
answers = []

json_output = {}

with open(os.path.join("questions.txt"), 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()

        if line:
            spinner.start(text=f"Updating questions list... `{line}`")
            questions.append(line)

spinner.succeed(text=f"Updating questions list...")

random.shuffle(questions)

for i, question in enumerate(questions):
    chat = [system_message]
    user_message = {"role": "user", "content": question}

    start_time = time.time()
    
    spinner.start(text=f"LRM Thinking about: `{question}`...")
    chat.append(user_message)

    while True:
        try:
            response = pipe(chat, max_new_tokens=1024)

            full_response = response[0]['generated_text']  # type: ignore
            thinking_str = ""
            output_str = ""

            for item in full_response:
                if item['role'] == 'assistant':  # type: ignore
                    content = item['content']  # type: ignore
                    
                    thinking_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL) # type: ignore
                    if thinking_match:
                        thinking_str = thinking_match.group(1).strip()
                        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip() # type: ignore
                        output_str = content
            
            if len(thinking_str) < 1:
                raise Exception("\nModel failed to reply")
            
            if len(output_str) < 1:
                raise Exception("\nModel failed to reply")

            break
        except Exception as ERROR:
            print(str(ERROR))

    end_time = time.time()
    time_taken = end_time - start_time
    spinner.succeed(text=f"LRM done with: `{question}`! Took {time_taken:.2f} seconds")

    print(f"\nLRM's Thinking: [italic blue]{thinking_str}[/italic blue]\n")
    print(f"Question: [green]`{question}`[/green]\n")
    print(f"LRM's Output: [red]{output_str}[/red]\n")

    print("For the [green]question[/green]: Press enter to take the [red]LRM's output[/red], or type the what is needed.")

    user_message_text = input("Text: ")
    if user_message_text == "":
        output_full = output_str
    else:
        output_full = user_message_text
    
    answers.append(output_full)

    try:
        with open('qa_output.json', 'r', encoding='utf-8') as infile:
            try:
                data = list(json.load(infile))
            except json.JSONDecodeError:
                data = []
    except FileNotFoundError:
        data = []

    with open('qa_output.json', 'w', encoding='utf-8') as outfile:
        json_object = {"instruction": system_prompt, "input": questions[i], "output": answers[i]}
        data.append(json_object)
        json.dump(data, outfile, ensure_ascii=False, indent=2)
        print(f"\n\n[bold italic green]Saved Q&A pairs to qa_output.json[/bold italic green]\n\n")


