
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

from code.evidence_relete.get_original_rational import fetch_original_rational
from get_summary_rational import fetch_summary_rational



# # 配置日志系统
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
                "content": """To effectively manage the task at hand, you are tasked with identifying and presenting the relationship between the provided rationale and associated evidence concerning a specific claim. This involves understanding and clearly articulating how each piece of evidence supports or refutes the rationale based on the original texts provided by the user. Follow these instructions:

- **Understanding User Inputs**: Prepare to receive pre-defined inputs concerning a claim's rationale and related external evidence directly from the user.

- **Identifying Relationships**: Your main task is to identify and explain the relationships between the rationale and the evidence as depicted in the original texts. This involves pinpointing specific sentences or segments that clearly demonstrate these relationships.

- **Presentation and Formatting**: Present these relationships in a structured format. Clearly distinguish between the rationale and the evidence, and articulate the connection between them as derived from the original texts.

- **Output Requirements**: Format the response in JSON, organizing the information into labeled fields that correspond to the identified relationships. Each field should contain the exact sentence from the original text that illustrates the relationship between the rationale and the evidence.

By adhering to these guidelines, you will ensure that the relationships between the rationale and the evidence are displayed clearly and accurately, reflecting the connections as they are described in the original source material. This precise approach is crucial for maintaining the integrity and accuracy of the information."""
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



def mocheg_fetch_evidences(url):
    # 定义请求头，模仿浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    # 发送GET请求，获取页面内容
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    article_tag = soup.find('article', attrs={'id': 'article-content'})
    # 如果找不到文章内容，返回空列表
    if not article_tag:
        return []

    evidences = []  # 初始化证据列表
    # 遍历所有的blockquote标签并提取文本作为证据：

    for block_tag in article_tag.find_all(name='blockquote'):
        evidences.append(block_tag.text.strip())

    response.close()  # 关闭HTTP响应
    return evidences  # 返回提取的证据列表


def fetch_relationship_with_evidence(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取并记录claim及其内容
        claim_content = soup.select(".claim_cont")[0].text.strip()

        
        # 提取并记录Rating的类别
        rating_content = soup.select(".rating_title_wrap")[0].text.strip()[:-18].strip()
        
        # 提取并记录article正文的所有内容
        article_content = fetch_article_content(url)

        original_rationals = fetch_original_rational(url)
        logging.info("------------------------------------------------")
        logging.info(f"original_rationals: \n {original_rationals}")
        logging.info("------------------------------------------------")

        summary_rationals = fetch_summary_rational(url)
        logging.info("------------------------------------------------")
        logging.info(f"summary_rationals: \n {summary_rationals}")
        logging.info("------------------------------------------------")

        evidences = mocheg_fetch_evidences(url)
        logging.info("------------------------------------------------")
        logging.info(f"evidences: \n {evidences}")
        logging.info("------------------------------------------------")


        # 针对每一个evidence，生成一个prompt，调用gpt35_analysis函数，获取relationship_with_evidence
        for i, evidence in enumerate(evidences):

            prompt = f"""Prompt:
"The objective is to analyze content from an article related to a specific claim, focusing specifically on the relationship between two types of rationales (original and summary) and the evidence presented. You are required to provide a single comprehensive explanation that encapsulates how both types of rationales relate to the evidence, using direct quotations from the article for the original rationales and synthesized reasoning for the summary rationales. Here's what you need to do:
- **Input Information**: Provide the claim, its rating, specific segments of the article content that serve as original rationales, a synthesized summary of rationales based on the entire article content, and the relevant evidence.
- **Identifying Relationships**: Your main task is to synthesize the relationships between both types of rationales and the evidence into one comprehensive explanation. This involves using specific sentences or segments from the article that demonstrate how the evidence supports or refutes each original rationale and a summarized explanation for how it relates to the summary rationales.
The task demands a meticulous extraction of text segments, ensuring they are presented in their original form as direct quotations from the article. This approach underscores the necessity for clarity and fidelity to the source material.

**Claim:** {claim_content}
**Rating:** {rating_content}
**Article Content:** {article_content}
**Original Rationales:** {original_rationals}
**Summary Rationales:** {summary_rationals}
**Evidence:** {evidence}
The response should provide one comprehensive explanation that articulates the relationships between the rationales (both original and synthesized) and the evidence, using exact quotes from the article for original rationales and summarized reasoning for summary rationales.
**Specified output format in JSON:**
{{
"relationship_with_evidence": "Comprehensive explanation of how the rationales (both original and synthesized) relate to the evidence, using exact quotes where applicable"
}}
Reminder: The final output must contain a single comprehensive explanation that accurately reflects the relationship as it appears based on the original text and synthesized understanding, using direct quotes from the original text for original rationales and synthesized summaries for summary rationales, with no alterations."
This task requires careful extraction of text fragments to ensure that they directly reference the article in its original form. That is to say, the final answer needs to be based on the original words and sentences in the original text, without any summary or modification"""



            # 提取证据
            gpt35_relationship_with_evidence= gpt35_analysis(prompt)



            complete_json = extract_complete_json(gpt35_relationship_with_evidence)

            logging.info("------------------------------------------------")

            logging.info(f"The {i} relationship_with_evidence of Evidence: \n {complete_json}")
            logging.info("------------------------------------------------")




            # # 调用 verify_model_output 函数
            # # 验证证据
            verification_results = verify_model_output(complete_json, article_content)

            logging.info("------------------------------------------------")
            logging.info(f"Verification Results: \n {verification_results}")

            logging.info("------------------------------------------------")


    # 你之前的else语句处理网页请求失败的情况
    else:
        logging.error(f"网页请求失败，状态码: {response.status_code}")

    # 假设这是函数的结尾，根据你的上下文可能需要返回一些值
    # return all_paragraphs_text, complete_json






# # # chatglm3出错，gpt35成功
url = "https://www.snopes.com/fact-check/haley-911-sept-10/"

fetch_relationship_with_evidence(url)

