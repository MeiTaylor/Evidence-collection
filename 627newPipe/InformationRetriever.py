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
# Prompts for Information Retrieving Verifier 
# ------------------------------------------ #


prompt_for_information_retrieving_verifier = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Is This An Authentic Video from a Beach Party in Kyiv in August 2023? | Snopes.com",
    "Video_transcript": "",
    "Video_description_on_platform": "This video clip is used in a fact-check article on Snopes.com. Visit the website for more details.",
    "Video_platform": "youtube",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "New_Question": {
    "Question": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?"
  },
  "Task": "To answer the question, is searching information online needed? Yes or no? Please provide a precise probability, and if the threshold is greater than 80%, give the result as 'Yes', otherwise give the result as 'No'.",
  "Prediction": ""
}
"""

# answer = gpt35_analysis(prompt_for_information_retrieving_verifier)

# print(answer)




import re

def analyze_string(answer):
    # 去除标点符号，并转换为小写
    answer = re.sub(r'[^\w\s]', '', answer).lower()
    words = answer.split()
    
    # 统计 "yes" 和 "no" 的出现次数
    yes_count = words.count("yes")
    no_count = words.count("no")
    
    # 找到字符串的第一个单词
    first_word = words[0] if words else ""
    
    # 判断第一个单词是否是 "yes" 或 "no"
    first_word_is = "yes" if first_word == "yes" else "no" if first_word == "no" else "neither"
    
    # 计算最终结果
    
    if yes_count > no_count and first_word_is == "yes":
        final_result = "yes"
    elif yes_count < no_count and first_word_is == "no":
        final_result = "no"
    
    # return yes_count, no_count, first_word_is, final_result
    return final_result

# # 示例字符串
# answer = """ Yes, searching information online is needed to answer the question about credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023). The probability of needing to search online is more than 80%, so the answer is "Yes." """

# # 调用函数并打印结果
# final_result = analyze_string(answer)

# print(f"The final result is: {final_result}")









# ---------------------------------- #
# Prompts for Queries Generation
# ---------------------------------- #

prompt_for_queries_generation = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Is This An Authentic Video from a Beach Party in Kyiv in August 2023? | Snopes.com",
    "Video_transcript": "",
    "Video_description_on_platform": "This video clip is used in a fact-check article on Snopes.com. Visit the website for more details.",
    "Video_platform": "youtube",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "New_Question": {
    "Question": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?"
  },
  "Task": "In order to answer this question, please determine what information is required, and design queries to search for this information on Google.",
  "Queries": {
    "Query 1": "",
    "Query 2": "",
    ······
  }
}

The final answer only needs "Queries": {
    "Query 1": "",
    "Query 2": "",
    ...
  }, no other explanatory or descriptive statements are needed.

"""

# answer = gpt35_analysis(prompt_for_queries_generation)

# print(answer)




# ------------------------------------------- #
# Prompts for Evidence Judgement and Ranking
# ------------------------------------------- #

