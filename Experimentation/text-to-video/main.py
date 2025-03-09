import torch
import random

from diffusers import LTXPipeline
from diffusers import LTXImageToVideoPipeline

from diffusers import I2VGenXLPipeline

from diffusers.utils import load_image
from diffusers.utils import export_to_gif
from diffusers.utils import export_to_video

pipeline_list = []

#pipeline = I2VGenXLPipeline.from_pretrained("ali-vilab/i2vgen-xl", torch_dtype=torch.float16, variant="fp16")
#pipeline = LTXPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)
pipeline = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)

#pipeline.unet.enable_forward_chunking()
#pipeline.enable_vae_slicing()
pipeline.enable_sequential_cpu_offload()

image_url = "https://tea-cup.midori-ai.xyz/download/39304d7b-d96e-483d-b566-cfc40b6748a8-full.png"
image = load_image(image_url).convert("RGB")

old_prompt = "(Black strapless dress, White cloak), 1woman, (dark green hair), bangs, closed mouth, (golden yellow eyes)+, (small Halo), walking towards camera"

prompt = """
A woman is walking.
She is wearing a black strapless dress and a white cloak. Dark green hair with bangs frames her face. 
Her eyes are a striking golden yellow, and a delicate golden halo adorns her head. 
She has a sliver staff she is using to walk.
She walks through the town, from left to right.
""".replace("\n", " ")

seed = random.randint(1, 99999)
negative_prompt = "Distorted, discontinuous, Ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, Ugly faces, incomplete arms"
generator = torch.manual_seed(seed)

output = pipeline(prompt=prompt, negative_prompt=negative_prompt, image=image, num_inference_steps=150, num_frames=120, frame_rate=24, height=704, width=480, generator=generator)

#output = pipeline(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=150, num_frames=120, frame_rate=24, generator=generator)

frames = output.frames[0]

export_to_gif(frames, "generated.gif", fps=24)
export_to_video(frames, "generated.mp4", fps=24)
