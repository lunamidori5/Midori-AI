import os
import re
import json
import uuid
import time
import pytz
import torch
import psutil
import random
import asyncio
import climage
import argparse
import datetime
import requests
import subprocess
import python_weather

from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM 

from prompt_importer import prompt_maker

try:
    from rich import print
except Exception as Error:
    from builtins import print

def log(message):
    print(message)

    if "login".lower() in message.lower():
        return

    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

parser = argparse.ArgumentParser(description="N/A")
parser.add_argument("-pn", "--photoname", help="Name of the photo to make")
parser.add_argument("-t", "--theme", help="Theme of the photo, ie happy")
args = parser.parse_args()

photo_name = str(args.photoname)
mood = photo_name.split("_")[0]

ram_info = psutil.virtual_memory()

ram_min_total = 40 * 1024 * 1024 * 1024

if os.name != 'nt':
    os.nice(19)

model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

try:
    from PIL import Image
    from diffusers import AutoPipelineForText2Image
    from diffusers import AutoPipelineForImage2Image

    from diffusers import KDPM2AncestralDiscreteScheduler
    from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
    
except Exception as e:
    log(f"Oops import error: {str(e)}")
        
    exit(0)


def is_amd_gpu():
  """
  Checks if an AMD GPU is present in the system.
  Returns:
    bool: True if an AMD GPU is detected, False otherwise.
  """
  try:
    # Run the 'lspci' command and filter for AMD/ATI graphics cards.
    result = subprocess.run(['lspci'], capture_output=True, text=True, check=True)
    output = result.stdout
    return "AMD" in output or "ATI" in output
  except (subprocess.CalledProcessError, FileNotFoundError):
    # Handle cases where 'lspci' is not available or returns an error.
    return False

def is_night_in_portland():
  """Checks if it is currently nighttime in Portland, OR.

  Returns:
    True if it is nighttime, False otherwise.
  """

  # Get the current time in Portland
  portland_timezone = pytz.timezone('America/Los_Angeles')
  now = datetime.datetime.now(portland_timezone)

  # Define nighttime hours (adjust as needed)
  night_start_hour = 20  # 8 PM
  night_end_hour = 7  # 7 AM

  # Check if it's within the nighttime hours
  if now.hour >= night_start_hour or now.hour < night_end_hour:
    return True
  else:
    return False

async def getweather():
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Beaverton, OR')

        # returns the current day's forecast temperature (int)
        log(weather.temperature)
        weather_now = str(weather.description)

        # get the weather forecast for a few days
        weather_tomorrow = []
        for forecast in weather.daily_forecasts:
            log(forecast)

            # hourly forecasts
            for hourly in forecast.hourly_forecasts:
                log(f' --> {hourly!r}')
                weather_tomorrow.append(str(hourly.description))

        return weather_now, weather_tomorrow

def progress(pipeline, step, timestep, callback_kwargs):

    latents = callback_kwargs["latents"]

    weights = (
        (60, -60, 25, -70),
        (60,  -5, 15, -50),
        (60,  10, -5, -35)
    )

    weights_tensor = torch.t(torch.tensor(weights, dtype=latents.dtype).to(latents.device))
    biases_tensor = torch.tensor((150, 140, 130), dtype=latents.dtype).to(latents.device)
    rgb_tensor = torch.einsum("...lxy,lr -> ...rxy", latents, weights_tensor) + biases_tensor.unsqueeze(-1).unsqueeze(-1)
    image_array = rgb_tensor.clamp(0, 255)[0].byte().cpu().numpy()
    image_array = image_array.transpose(1, 2, 0)
    
    image = Image.fromarray(image_array)
    image.save(f"{photo_name}")

    output = climage.convert(photo_name, is_unicode=True, width=75)

    log(output)
    
    return callback_kwargs

async def get_model():
    url = "https://tea-cup.midori-ai.xyz/download/list.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        python_list = list(data)
        image_model = python_list
        log(str(python_list))
    else:
        image_model = ["cagliostrolab/animagine-xl-3.0", "dreamlike-art/dreamlike-anime-1.0", "Linaqruf/animagine-xl"]
        log("An error occurred while fetching the file.")

    return image_model

async def load_loras(pipeline, lora):

    try:
        log(f"Loading lora: {lora}")
        pipeline.load_lora_weights(lora)
    except Exception as e:
        log(f"Error trying to run ``LORAs`` : {str(e)}")

    return pipeline

