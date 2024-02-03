def carly(client_openai):
    completion = client_openai.chat.completions.create(
    model="gpt-4.1-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
    )

    for chunk in completion:
        print(chunk.choices[0].delta)