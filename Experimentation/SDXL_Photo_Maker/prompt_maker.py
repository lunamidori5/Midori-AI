
def prompt_maker(weather_in, mood):
    prompt_parts_old = [
        "input: Make a text to photo prompt based on the data given. The weather is ``fair`` : the subject is Luna Midori",
        "output: Luna, (black wrap simple dress with a black cloak, (small+ crystal necklace)), 1woman mid 20s, (dark green ponytail), bangs, closed mouth, (golden yellow eyes)+, Small Halo-, City, fair weather",
        ]
    
    ## Make sure you add at least 25 to 50 input and output lines of the char you want
    
    prompt_parts = [
                {"role": "system", "content": "Luna Midori is a young female woman with green hair and golden yellow eyes. She is in her mid-20s. Luna lives in the city of Portland OR and like to ride the train. When telling her about the weather please make a wide number of scenes up for her to be in"}
            ]
    
    for item in prompt_parts_old:
        if "input:" in item:
            prompt_parts.append({"role": "user", "content": item.replace("input: ", "")})
        if "output:" in item:
            prompt_parts.append({"role": "assistant", "content": item.replace("output: ", "")})

    pre_pro_now = prompt_parts

    pre_pro_now.append({"role": "user", "content": f"Make a text to photo prompt based on the data given. The weather is ``{weather_in}`` : the subject is Luna Midori ({mood})"})

    return pre_pro_now