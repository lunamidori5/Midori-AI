import torch
import random

from diffusers import LTXPipeline
from diffusers import I2VGenXLPipeline

from diffusers.utils import load_image
from diffusers.utils import export_to_gif
from diffusers.utils import export_to_video

pipeline = I2VGenXLPipeline.from_pretrained("ali-vilab/i2vgen-xl", torch_dtype=torch.float16, variant="fp16")
#pipeline = LTXPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)

pipeline.unet.enable_forward_chunking()
pipeline.enable_vae_slicing()
pipeline.enable_sequential_cpu_offload()

image_url = "https://tea-cup.midori-ai.xyz/download/39304d7b-d96e-483d-b566-cfc40b6748a8-full.png"
image = load_image(image_url).convert("RGB")

prompt = "(Black strapless dress, White cloak), 1woman, (dark green hair), bangs, closed mouth, (golden yellow eyes)+, (small Halo), walking towards camera"
negative_prompt = "Distorted, discontinuous, Ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, Ugly faces, incomplete arms"
generator = torch.manual_seed(random.randint(1, 99999))

frames = pipeline(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=image,
    num_inference_steps=35,
    guidance_scale=1.0,
    num_frames=30,
    height=800,
    width=448,
    generator=generator,
    decode_chunk_size=5
).frames[0]

export_to_gif(frames, "generated.gif")
export_to_video(frames, "generated.mp4", fps=2)