prompt_for_evidence_judgement_and_ranking = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Is This An Authentic Video from a Beach Party in Kyiv in August 2023? | Snopes.com",
    "Video_transcript": "",
    "Video_description_on_platform": "This video clip is used in a fact-check article on Snopes.com. Visit the website for more details.",
    "Video_platform": "youtube",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "New_Question": {
    "Question": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?"
  },
  "Task": "Please summarize the related evidence from the searched documents, evaluate the quality, relevance, timeliness of the evidence extracted (comprehensively considering its url, author, content, platform and other relevant information), and rank the searched evidence and grade the three metrics for them from 1 to 5.",
  "Evidence": {
    "Evidence 1": {
      "Source": "Reuters",
      "Article Title": "Ukraine counteroffensive maps",
      "Publication Time": "June 26, 2023",
      "Content Details": "This article discusses the strategies and challenges of the Ukrainian counteroffensive, including tactical deployments and the use of advanced military technology. It also touches on shortages in artillery shells impacting operations.",
      "Quality Score": "",
      "Relevance Score": "",
      "Newness Score": ""
    },
    "Evidence 2": {
      "Source": "Reuters",
      "Article Title": "Ukrainian intercepts show Russian soldiers’ anger at losses, disarray",
      "Publication Time": "September 5, 2023",
      "Content Details": "The article reveals the dire conditions and low morale among Russian soldiers through excerpts from intercepted communications, providing a glimpse into the internal challenges faced by Russian forces.",
      "Quality Score": "",
      "Relevance Score": "",
      "Newness Score": ""
    },
    "Evidence 3": {
      "Source": "Reuters",
      "Article Title": "How weapons from Western allies are strengthening Ukraine's defense against Russia",
      "Publication Time": "Date not specified",
      "Content Details": "Analyzes the impact of Western military support on Ukraine's defense capabilities, detailing various systems and equipment provided and their strategic importance in the conflict.",
      "Quality Score": "",
      "Relevance Score": "",
      "Newness Score": ""
    }
  }
}
"""


# answer = gpt35_analysis(prompt_for_evidence_judgement_and_ranking)

# print(answer)






# ------------------------------------------- #
# Prompts for Evidence Selection
# ------------------------------------------- #

prompt_for_evidence_selection = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Is This An Authentic Video from a Beach Party in Kyiv in August 2023? | Snopes.com",
    "Video_transcript": "",
    "Video_description_on_platform": "This video clip is used in a fact-check article on Snopes.com. Visit the website for more details.",
    "Video_platform": "youtube",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "New_Question": {
    "Question": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?"
  },
  "Current Evidence Searching queries on google": {
    "Query 1": "Ukraine war news August 6-7, 2023",
    "Query 2": "Conflict in Ukraine latest updates August 2023"
  },
  "Evidence Found and Judgments on Them": {
    "Evidence 1": {
      "Source": "Reuters",
      "Article Title": "Ukraine counteroffensive maps",
      "Publication Time": "June 26, 2023",
      "Content Details": "This article discusses the strategies and challenges of the Ukrainian counteroffensive, including tactical deployments and the use of advanced military technology. It also touches on shortages in artillery shells impacting operations.",
      "Quality Score": "5 - The article's information comes from a highly credible source renowned for accurate and comprehensive coverage.",
      "Relevance Score": "5 - Directly addresses the military activities in Ukraine around the time in question, offering insights into efforts to regain territory.",
      "Newness Score": "5 - Offers recent information pertinent to the timeframe surrounding August 7, 2023."
    },
    "Evidence 2": {
      "Source": "Reuters",
      "Article Title": "Ukrainian intercepts show Russian soldiers’ anger at losses, disarray",
      "Publication Time": "September 5, 2023",
      "Content Details": "The article reveals the dire conditions and low morale among Russian soldiers through excerpts from intercepted communications, providing a glimpse into the internal challenges faced by Russian forces.",
      "Quality Score": "5 - Based on primary intercepted communications, verified and reported by a reputable news organization.",
      "Relevance Score": "5 - Provides insights into the Russian military's situation, which directly affects the conflict's dynamics.",
      "Newness Score": "5 - Timely and relevant, shedding light on the state of Russian forces close to the date in question."
    },
    "Evidence 3": {
      "Source": "Reuters",
      "Article Title": "How weapons from Western allies are strengthening Ukraine's defense against Russia",
      "Publication Time": "Date not specified",
      "Content Details": "Analyzes the impact of Western military support on Ukraine's defense capabilities, detailing various systems and equipment provided and their strategic importance in the conflict.",
      "Quality Score": "5 - Offers a thorough analysis from a reliable source, providing a detailed overview of international involvement in the conflict.",
      "Relevance Score": "5 - Essential for understanding the scale and impact of the military support that shapes the ongoing conflict.",
      "Newness Score": "4 - Likely current, given the continuous flow of Western support, but a specific publication date would confirm its exact timeliness."
    }
  },
  "Task": "Based on the quality, relevance, timeliness of the pieces of evidence, decide which of them are suitable to answer 'this question'. If none are suitable, generate none. And regenerate new queries to search for the more suitable information on Google."
}

The final output only requires all numbers that comply with Good Evidence, without any other explanatory or decorative statements (for example, if "Evidence N" is Good Evidence, then only "Evidence N" needs to be answered)
"""

