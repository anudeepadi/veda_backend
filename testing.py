import openai

openai.api_key = 'pk-**********************************************'
openai.base_url = "http://localhost:3040/v1/"

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Human: Hello\nAI:",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["Human: ", "AI: "]
)

print(response.choices[0].text)