
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



# 配置日志系统
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='get_free_evidence.log', filemode='a', encoding='utf-8')
# 首先清空日志文件
open('get_free_evidence.log', 'w').close()




import json



api_key = 'sk-T79RDgru0A5379d9d04cT3BlBKFJ7b21709730554F339d9c'


def gpt35_analysis(prompt):
    headers = {
        "Authorization": 'Bearer ' + api_key,
    }

    params = {
        "messages": [
            {
                "role": "system",
                "content": """To effectively manage the task at hand, you are tasked with synthesizing the relationship between the provided rationale and associated evidence concerning a specific claim, based on the content provided by the user. This involves understanding the essence of the article and articulating how the evidence supports or refutes the synthesized rationale. Follow these instructions:

- **Understanding User Inputs**: Prepare to receive pre-defined inputs concerning a claim's rationale and related external evidence directly from the user.

- **Synthesizing Relationships**: Your main task is to synthesize and explain the relationships between the rationale and the evidence. This involves creating a comprehensive explanation that integrates how the evidence supports or refutes the rationale, based on your understanding of the content.

- **Presentation and Formatting**: Present these relationships in a structured format. Clearly articulate the synthesized connection between the rationale and the evidence.

- **Output Requirements**: Format the response in JSON, organizing the information into a single field that corresponds to the synthesized relationship. The field should contain a comprehensive explanation that articulates the relationship between the rationale and the evidence.

By adhering to these guidelines, you will ensure that the relationships between the rationale and the evidence are displayed clearly and accurately, reflecting the synthesized connections as they are derived from the understanding of the source material. This approach is crucial for maintaining the clarity and integrity of the information."""

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



# # 调整evidence数组中的内容
# def adjust_evidence(evidence):




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






import requests
from bs4 import BeautifulSoup

def mocheg_fetch_evidences_and_all_links(url):
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

    evidences_and_links = []  # 初始化证据和链接列表
    seen_links = set()  # 用于存储已找到的链接以避免重复
    # 遍历所有的blockquote标签并提取文本和所有链接作为证据
    for block_tag in article_tag.find_all('blockquote'):
        evidence_text = block_tag.text.strip()  # 获取文本内容
        links = []

        # 获取cite属性中的链接并检查重复
        cite_link = block_tag.get('cite')
        if cite_link and cite_link not in seen_links:
            links.append(cite_link)
            seen_links.add(cite_link)

        # 获取所有<a>标签的href属性列表并检查重复
        for a_tag in block_tag.find_all('a'):
            href = a_tag.get('href')
            if href and href.startswith(('http://', 'https://')) and href not in seen_links:
                links.append(href)
                seen_links.add(href)

        evidences_and_links.append((evidence_text, links))

    response.close()  # 关闭HTTP响应
    return evidences_and_links  # 返回证据和所有链接的列表


def fetch_iframe_video_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    # 发送GET请求，获取页面内容
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    video_links = []  # 初始化视频链接列表
    # 遍历所有的iframe标签并提取data-src或src属性中的链接
    for iframe in soup.find_all('iframe'):
        video_link = iframe.get('data-src') or iframe.get('src')
        if video_link:
            video_links.append(video_link)

    response.close()  # 关闭HTTP响应
    return video_links  # 返回视频链接的列表


def check_and_correct_format(complete_json, rationale_key, i):
    # 检查并修正格式，确保complete_json为期望的单键值对格式，值为字符串，且以合适的单词开始
    expected_start_words = {"Relevant", "Irrelevant"}
    if complete_json and isinstance(complete_json, dict) and len(complete_json) == 1:
        key, value = next(iter(complete_json.items()))
        if isinstance(value, str):
            first_word = value.split('.')[0]  # 获取第一个单词，假设第一个句点之前为第一个单词
            if first_word in expected_start_words:
                expected_key = f"<{rationale_key},evidence{i+1}>"
                if key != expected_key:
                    complete_json[expected_key] = complete_json.pop(key)
                return complete_json, True
            else:
                logging.error(f"Response starts with an incorrect word: {first_word}. Expected one of {expected_start_words}.")
        else:
            logging.error("Value is not a simple string. The format is incorrect.")
    else:
        logging.error("JSON format is incorrect, empty, or contains multiple pairs.")
    return None, False




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

        original_rationales = fetch_original_rational(url)
        logging.info("------------------------------------------------")
        logging.info(f"original_rationales: \n {original_rationales}")
        logging.info("------------------------------------------------")

        summary_rationales = fetch_summary_rational(url)
        logging.info("------------------------------------------------")
        logging.info(f"summary_rationales: \n {summary_rationales}")
        logging.info("------------------------------------------------")

        evidences = mocheg_fetch_evidences_and_all_links(url)
        logging.info("------------------------------------------------")
        logging.info(f"evidences: \n {evidences}")
        logging.info("------------------------------------------------")

        relationships = []
        # 针对每一个evidence，生成一个prompt，调用gpt35_analysis函数，获取relationship_with_evidence
        for i, (evidence, links) in enumerate(evidences):

            for rationale_key, rationale_text in original_rationales.items():
                

                prompt = f"""
The objective is to rigorously analyze the direct relationship between the evidence and the claims or fact-checking rationales in the fact-checking article. Identify the relationship between the evidence and the claims or fact-checking rationales. Specifically, determine whether the evidence is the source post of a claim or if it supports a particular fact-checking rationale, and identify which reason or reasons it supports. Here's the specific task:

- **Input Information**: 
  - **Claim**: {claim_content}
  - **Rating**: {rating_content}
  - **Rationales**: Provided as a dictionary with each `rationale_key` associated with its `rationale_text`, formed by combining two different sources of rationale details. The combined dictionary is `combined_rationales`. {combined_rationales}
  - **Evidence**: {evidence}
  - **Article Content**: {article_content}

- **Synthesizing Relationships**: 
  - Evaluate whether the relationship between the claim or rationale and the evidence is exceptionally direct based on the content of the article:
    - **Relevant Evidence**: If the evidence directly supports the content of the claim or matches one of the rationale details, classify this as 'Relevant' and provide a detailed explanation of how the evidence, as presented in the article, supports the claim or the most closely related rationale. The relationship must be direct, explicit, and clear.
    - **Irrelevant Evidence**: If the evidence does not directly support the claim or does not match any of the rationale details, classify this as 'Irrelevant'.

- **Determination of Best Match**:
  - For each rationale provided in `combined_rationales`, compare the evidence against the rationale detail.
  - Identify the `rationale_key` and `rationale_text` that best matches the evidence based on how directly the evidence supports or contradicts the rationale detail.

- **Response Requirements**:
  - 'Relevant' if the evidence directly supports the claim or matches the best found rationale, clearly and explicitly describing the same event, fact, or thing.
  - 'Irrelevant' if the content or the topic addressed by the claim or rationale and the evidence is different, or if their connection is not directly supportive.

- **Output Format**:
  - If a direct and clear relationship is identified, the output format should be:
    {{
    "<best_match_rationale_key,evidence{i+1}>": "Your primary task is to select the most suitable rationale from the given `combined_rationales` and fill it in as the `best_match_rationale_key` in "<best_match_rationale_key, evidence {i+1}>". Then, provide detailed and specific reasons why this evidence directly supports or is closely related to the chosen rationale. Ensure that the explanation clearly demonstrates the direct and explicit connection between the evidence and the rationale, focusing on the same event, fact, or thing described in both the evidence and the rationale."
    }}
  - If no direct and clear relationship is identified between any rationales and the evidence, the output format should be:
    {{
    "<all_rationale_key,evidence{i+1}>": "Irrelevant"
    }}

Ensure to avoid any classification based on indirect, vague, or ambiguous relationships. Focus strictly on very direct and explicit connections as presented in the article.
"""
            

                # 提取证据
                gpt35_relationship_with_evidence= gpt35_analysis(prompt)

                complete_json = extract_complete_json(gpt35_relationship_with_evidence)

                logging.info("------------------------------------------------")

                logging.info(f"The {i} relationship_with_evidence of Evidence: \n {complete_json}")
                logging.info("------------------------------------------------")


                # 检查并可能修正格式
                complete_json, is_correct = check_and_correct_format(complete_json, rationale_key, i)
                max_attempts = 5
                attempts = 0
                # 如果complete_json格式不正确或为空，则重新生成和检查，直至符合格式要求
                while not is_correct:
                    attempts += 1
                    gpt35_relationship_with_evidence = gpt35_analysis(prompt)
                    complete_json = extract_complete_json(gpt35_relationship_with_evidence)
                    logging.info("------------------------------------------------")
                    logging.info(f"The {i} relationship_with_evidence of Evidence: \n {complete_json}")
                    logging.info("------------------------------------------------")
                    complete_json, is_correct = check_and_correct_format(complete_json, rationale_key, i)

                    if attempts > max_attempts:
                        logging.error(f"Failed to generate correct JSON format after {max_attempts} attempts.")
                        break

                relationships.append(complete_json)






            for rationale_key, rationale_text in summary_rationales['detailed_reasons'].items():




                prompt = f"""The objective is to rigorously analyze the direct relationship between the evidence and the claims or fact-checking rationales in the fact-checking article. Identify the relationship between the evidence and the claims or fact-checking rationales. Specifically, determine whether the evidence is the source post of a claim or if it supports a particular fact-checking rationale, and identify which reason or reasons it supports. Here's the specific task:
- **Input Information**: Input Information: Provide the claim, its rating, a rationale detail, and the relevant evidence. Additionally, include the full content of the article from which the evidence is derived.
- **Synthesizing Relationships**: Evaluate whether the relationship between the claim or rationale and the evidence is exceptionally direct based on the content of the article:
Relevant Evidence: If the evidence directly supports the content of the claim or matches the rationale detail, classify this as 'Relevant' and provide a detailed explanation of how the evidence, as presented in the article, supports the claim or rationale. Note that the relationship must be direct, explicit, and clear, not indirect or implied. The evidence and rationale must describe the same event, fact, or thing to be considered directly related. Focus mainly on the context of the current evidence position within the surrounding text and do not confuse it with other irrelevant evidence information from different parts of the article. Only classify as 'Relevant' when there is a high level of confidence in the direct relevance.And the reason for the final output of the Relevant is simple, intuitive, and does not cause ambiguity
Irrelevant Evidence: If the evidence does not directly support the claim or does not match the rationale detail, classify this as 'Irrelevant'. Remember to just answer with the word "Irrelevant" without any additional content. Focus mainly on the context of the current evidence position within the surrounding text and do not confuse it with other irrelevant evidence information from different parts of the article. If the relationship is not sufficiently direct and confident, it should be classified as 'Irrelevant'.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Rationale Detail:** {rationale_text}
**Evidence:** {evidence}
**Article Content:** {article_content}
The response should classify the relationship between the claim or rationale and the evidence, based on the content of the article, with absolute precision:
- 'Relevant' if the evidence directly supports the claim or matches the rationale, taking into account the context of the current evidence position and its surrounding text, and avoiding confusion with other irrelevant evidence information. The evidence and rationale must be directly related, describing the same event, fact, or thing, with an explicit and obvious connection, not an indirect or implied one. Only classify as 'Relevant' when there is a high level of confidence in the direct relevance. The reason for emphasizing the Relevance of the final output is that it is easy to understand, intuitive, and does not cause ambiguity.
- 'Irrelevant' if the content or the topic addressed by the claim or rationale and the evidence is different, or if their connection is not directly supportive, taking into account the context of the current evidence position and its surrounding text, and avoiding confusion with other irrelevant evidence information. If the relationship is not the most direct, obvious, and explicit, it should be classified as 'Irrelevant'.

Ensure to avoid any classification based on indirect, vague, or ambiguous relationships.
**Specific output requirement**: For responses classified as 'Irrelevant', only the word "Irrelevant" should be used, with no further explanation. For 'Relevant', first state the classification followed by a detailed explanation.
When searching for relationships in the original text, focus mainly on the context of the current evidence position and do not confuse it with other irrelevant evidence information
**Specified output format in JSON:**
{{
"<{rationale_key},evidence{i+1}>": "First and foremost, summarize as 'Relevant' or 'Irrelevant', answer one of these two words. Provide an explanation only if the relationship is 'Relevant'. If 'Irrelevant', no further details should be provided.And it is important to note that the reason for the final output is simple, intuitive, and does not cause ambiguity. The reason for emphasizing the Relevance of the final output is that it is easy to understand, intuitive, and does not cause ambiguity"
}}
Example of final output content:
{{
"<reason1,evidence1>": "Relevant. The evidence directly supports the claim by providing specific data that aligns with the rationale provided in the article."
}}
Reminder: Focus strictly on very direct and explicit connections as presented in the article. Classify all other relationships as 'Irrelevant' and provide explanations only for very direct 'Relevant' relationships.
"""



                # Call GPT-3 or relevant analysis function
                gpt_relationship_with_evidence = gpt35_analysis(prompt)
                complete_json = extract_complete_json(gpt_relationship_with_evidence)

                # Logging and storing each relationship result
                logging.info("------------------------------------------------")
                logging.info(f"The relationship between {rationale_key} and evidence {i}: \n {complete_json}")
                logging.info("------------------------------------------------")


                # 检查并可能修正格式
                complete_json, is_correct = check_and_correct_format(complete_json, rationale_key, i)
                max_attempts = 5
                attempts = 0
                # 如果complete_json格式不正确或为空，则重新生成和检查，直至符合格式要求
                while not is_correct:
                    attempts += 1
                    gpt35_relationship_with_evidence = gpt35_analysis(prompt)
                    complete_json = extract_complete_json(gpt35_relationship_with_evidence)
                    logging.info("------------------------------------------------")
                    logging.info(f"The {i} relationship_with_evidence of Evidence: \n {complete_json}")
                    logging.info("------------------------------------------------")
                    complete_json, is_correct = check_and_correct_format(complete_json, rationale_key, i)

                    if attempts > max_attempts:
                        logging.error(f"Failed to generate correct JSON format after {max_attempts} attempts.")
                        break

                relationships.append(complete_json)


        

        
        logging.info("------------------------------------------------")
        logging.info(f"relationships: \n {relationships}")
        logging.info("------------------------------------------------")

        # iframe视频链接
        video_links = fetch_iframe_video_links(url)
        logging.info("------------------------------------------------")
        logging.info(f"iframe video_links: \n {video_links}")
        logging.info("------------------------------------------------")

        result_data = {}  # 初始化最终存储的字典
        result_data['url'] = url
        result_data['claim'] = claim_content
        result_data['rating'] = rating_content
        result_data['content'] = article_content
        result_data['original_rationales'] = original_rationales
        result_data['summary_rationales'] = summary_rationales
        result_data['evidences'] = evidences
        # tagged_evidences = {f"evidence{i}": evidence for i, evidence in enumerate(evidences)}
        tagged_evidences = {"num_of_evidence": len(evidences)}  # 创建字典并添加计数键
        tagged_evidences.update({f"evidence{i+1}": evidence for i, evidence in enumerate(evidences)})  # 使用推导式更新字典

        result_data['evidences'] = tagged_evidences
        result_data['relationship_with_evidence'] = relationships
        # 在other中的iframe_video_links键中添加视频链接
        result_data['other'] = {"iframe_video_links": video_links}


        # json文件名字，根据url最后的自动提取，比如说https://www.snopes.com/fact-check/haley-911-sept-10/，那么json文件名字就是haley-911-sept-10.json
        json_file_name = url.split('/')[-2] + '.json'
        with open(json_file_name, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        


    # 你之前的else语句处理网页请求失败的情况
    else:
        logging.error(f"网页请求失败，状态码: {response.status_code}")

    # 假设这是函数的结尾，根据你的上下文可能需要返回一些值
    # return all_paragraphs_text, complete_json



# # # chatglm3出错，gpt35成功
url = "https://www.snopes.com/fact-check/haley-911-sept-10/"

# url = "https://www.snopes.com/fact-check/israel-aid-gaza-moldova/"

url = "https://www.snopes.com/fact-check/swift-trump-won-grammys/"

# url = "https://www.snopes.com/fact-check/trump-uaw-raises-2008/"

# url ="https://www.snopes.com/fact-check/kim-jong-un-watching-volleyball/"

# url = "https://www.snopes.com/fact-check/texas-mexico-border-tanks/"

# url = "https://www.snopes.com/fact-check/amy-schumer-falling-down-stairs/"

# url = "https://www.snopes.com/fact-check/texas-mexico-border-tanks/"

# url = "https://www.snopes.com/fact-check/ice-helix-polar-vortex-video/"


# url = "https://www.snopes.com/fact-check/video-scuba-diver-swimming-dinosaur/"

# url = "https://www.snopes.com/fact-check/haiti-cannibalism-video/"

# fetch_relationship_with_evidence(url)



# 你的URL列表
# urls = [
#     "https://www.snopes.com/fact-check/haley-911-sept-10/",
#     "https://www.snopes.com/fact-check/israel-aid-gaza-moldova/",
#     "https://www.snopes.com/fact-check/swift-trump-won-grammys/",
#     "https://www.snopes.com/fact-check/trump-uaw-raises-2008/",
#     "https://www.snopes.com/fact-check/biden-nibble-girl-finland/",
#     "https://www.snopes.com/fact-check/texas-mexico-border-tanks/",
#     "https://www.snopes.com/fact-check/ribbon-worm-video/",
#     "https://www.snopes.com/fact-check/trump-911-inside-job/",
#     "https://www.snopes.com/fact-check/kim-jong-un-watching-volleyball/",
#     "https://www.snopes.com/fact-check/taylor-swift-buffalo-bills/",
#     "https://www.snopes.com/fact-check/ice-helix-polar-vortex-video/",
#     "https://www.snopes.com/fact-check/miami-plane-fire-after-takeoff-video/",
#     # "https://www.snopes.com/fact-check/meryl-streep-at-beatles-concert/",
#     # "https://www.snopes.com/fact-check/michael-moore-supports-trump/",
#     # "https://www.snopes.com/fact-check/us-cargo-ship-houthi-missile/",
#     # "https://www.snopes.com/fact-check/palestinian-baby-dolls-israel/",
#     # "https://www.snopes.com/fact-check/video-woman-attacked-paranormal-forces/",
#     # "https://www.snopes.com/fact-check/biden-border-fence-2007/",
#     # "https://www.snopes.com/fact-check/italy-nazi-rally/",
#     # "https://www.snopes.com/fact-check/god-made-trump-video/",
#     # "https://www.snopes.com/fact-check/jo-koy-taylor-swift/",
#     # "https://www.snopes.com/fact-check/young-girls-epsteins-island/",
#     # "https://www.snopes.com/fact-check/trump-perry-school-shooting/",
#     # "https://www.snopes.com/fact-check/putin-mcgregor-warning/",
#     # "https://www.snopes.com/fact-check/kim-putin-toast/",
#     # "https://www.snopes.com/fact-check/bill-clinton-hospitalized-epstein/",
#     # "https://www.snopes.com/fact-check/amy-schumer-falling-down-stairs/",
#     # "https://www.snopes.com/fact-check/ribbon-worm-video/"
# ]


urls = [
    "https://www.snopes.com/fact-check/haley-911-sept-10/",
    "https://www.snopes.com/fact-check/israel-aid-gaza-moldova/",
    "https://www.snopes.com/fact-check/swift-trump-won-grammys/",
    "https://www.snopes.com/fact-check/video-scuba-diver-swimming-dinosaur/",
    "https://www.snopes.com/fact-check/biden-nibble-girl-finland/",
    "https://www.snopes.com/fact-check/texas-mexico-border-tanks/",
    "https://www.snopes.com/fact-check/trump-911-inside-job/",
    "https://www.snopes.com/fact-check/kim-jong-un-watching-volleyball/",
    "https://www.snopes.com/fact-check/taylor-swift-buffalo-bills/",
    "https://www.snopes.com/fact-check/ice-helix-polar-vortex-video/",
    "https://www.snopes.com/fact-check/miami-plane-fire-after-takeoff-video/",
    "https://www.snopes.com/fact-check/meryl-streep-at-beatles-concert/",
    "https://www.snopes.com/fact-check/michael-moore-supports-trump/",
    "https://www.snopes.com/fact-check/us-cargo-ship-houthi-missile/",
    "https://www.snopes.com/fact-check/palestinian-baby-dolls-israel/",
    "https://www.snopes.com/fact-check/video-woman-attacked-paranormal-forces/",
    "https://www.snopes.com/fact-check/biden-border-fence-2007/",
    "https://www.snopes.com/fact-check/italy-nazi-rally/",
    "https://www.snopes.com/fact-check/god-made-trump-video/",
    "https://www.snopes.com/fact-check/jo-koy-taylor-swift/",
    "https://www.snopes.com/fact-check/young-girls-epsteins-island/",
    "https://www.snopes.com/fact-check/trump-perry-school-shooting/",
    "https://www.snopes.com/fact-check/putin-mcgregor-warning/",
    "https://www.snopes.com/fact-check/kim-putin-toast/",
    "https://www.snopes.com/fact-check/bill-clinton-hospitalized-epstein/",
    "https://www.snopes.com/fact-check/amy-schumer-falling-down-stairs/",
    "https://www.snopes.com/fact-check/haiti-cannibalism-video/"
]


i = 0
# # 获得28个URL的相关性和证据
for url in urls:
    i += 1
    print(i)

    json_file_name = url.split('/')[-2] + '.json'
    if os.path.exists(json_file_name):
        print(f"已经存在{json_file_name}文件")
        logging.info(f"已经存在{json_file_name}文件")
        continue

    print(f"Fetching relationship with evidence for URL: {url}")
    logging.info("***************************")
    logging.info(f"Fetching relationship with evidence for URL: {url}")
    fetch_relationship_with_evidence(url)
    time.sleep(10)  # 休眠10秒以避免频繁请求网站