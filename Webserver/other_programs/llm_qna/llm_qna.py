import os
import re
import sys
import json
import time
import torch
import base64
import shutil
import hashlib
import tarfile
import zipfile
import getpass
import pathlib
import platform
import argparse
import subprocess

from halo import Halo

from rich import print
from rich.text import Text
from rich.tree import Tree
from rich.markup import escape
from rich.console import Console
from rich.prompt import Confirm
from rich.filesize import decimal

from transformers import pipeline

pipe = pipeline("text-generation", "deepseek-ai/DeepSeek-R1-Distill-Llama-8B", torch_dtype=torch.bfloat16, device_map="auto")

spinner = Halo(text='Loading', spinner='dots', color='green')

system_message = {"role": "system", "content": "You are a ai that must speak in emotes to the user."}
demo_user_message = {"role": "user", "content": "Hey, can you tell me any fun things to do in New York?"}

chat = [system_message]

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

print()

print(f"Thinking: [italic blue]{thinking_str}[/italic blue]")

print()

print(f"Output: {output_str}")