# answer = gpt35_analysis(prompt_for_evidence_selection)

# print(answer)








# -------------------------------------------------- #
# Prompts for Question Answer based on the Evidence
# -------------------------------------------------- #
prompt_for_question_answer_based_on_evidence = """
{
  "Claim": "A video that went viral in August 2023 showed a beach party in Kyiv, proving that the war in Ukraine is a hoax.",
  "Video_information": {
    "Video_headline": "Is This An Authentic Video from a Beach Party in Kyiv in August 2023? | Snopes.com",
    "Video_transcript": "",
    "Video_description_on_platform": "This video clip is used in a fact-check article on Snopes.com. Visit the website for more details.",
    "Video_platform": "youtube",
    "Video_date": "2023_08_07",
    "Video_description_from_descriptor": "The video clip is a mix-up, which shows a beach party with clips and photos of many boys and girls, drinks and beach umbrellas. It seems to happen on a daytime with lots of sunshine. It is hard to determine the location of party from the video pictures or contents."
  },
  "QA_CONTEXTS": {
    "Question_1": "Is there a beach party in Kyiv on or around the date of the video (Aug. 7, 2023)?",
    "Answer_1": "Yes, there was indeed a beach party in Kyiv on August 6, 2023. The event, held at a local beach club, drew attention and was documented in online posts and social media, highlighting the Ukrainians' efforts to maintain some semblance of normalcy despite the ongoing war."
  },
  "New_Question": {
    "Question": "Are there credible reports or evidence of continued conflict or other significant events in Ukraine on or around the date of the video (August 7, 2023)?"
  },
  "Good evidence information": {
    "Evidence 1": {
      "Source": "Reuters",
      "Article Title": "Ukraine counteroffensive maps",
      "Publication Time": "June 26, 2023",
      "Content Details": "This article discusses the strategies and challenges of the Ukrainian counteroffensive, including tactical deployments and the use of advanced military technology. It also touches on shortages in artillery shells impacting operations.",
      "Quality Score": "5 - The article's information comes from a highly credible source renowned for accurate and comprehensive coverage.",
      "Relevance Score": "5 - Directly addresses the military activities in Ukraine around the time in question, offering insights into efforts to regain territory.",
      "Newness Score": "5 - Offers recent information pertinent to the timeframe surrounding August 7, 2023."
    },
    "Evidence 2": {
      "Source": "Reuters",
      "Article Title": "Ukrainian intercepts show Russian soldiers’ anger at losses, disarray",
      "Publication Time": "September 5, 2023",
      "Content Details": "The article reveals the dire conditions and low morale among Russian soldiers through excerpts from intercepted communications, providing a glimpse into the internal challenges faced by Russian forces.",
      "Quality Score": "5 - Based on primary intercepted communications, verified and reported by a reputable news organization.",
      "Relevance Score": "5 - Provides insights into the Russian military's situation, which directly affects the conflict's dynamics.",
      "Newness Score": "5 - Timely and relevant, shedding light on the state of Russian forces close to the date in question."
    },
    "Evidence 3": {
      "Source": "Reuters",
      "Article Title": "How weapons from Western allies are strengthening Ukraine's defense against Russia",
      "Publication Time": "Date not specified",
      "Content Details": "Analyzes the impact of Western military support on Ukraine's defense capabilities, detailing various systems and equipment provided and their strategic importance in the conflict.",
      "Quality Score": "5 - Offers a thorough analysis from a reliable source, providing a detailed overview of international involvement in the conflict.",
      "Relevance Score": "5 - Essential for understanding the scale and impact of the military support that shapes the ongoing conflict.",
      "Newness Score": "4 - Likely current, given the continuous flow of Western support, but a specific publication date would confirm its exact timeliness."
    }
  },
  "Task": "Based on the evidence extracted, generate an explanatory answer to the question that references the evidence. And evaluate the confidence (XX%) of your answer based on the analysis of the above evaluation of the evidence and the logic of the reasoning process."
}
"""

answer = gpt35_analysis(prompt_for_question_answer_based_on_evidence)

print(answer)