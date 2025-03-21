from openai import OpenAI

def query_deepseek(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model="deepseek/deepseek-r1-zero:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content