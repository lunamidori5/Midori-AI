
import re
import torch

from halo import Halo

from rich import print

from transformers import pipeline

pipe = pipeline("text-generation", "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", torch_dtype=torch.bfloat16, device_map="auto")

spinner = Halo(text='Loading', spinner='dots', color='green')

system_message = {"role": "system", "content": "Please keep messsages and thinking short to save tokens."}
demo_user_message = {"role": "user", "content": "Hey, can you tell me any fun things to do in New York?"}

chat = [system_message]

while True:

    user_message_text = input("Type your message: ")
    user_message = {"role": "user", "content": user_message_text}

    spinner.start(text=f"LRM Thinking...")

    chat.append(user_message)

    response = pipe(chat, max_new_tokens=512 * 4)

    full_response = response[0]['generated_text'] # type: ignore
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

    spinner.succeed(text=f"LRM done!")

    models_message = {"role": "model", "content": f"<think>{thinking_str}</think> {output_str}"}

    chat.append(models_message)

    print(f"\nModel's Thinking: [italic blue]{thinking_str}[/italic blue]\n")
    print(f"Model's Output: {output_str}\n")