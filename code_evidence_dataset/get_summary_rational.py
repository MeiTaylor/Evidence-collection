
import requests
from bs4 import BeautifulSoup
import logging
# from transformers import AutoTokenizer, AutoModel

import json
import requests as requests
import sys
import time
import os
import re
import regex


# # # 配置日志系统
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='fetch_summary_rational.log', filemode='a', encoding='utf-8')
# # 首先清空日志文件
# open('fetch_summary_rational.log', 'w').close()





import json


def verify_model_output(model_output_json, article_content):
    # 如果model_output_json是字符串，则尝试解析为字典
    if isinstance(model_output_json, str):
        try:
            model_output = json.loads(model_output_json)
        except json.JSONDecodeError:
            return "Invalid JSON format"
    elif isinstance(model_output_json, dict):
        model_output = model_output_json
    else:
        return "Invalid input type"
    
    # 存储结果的字典
    verification_results = {}

    # 对每个键值进行验证
    for key, value in model_output.items():
        # 规范化值的空格
        normalized_value = " ".join(value.split())
        # 为比较准备文章内容，将所有引号转换为双引号
        temp_article_content = article_content.replace("'", "\"")
        # 将JSON值中的单引号也转换为双引号以匹配文章内容
        normalized_value = normalized_value.replace("'", "\"")
        
        # 检查是否为文章内容的一部分
        if normalized_value in temp_article_content:
            start_index = temp_article_content.find(normalized_value)
            end_index = start_index + len(normalized_value)
            # 从原始文章内容中获取精确匹配的部分，以保留原文的引号
            exact_match = article_content[start_index:end_index]
            verification_results[key] = exact_match

    return verification_results





api_key = 'sk-T79RDgru0A5379d9d04cT3BlBKFJ7b21709730554F339d9c'


def gpt35_analysis(prompt):
    headers = {
        "Authorization": 'Bearer ' + api_key,
    }

    params = {
        "messages": [
            {
                "role": "system",
                "content": """"To effectively analyze the provided paragraphs from an article in relation to a specific claim and its assigned rating, you are tasked with summarizing a 'rationale' that supports or refutes the claim based on the information presented. This task involves synthesizing the key points into a concise rationale rather than quoting directly from the text. Follow these detailed instructions for accomplishing this task:

- **Understanding the Claim and Rating**: Start by comprehending the claim and its corresponding rating. Understanding the context of the claim and the reasons provided in the text for this rating is essential for synthesizing a valid rationale.

- **Synthesizing the Rationale**: Focus on integrating various points within the article that collectively explain the reasoning behind the claim's rating. Derive a coherent summary that encapsulates why the claim has been evaluated in such a manner, based on the evidence and arguments presented throughout the text.

- **Adherence to the Essence of the Text**: While direct quotations are not required, it is crucial that the synthesized rationale accurately reflects the arguments and evidence found in the text. Ensure that the summary remains true to the original content’s intent and factual basis.

- **Presentation and Formatting**: Present your synthesized findings in a clear and structured format. The rationale should be concise and reflect a comprehensive understanding of the text.

- **Output Requirements**: Format your response in plain text or JSON, labeling the field as 'synthesized_rationale'. This field should contain a synthesized summary that clearly articulates the rationale for the rating based on the analysis of the text.

By following these guidelines, you will be able to provide a clear, structured, and insightful synthesis that captures the essence of the reasons behind the claim's rating based on the article's content."""
            },
            {
                "role": "user",
                "content":prompt
            }
        ],
        "model": 'gpt-3.5-turbo'
    }
    response = requests.post(
        "https://aigptx.top/v1/chat/completions",
        headers=headers,
        json=params,
        stream=False
    )
    res = response.json()
    # print(res)
    res_content = res['choices'][0]['message']['content']
    # print(res_content)
    return res_content




