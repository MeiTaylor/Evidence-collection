import json
import requests
import re





api_key = 'sk-NMDvPWjVD75ac1ba4D4cT3BLbkFJb3a0AeE39e8C4E6D9022'

def gpt35_analysis(prompt):
    url = "https://cn2us02.opapi.win/v1/chat/completions"

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    res_content = res['choices'][0]['message']['content']
    return res_content





# ------------------------------------------ #
# Prompts for Claim Verifier 
# ------------------------------------------ #

prompt_for_claim_verifier = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Stew Peters - The war in Ukraine is FAKE.",
    "Video_transcript": "",
    "Video_decription": "The war in Ukraine is FAKE. https://t.co/l63GG7oUTl",
    "Video_platform": "twitter",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war.",
    "Question_2": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?",
    "Answer_2": "Yes, there were credible reports and evidence of continued conflict and other significant events in Ukraine around the date of the video (August 7, 2023). During this period, there were ongoing military actions, including shelling and missile attacks in various regions of Ukraine. For instance, reports from early August 2023 highlighted Ukrainian forces making gains in the south while facing continued hostilities in other parts, such as Kherson, which was under shelling​​."
  },
  "Task": "Can we know whether the claim is true or false now? Yes or no? Please provide a reliability probability based on the existing information, and if the threshold is greater than 80%, give the result as 'Yes', otherwise give the result as 'No'.",
  "Prediction": ""
}

The final output only requires a reliability probability (0%~100%), as well as Yes and No to indicate whether the existing information can support the judgment of truth or falsehood. There is only one Yes or NO, and a reliability probability of 0% to 100%
"""

# answer = gpt35_analysis(prompt_for_claim_verifier)

# print(answer)







# ------------------------------------------ #
# Prompts for the initial question generation
# ------------------------------------------ #

prompt_for_initial_question = """
{
  "Prompts for Question Generation": {
    "Purpose": "Generate questions to determine the veracity of the claim.",
    "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
    "Video_information": {
      "Video_headline": "Stew Peters - The war in Ukraine is FAKE.",
      "Video_transcript": "",
      "Video_description": "The war in Ukraine is FAKE. https://t.co/l63GG7oUTl",
      "Video_platform": "twitter",
      "Video_date": "2023_08_07",
      "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
    },
    "Task": "Based on all the information provided, generate a question that only requires one question to verify the authenticity of the video content and the authenticity of the statement.",
    "Initial_Question_Generation": {
      "Question": ""
    }
  }
}
"""

# answer = gpt35_analysis(prompt_for_initial_question)

# print(answer)



# ---------------------------------------------- #
# Prompts for the follow-up question generation
# ---------------------------------------------- #

prompt_for_the_follow_up_question = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Stew Peters - The war in Ukraine is FAKE.",
    "Video_transcript": "",
    "Video_decription": "The war in Ukraine is FAKE. https://t.co/l63GG7oUTl",
    "Video_platform": "twitter",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "Task": "To verify the claim, what is the next question we need to know the answer to?"
}
"""

# answer = gpt35_analysis(prompt_for_the_follow_up_question)

# print(answer)





# ------------------------------- #
# Prompts for Validator
# ------------------------------- #
prompt_for_validator = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Stew Peters - The war in Ukraine is FAKE.",
    "Video_transcript": "",
    "Video_decription": "The war in Ukraine is FAKE. https://t.co/l63GG7oUTl",
    "Video_platform": "twitter",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war.",
    "Question_2": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?",
    "Answer_2": "Yes, there were credible reports and evidence of continued conflict and other significant events in Ukraine around the date of the video (August 7, 2023). During this period, there were ongoing military actions, including shelling and missile attacks in various regions of Ukraine. For instance, reports from early August 2023 highlighted Ukrainian forces making gains in the south while facing continued hostilities in other parts, such as Kherson, which was under shelling​​."
  },
  "Task": "Does the QA pair have additional knowledge useful for verifying the claim? Just answer yes or no"
}
"""

# answer = gpt35_analysis(prompt_for_validator)

# print(answer)







# ------------------------------- #
# Prompts for Reasoner
# ------------------------------- #

prompt_for_reasoner = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Stew Peters - The war in Ukraine is FAKE.",
    "Video_transcript": "",
    "Video_decription": "The war in Ukraine is FAKE. https://t.co/l63GG7oUTl",
    "Video_platform": "twitter",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "Contexts": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war.",
    "Question_2": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?",
    "Answer_2": "Yes, there were credible reports and evidence of continued conflict and other significant events in Ukraine around the date of the video (August 7, 2023). During this period, there were ongoing military actions, including shelling and missile attacks in various regions of Ukraine. For instance, reports from early August 2023 highlighted Ukrainian forces making gains in the south while facing continued hostilities in other parts, such as Kherson, which was under shelling​​.",
    "Question_3": "Could the beach party in Kyiv serve as sufficient evidence to prove that the war in Ukraine is a hoax? If not, what is the real relationship between them?",
    "Answer_3": "No, a beach party in Kyiv cannot serve as sufficient evidence to prove that the war in Ukraine is a hoax. Such events, occurring even in conflict zones, do not negate the existence or the severity of ongoing conflicts. Instead, they can represent moments of resilience or normalcy that local populations strive for despite the circumstances."
  },
  "Task": "Is this claim true or false? And which information type does it belong to: Real, Unverified, Outdated, or False? If 'False,' specify the type: False video description, Video Clip Edit, Computer-generated Imagery, False speech, Staged Video, Text-Video Contradictory, Text unsupported by the video. Please provide your reasoning process.",
  "Output_Format": {
    "Answer": "",
    "Reasons": "",
    "Therefore, the claim authenticity is": "",
    "The information type is": "",
    "If it is false, the specific type of False Information is": ""
  }
}
"""

answer = gpt35_analysis(prompt_for_reasoner)
print(answer)