import torch
import random

from diffusers import LTXPipeline
from diffusers import LTXImageToVideoPipeline

from diffusers import I2VGenXLPipeline

from diffusers.utils import load_image
from diffusers.utils import export_to_gif
from diffusers.utils import export_to_video

#pipeline = I2VGenXLPipeline.from_pretrained("ali-vilab/i2vgen-xl", torch_dtype=torch.float16, variant="fp16")
pipeline = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)

#pipeline.unet.enable_forward_chunking()
#pipeline.enable_vae_slicing()
pipeline.enable_sequential_cpu_offload()

image_url = "https://tea-cup.midori-ai.xyz/download/39304d7b-d96e-483d-b566-cfc40b6748a8-full.png"
image = load_image(image_url).convert("RGB")

old_prompt = "(Black strapless dress, White cloak), 1woman, (dark green hair), bangs, closed mouth, (golden yellow eyes)+, (small Halo), walking towards camera"

prompt = """
Cinematic shot of a woman walking towards the camera. 
The scene is a cave filled with ethereal light. 
She is wearing a black strapless dress and a white cloak. 
Dark green hair with bangs frames her face. 
Her eyes are a striking golden yellow, and a delicate halo adorns her head. 
She moves with a magical aura, a gentle wave of distorted light rippling behind her as she progresses through the cave.
""".replace("\n", " ")

negative_prompt = "Distorted, discontinuous, Ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, Ugly faces, incomplete arms"
generator = torch.manual_seed(random.randint(1, 99999))

output = pipeline(
    prompt=prompt, negative_prompt=negative_prompt, 
    image=image, num_inference_steps=45, guidance_scale=9.0, num_frames=75, 
    height=1280, width=704, generator=generator)

frames = output.frames[0]

export_to_gif(frames, "generated.gif", fps=2)
export_to_video(frames, "generated.mp4", fps=2)
