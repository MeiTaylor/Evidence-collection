
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
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='get_rational.log', filemode='a', encoding='utf-8')
# # 首先清空日志文件
# open('get_rational.log', 'w').close()





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

    # 将文章内容统一转换为小写，并将所有单引号替换为双引号以供后续比较
    temp_article_content = article_content.lower().replace("'", "\"")

    # 对每个键值进行验证
    for key, value in model_output.items():
        # 规范化值的空格，并转换为小写，同时将所有单引号替换为双引号
        normalized_value = " ".join(value.split()).lower().replace("'", "\"")
        
        # 检查是否为文章内容的一部分
        if normalized_value in temp_article_content:
            start_index = temp_article_content.find(normalized_value)
            end_index = start_index + len(normalized_value)
            # 从原始文章内容中获取精确匹配的部分，以保留原文的大小写和引号
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
                "content": """"To effectively analyze the provided paragraphs from an article in relation to a specific claim and its assigned rating, you are tasked with identifying segments that serve as the 'rationale' for the rating. Each identified segment must be quoted directly from the text without any modification. Follow these detailed instructions for accomplishing this task:

- **Understanding the Claim and Rating**: Start by comprehending the claim and its corresponding rating. Grasping the context and rationale behind this rating is essential for identifying relevant text segments.

- **Extracting the Rationale**: Focus on finding sentences within the article that explicitly explain the reasoning behind the claim's rating. Look for sentences that directly address why the claim has been evaluated as such, ensuring these excerpts clearly reflect the rationale for the rating.

- **Adherence to Original Text**: It is crucial that all extracted text segments—representing the rationale—are quoted verbatim. Avoid any deviation from the original text such as paraphrasing or summarizing.

- **Presentation and Formatting**: Present your findings in a structured format. Each identified rationale should be clearly cited and presented as found in the original text.

- **Output Requirements**: Format your response in JSON, with fields labeled 'rationale1', 'rationale2', etc., depending on the number of rationales extracted. Each field should contain the exact sentence from the article that illustrates the rationale for the rating.

By following these guidelines, you will be able to provide a clear, structured, and precise analysis that reflects the reasons behind the claim's rating based on the original article text."
"""
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



def check_main_rationale_present(complete_json):
    # 检查是否包含 "main_rationale" 键
    # return "main_rationale" in complete_json.get("original_rationales", {})
    if complete_json:
        if "main_rationale" in complete_json:
            return True
    return False



def fetch_original_rational(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')


        # logging.info("Claim")
        
        # 提取并记录claim及其内容
        claim_content = soup.select(".claim_cont")[0].text.strip()

        
        # 提取并记录Rating的类别
        rating_content = soup.select(".rating_title_wrap")[0].text.strip()[:-18].strip()

        
        # 提取并记录article正文的所有内容
        article_content = fetch_article_content(url)



        prompt = f""""The objective is to analyze a series of paragraphs from an article to support or refute a given claim. This analysis requires identifying specific segments within the text classified as 'rationale' for the rating. These segments should be original, unaltered sentences from the article:
- 'Rationale': Please identify at least one paragraph in the article that serves as the 'rationale' for the rating. According to the definition, 'rationale' refers to a paragraph that summarizes the evidence based on the predicted truthfulness label and explains the ruling process. This paragraph should clearly demonstrate why, based on the provided evidence and analysis, the assertion has been assigned this specific truthfulness rating.Raw Rationale is a sentence directly extracted from an article, reflecting the core evidence or reasoning behind why a particular rating is given.Additional_rational is also a sentence directly extracted from the article, used to provide additional support or background information, enhance the argument of the main reason, but may not necessarily include the specific content of the rating.
The task demands a meticulous extraction of text segments, ensuring they are presented in their original form as direct quotations from the article. This approach underscores the necessity for clarity and fidelity to the source material.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Paragraphs:** {article_content}
The rationale must be an exact quotation from the text, clearly distinguished in the response to demonstrate the foundation of the rating provided. It is imperative that the rationale provided in the JSON output is an exact, unaltered replica of the sentences found in the original text, without any alterations, rephrasing, or summarization.
**Specified output format in JSON:**
{{
"main_rationale": "Exact original sentence from the text reflecting the rationale for the '{rating_content}' rating",
"addtional_rationale1": "Exact original sentence from the text providing additional support, not necessarily including '{rating_content}'",
"addtional_rationale2": "Exact original sentence from the text providing additional support, not necessarily including '{rating_content}'",
"addtional_rationale3": ············
}}
Reminder: The final output must strictly contain the original sentences for the rationale and additional rationales directly extracted from the paragraphs, exactly as they appear in the source, without any alterations, rephrasing, or summarization."""


        # logging.info("------------------------------------------------")
        max_attempts = 5
        attempt = 0
        complete_json = None
        main_rational_present = False
        while not main_rational_present:
            attempt += 1
            # 提取证据
            gpt35_rationale= gpt35_analysis(prompt)

            complete_json = extract_complete_json(gpt35_rationale)

            logging.info("------------------------------------------------")

            logging.info(f"GPT35 Original Rational: \n {complete_json}")
            logging.info("------------------------------------------------")

            verification_results = verify_model_output(complete_json, article_content)

            main_rational_present = check_main_rationale_present(verification_results)

            if main_rational_present or attempt > max_attempts:
                break




        







    # 你之前的else语句处理网页请求失败的情况
    else:
        logging.error(f"网页请求失败，状态码: {response.status_code}")

    # 假设这是函数的结尾，根据你的上下文可能需要返回一些值
    return verification_results











# # # chatglm3出错，gpt35成功
# url = "https://www.snopes.com/fact-check/amy-schumer-falling-down-stairs/"

# verification_results = fetch_original_rational(url)

# logging.info("------------------------------------------------")
# logging.info(f"Verification original_rational: \n {verification_results}")

# # # all_paragraphs_text, extracted_complete_json = fetch_and_log_webpage_content(url)

# # # logging.info("Done.")
# # # logging.info("------------------------------------------------")
# # # logging.info("正文内容如下：")
# # # logging.info(all_paragraphs_text)
# # # logging.info("------------------------------------------------")
# # # logging.info("证据如下：")
# # # logging.info(extracted_complete_json)



# # print("Done.")
