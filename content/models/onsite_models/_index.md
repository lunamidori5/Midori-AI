
+++
disableToc = false
title = "Recommended Models"
weight = 154
+++

All models are highly recommened for newer users as they are super easy to use and use the CHAT templ files from [Twinz](https://github.com/TwinFinz)

| Model Size | Description | Links |
|---|---|---|
| 7b | CPU Friendly, small, okay quality | https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF |
| 2x7b | Normal sized, good quality | https://huggingface.co/TheBloke/laser-dolphin-mixtral-2x7b-dpo-GGUF |
| 8x7b | Big, great quality | https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF |
| 70b | Large, hard to run, significant quality | https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF |

| Quant Mode | Description |
|---|---|
| Q3 | Smallest , significant quality loss - not recommended |
| Q4 | Medium, balanced quality |
| Q5 | Large, very low quality loss - recommended for  most users |
| Q6 | Very large, extremely low quality loss |
| Q8 | Extremely large, extremely low quality loss, hard to use - not recommended |
| None | Extremely large, No quality loss, super hard to use - really not recommended |

The minimum RAM and VRAM requirements for each model size, as a rough estimate.
- 7b: System RAM: 10  GB / VRAM: 2 GB
- 2x7b: System RAM: 25 GB / VRAM: 8 GB
- 8x7b: System RAM: 55 GB / VRAM: 28 GB
- 70b: System RAM: 105 GB / VRAM: AI Card or better