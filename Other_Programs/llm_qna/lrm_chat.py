
import re
import time
import torch

from halo import Halo

from rich import print

from transformers import pipeline

model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

print(f"Loading `{model}`...")
pipe = pipeline("text-generation", model, torch_dtype=torch.bfloat16, device_map="auto")
print(f"Loaded `{model}`")

spinner = Halo(text='Loading', spinner='dots', color='green')

system_message = {"role": "system", "content": "You are now `d8a` a ai that helps the user. Please keep messsages and thinking short to save tokens."}
demo_user_message = {"role": "user", "content": "Hey, can you tell me any fun things to do in New York?"}

chat = [system_message]

while True:

    user_message_text = input("Type your message: ")
    user_message = {"role": "user", "content": user_message_text}

    print()

    spinner.start(text=f"LRM Thinking...")

    start_time = time.time()
    
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
    spinner.succeed(text=f"LRM done took {time_taken:.2f} seconds")

    models_message = {"role": "model", "content": f"<think>{thinking_str}</think> {output_str}"}

    chat.append(models_message)

    print(f"\nLRM's Thinking: [italic blue]{thinking_str}[/italic blue]\n")
    print(f"LRM's Output: [red]{output_str}[/red]\n")