def extract_complete_json(response_text):
    # 使用正则表达式模式匹配嵌套的JSON结构，使用`regex`模块
    json_pattern = r'(\{(?:[^{}]|(?1))*\})'
    matches = regex.findall(json_pattern, response_text)
    if matches:
        try:
            # 尝试解析每个匹配项以找到第一个有效的JSON
            for match in matches:
                json_data = json.loads(match)
                # 返回第一个有效的JSON数据
                return json_data
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
    return None




import requests
from bs4 import BeautifulSoup
import logging

def fetch_article_content(url):
    """
    Fetch and return all paragraph text content from the article at the given URL,
    excluding paragraphs that contain specific substrings, such as "About this rating".
    
    Parameters:
    - url: str, the URL of the article to fetch content from.
    
    Returns:
    - str, all filtered paragraph text content combined.
    """
    
    # 配置日志系统
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='filtered_article_content.log', filemode='w', encoding='utf-8')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    # 发起请求获取网页内容
    response = requests.get(url, headers=headers)
    filtered_paragraphs_text = ""  # 初始化字符串以存储所有过滤后的段落文本
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尝试获取文章内容
        article_content = soup.find('article', attrs={'id': 'article-content'}) or soup.find('article')
        
        if article_content:
            paragraphs = article_content.find_all('p')
            # 过滤不包含特定子串的段落
            filtered_paragraphs = [p for p in paragraphs if "About this rating" not in p.text]
            
            # 合并所有过滤后的段落文本，每个段落之间用换行符分隔
            filtered_paragraphs_text = '\n'.join(paragraph.text for paragraph in filtered_paragraphs)
            
            # 将合并后的段落文本记录到日志
            # logging.info(f"Filtered article paragraphs combined:\n{filtered_paragraphs_text}")
        else:
            logging.info("No article content found.")
            filtered_paragraphs_text = "No article content found."
    else:
        logging.error(f"Failed to retrieve webpage, status code: {response.status_code}")
        filtered_paragraphs_text = "Failed to retrieve webpage."
    
    return filtered_paragraphs_text