async def full_generate(text, neg_text):
    image_model = await get_model()

    image_name_uuid = f'img_{str(uuid.uuid4())}.png'
    model_name = image_model[random.randint(0, len(image_model)-1)]

    ddim = KDPM2AncestralDiscreteScheduler.from_pretrained(model_name, subfolder="scheduler")

    if torch.cuda.is_available():
        if is_amd_gpu():
            device = "cpu"
        else:
            device = "cuda"
    else:
        device = "cpu"

    try:
        log(f"Trying {model_name} with Auto Huggingface XL Pipeline ({device})")
        pipeline = StableDiffusionXLPipeline.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)
    except Exception as e:
        log(f"Error trying to run ``Auto Huggingface XL Pipline`` : {str(e)}")
        log(f"Forcing {model_name} with Huggingface Pipeline")
        pipeline = AutoPipelineForText2Image.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)
    
    try:
        log(f"Trying {model_name} with Auto Huggingface XL I2I Pipeline ({device})")
        pipeline_main = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline_main.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline_main.scheduler.config)
    except Exception as e:
        log(f"Error trying to run ``Auto Huggingface XL I2I Pipeline`` : {str(e)}")
        log(f"Forcing {model_name} with Huggingface I2I Pipeline")
        pipeline_main = AutoPipelineForImage2Image.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline_main.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline_main.scheduler.config)
    
    if device == "cuda":
        pipeline.enable_sequential_cpu_offload()
        pipeline_main.enable_sequential_cpu_offload()

        pipeline.enable_vae_slicing()
        pipeline_main.enable_vae_slicing()

        pipeline.enable_vae_tiling()
        pipeline_main.enable_vae_tiling()
    
    else:
        pipeline.to("cpu")
        pipeline_main.to("cpu")

    pipeline = await load_loras(pipeline, "minimaxir/sdxl-wrong-lora")
    pipeline_main = await load_loras(pipeline_main, "minimaxir/sdxl-wrong-lora")
    
    is_night = is_night_in_portland()

    if is_night:
        pipeline = await load_loras(pipeline, 'ostris/nighttime-lora')
        pipeline_main = await load_loras(pipeline_main, 'ostris/nighttime-lora')
    
    if "luna".lower() in text.lower():
        pipeline = await load_loras(pipeline, 'Bobbarker67/lunamidori_lora')
        pipeline_main = await load_loras(pipeline_main, 'Bobbarker67/lunamidori_lora')
    
    if "carly".lower() in text.lower():
        pipeline = await load_loras(pipeline, 'Bobbarker67/lunamidori_lora')
        pipeline_main = await load_loras(pipeline_main, 'Bobbarker67/lunamidori_lora')

    max_int = 1024

    log(f"Generating starting latent image...  ({device})")
    retrys_int = 0
    while retrys_int < 20:
        try:
            image = pipeline(prompt=text, negative_prompt=neg_text, denoising_end=0.95, height=max_int, width=max_int, callback_on_step_end=progress, callback_on_step_end_tensor_inputs=["latents"], output_type="latent",).images
            break
        except Exception as error:
            log(f"ERROR {str(error)}")
            retrys_int = retrys_int + 1
            
            await asyncio.sleep(15)

    log("Starting latent image generated.")

    log("Generating final image...")
    retrys_int = 0
    while retrys_int < 20:
        try:
            image = pipeline_main(prompt=text, negative_prompt=neg_text, denoising_start=0.85, height=max_int, width=max_int, callback_on_step_end=progress, callback_on_step_end_tensor_inputs=["latents"], image=image).images[0]
            break
        except Exception as error:
            log(f"ERROR {str(error)}")
            retrys_int = retrys_int + 1
            
            await asyncio.sleep(15)

    log("Final image generated.")

    log("Saving images...")
    image.save(image_name_uuid)
    result = Image.open(image_name_uuid).convert('RGBA')
    result.save(photo_name, 'PNG')
    log("Images saved.")

