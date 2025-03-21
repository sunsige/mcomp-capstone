from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
  # https://openrouter.ai/deepseek/deepseek-r1-zero:free
)

completion = client.chat.completions.create(
  extra_headers={},
  extra_body={},
  model="deepseek/deepseek-r1-zero:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)