def fetch_summary_rational(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')


        logging.info("Claim")
        
        # 提取并记录claim及其内容
        claim_content = soup.select(".claim_cont")[0].text.strip()
        # logging.info(f"Claim: {claim_content}")

        # logging.info("------------------------------------------------")

        # logging.info("Rating")
        
        # 提取并记录Rating的类别
        rating_content = soup.select(".rating_title_wrap")[0].text.strip()[:-18].strip()
        # logging.info(f"Rating: {rating_content}")

        # logging.info("------------------------------------------------")

        # logging.info("Article Content")
        
        # 提取并记录article正文的所有内容
        article_content = fetch_article_content(url)

        # 将合并后的段落文本记录到日志
        # logging.info(f"Filtered article paragraphs combined:\n{article_content}")

        # logging.info("------------------------------------------------")


        # logging.info("开始提取Evidence")


#         prompt = f""""The objective is to analyze a series of paragraphs from an article to support or refute a given claim. This analysis requires synthesizing a 'rationale' from the content that supports the given rating, rather than directly quoting sentences from the article:
# - 'Rationale': Based on the entire content provided, synthesize a rationale that explains why the claim has been assigned this specific truthfulness rating. Consider the key arguments, evidence, and data presented throughout the text and integrate them into a comprehensive rationale that articulates the judgment process.
# **Claim:** {claim_content}
# **Rating:** {rating_content}
# **Paragraphs:** {article_content}
# The response should demonstrate a clear and insightful understanding of the text, forming a synthesized rationale that aligns with the overall content and intent of the article. This summary should reflect a high level of analytical thought and provide a well-rounded explanation of why the claim has been rated as it has.
# **Specified output format in JSON (or text, if preferred):**
# {{
# "synthesized_rationale": "A synthesized summary that clearly articulates the rationale for the '{rating_content}' rating based on a comprehensive analysis of the text."
# }}
# Reminder: The final output must present a synthesized summary that captures the essence of the rationale without directly quoting from the article. The summary should be original, yet closely aligned with the content and analysis provided in the text."
# """

        prompt = f"""
The objective is to analyze a series of paragraphs from an article to support or refute a given claim. This analysis requires synthesizing a 'rationale' from the content that supports the given rating, rather than directly quoting sentences from the article:

- 'Rationale': Rationale refer to the explanations or logical underpinnings provided by fact-checkers after assessing a claim or assertion. These explanations detail why a claim is considered true, false, misleading, or other false types. Paragraph that analyzes, interpretates, summarizes the background, context, or broader circumstances (including evidence) surrounding a claim to predict truthfulness label and explains the ruling process.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Paragraphs:** {article_content}

First, please synthesize a comprehensive and professional rationale that thoroughly articulates the reasons for the '{rating_content}' rating. This rationale should be based on an in-depth analysis of the text, considering all relevant factors . Ensure that the rationale is detailed, covering all major reasons for the rating, and presenting a clear, well-organized, and logically sound argument that effectively supports the given rating.

Following this, generate several specific, individual reasons. Each reason should support the synthesized rationale and be presented as separate entries, each labeled uniquely (e.g., detailed_reasons1, detailed_reasons2, etc.), explaining in detail how it connects to and supports the overall rationale based on the content of the paragraphs. Each specific reason should be focused on a single, small aspect of the rationale, and should be clearly and explicitly connected to the synthesized rationale.

For each specific reason, ensure that:
- It directly supports the synthesized rationale.
- It includes a clear explanation of how it was derived from the article content.
- It addresses any potential counterarguments and explains why they do not change the overall rating.

**Specified output format in JSON (or text, if preferred):**
{{
    "synthesized_rationale": "A synthesized summary that clearly and thoroughly articulates the rationale for the '{rating_content}' rating based on a comprehensive analysis of the text.",
    "detailed_reasons": {{
       "reason1": "Detailed explanation of the first specific reason supporting the overall rationale.",
       "reason2": "Detailed explanation of the second specific reason supporting the overall rationale.",
       "reason3": "Detailed explanation of the third specific reason supporting the overall rationale.",
       ...
    }}
}}

Reminder: The final output must present a synthesized summary that captures the essence of the rationale without directly quoting from the article. The summary should be original, yet closely aligned with the content and analysis provided in the text.
"""



        # logging.info("------------------------------------------------")


        # 提取证据
        gpt35_rational= gpt35_analysis(prompt)

        # logging.info(f"GPT-3.5 Rational: \n {gpt35_rational}")

        # logging.info("------------------------------------------------")


        complete_summary_rational = extract_complete_json(gpt35_rational)

        # logging.info("------------------------------------------------")

        # logging.info(f"complete_summary_rational : \n {complete_summary_rational}")
        # logging.info("------------------------------------------------")



    # 你之前的else语句处理网页请求失败的情况
    else:
        logging.error(f"网页请求失败，状态码: {response.status_code}")

    # 假设这是函数的结尾，根据你的上下文可能需要返回一些值
    return complete_summary_rational











# # # chatglm3出错，gpt35成功
# url = "https://www.snopes.com/fact-check/swift-trump-won-grammys/"

# fetch_single_reason(url)

# # all_paragraphs_text, extracted_complete_json = fetch_and_log_webpage_content(url)

# # logging.info("Done.")
# # logging.info("------------------------------------------------")
# # logging.info("正文内容如下：")
# # logging.info(all_paragraphs_text)
# # logging.info("------------------------------------------------")
# # logging.info("证据如下：")
# # logging.info(extracted_complete_json)


# url = "https://www.snopes.com/fact-check/amy-schumer-falling-down-stairs/"

# complete_summary_rational = fetch_summary_rational(url)

# print(complete_summary_rational)
# logging.info(complete_summary_rational)

# print("Done.")