async def partly_generate(text, neg_text):
    image_model = await get_model()

    image_name_uuid = f'img_{str(uuid.uuid4())}.png'
    model_name = image_model[random.randint(0, len(image_model)-1)]

    ddim = KDPM2AncestralDiscreteScheduler.from_pretrained(model_name, subfolder="scheduler")

    if torch.cuda.is_available():
        if is_amd_gpu():
            device = "cpu"
        else:
            device = "cuda"
    else:
        device = "cpu"

    try:
        log(f"Trying {model_name} with Auto Huggingface XL Pipeline ({device})")
        pipeline = StableDiffusionXLPipeline.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)
    except Exception as e:
        log(f"Error trying to run ``Auto Huggingface XL Pipline`` : {str(e)}")
        log(f"Forcing {model_name} with Huggingface Pipeline")
        pipeline = AutoPipelineForText2Image.from_pretrained(model_name, scheduler=ddim, use_safetensors=True)
        #pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)
    
    if device == "cuda":
        pipeline.enable_sequential_cpu_offload()
        pipeline.enable_vae_slicing()
        pipeline.enable_vae_tiling()
    
    else:
        pipeline.to("cpu")

    pipeline = await load_loras(pipeline, "minimaxir/sdxl-wrong-lora")
    
    is_night = is_night_in_portland()

    if is_night:
        pipeline = await load_loras(pipeline, 'ostris/nighttime-lora')
    
    if "luna".lower() in text.lower():
        pipeline = await load_loras(pipeline, 'Bobbarker67/lunamidori_lora')
    
    if "carly".lower() in text.lower():
        pipeline = await load_loras(pipeline, 'Bobbarker67/lunamidori_lora')

    max_int = 1024

    log("Generating final image...")
    retrys_int = 0
    while retrys_int < 20:
        try:
            image = pipeline(prompt=text, negative_prompt=neg_text, height=max_int, width=max_int, callback_on_step_end=progress, callback_on_step_end_tensor_inputs=["latents"]).images[0]
            break
        except Exception as error:
            log(f"ERROR {str(error)}")
            retrys_int = retrys_int + 1
            
            await asyncio.sleep(15)

    log("Final image generated.")

    log("Saving images...")
    image.save(image_name_uuid)
    result = Image.open(image_name_uuid).convert('RGBA')
    result.save(photo_name, 'PNG')
    log("Images saved.")

async def main():
    os.system("touch program.lock")
    while True:

        colors = ["crimson", "teal", "fuchsia", "olive", "indigo", "sienna", "aquamarine", "coral", "orchid", "chartreuse", "lavender", "tan", " salmon", "plum", "turquoise"]

        try:
            weather_now, weather_tomorrow = await getweather()
        except Exception as e:
            log(f"Oops something went wrong - {str(e)}")
            weather_now = f"(glichy {colors[random.randint(0, 14)]} and {colors[random.randint(0, 14)]} rain)"
            weather_tomorrow = f"(glichy {colors[random.randint(0, 14)]} and {colors[random.randint(0, 14)]} rain)"
        
        weather_pre_now = weather_now

        log("Current Forecast:")
        log(weather_now)
        retrys = 0
        pre_pro_now = prompt_maker(weather_pre_now, mood)

        pipe = pipeline("text-generation", model, torch_dtype="auto", device_map="auto")

        while True:
            try:
                response = pipe(pre_pro_now, max_new_tokens=1024)

                thinking_full_response = response[0]['generated_text'][-1]['content']  # type: ignore
                full_response = response[0]['generated_text'][0]['content']  # type: ignore
                thinking_str = ""
                output_str = ""
                content = "<think> "
                
                if "<think>" in thinking_full_response:
                    content = thinking_full_response  # type: ignore
                else:
                    content += thinking_full_response  # type: ignore
                
                thinking_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL) # type: ignore
                if thinking_match:
                    thinking_str = thinking_match.group(1).strip()
                    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip() # type: ignore
                    output_str = content
                else:
                    output_str = content
            
                if len(thinking_str) < 1:
                    log(f"Model failed to reply: full replay ``{full_response}``")
                    log(f"Model failed to reply: full thinking ``{thinking_full_response}``")
                    thinking_str = "Model failed to output thinking"
                
                if len(output_str) < 1:
                    Exception("\nModel failed to reply")
                
                decoded_output = output_str

                await asyncio.sleep(1)

                if "Make a text to photo prompt" in decoded_output:
                    raise ValueError("Bad text seen, trying again")

                break
            except Exception as e:
                log(str(e) + f": text seen {output_str} / full replay {full_response}")
                retrys =+ 1

                if retrys > 50:
                    exit(404)
                
        del pipe

        spacer_str = "~" * 10
        colored_spacer = f"[green]{spacer_str}[/green]"

        log(colored_spacer)

        log("Forecast for the Prompt:")

        log(colored_spacer)

        log(f"LRM's Thinking: [italic blue]{thinking_str}[/italic blue]")

        log(colored_spacer)

        log(f"LRM's Output: [red]{output_str}[/red]")

        log(colored_spacer)

        stuff_to_be_removed = "| nude, nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, wrong, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], nudes, naked, sex, horny, sexual"

        if ram_info.total >= ram_min_total:
            retrys = 0
            while retrys < 2:
                try:
                    await full_generate(decoded_output, stuff_to_be_removed)
                    break
                except Exception as e:
                    log(str(e))
                    retrys += 1
        else:
            retrys = 0
            while retrys < 2:
                try:
                    await partly_generate(decoded_output, stuff_to_be_removed)
                    break
                except Exception as e:
                    log(str(e))
                    retrys += 1
                    
        os.remove("program.lock")
        
        exit(0)

if __name__ == "__main__":
    asyncio.run(main())
