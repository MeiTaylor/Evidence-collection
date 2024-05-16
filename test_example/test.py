import requests
from bs4 import BeautifulSoup
import logging

api_key = 'sk-T79RDgru0A5379d9d04cT3BlBKFJ7b21709730554F339d9c'



def fetch_article_content(url):
    

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



def gpt35_analysis(prompt):
    headers = {
        "Authorization": 'Bearer ' + api_key,
    }

    params = {
        "messages": [
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


    evidences = mocheg_fetch_evidences_and_all_links(url)

    for evidence, links in evidences:
        print(f"Evidence: {evidence}")
        print("Links:")
        for link in links:
            print(link)
        print()
        print("----------------------------------------")
        print()
        


    # 针对每一个evidence，生成一个prompt，调用gpt35_analysis函数，获取relationship_with_evidence
    for i, (evidence,links) in enumerate(evidences):

#         prompt = f"""You will be given a Claim, Rating, Evidence, and Article Content from a Snopes fact-checking article. Your task is to determine if the Evidence is the Original Post.

# **Definition of Original Post:** The Original Post is the initial statement or information that was published, which often consists of a rumor, misleading information, or content that requires fact-checking. It is the main subject that Snopes analyzes and verifies. The Original Post typically originates from sources such as social media posts, online articles, news reports, or user submissions.

# **Claim:** {claim_content}
# **Rating:** {rating_content}
# **Evidence:** {evidence}
# **Article Content:** {article_content}

# **Task Requirements:**
# 1. Carefully read the Claim, Rating, and Article Content.
# 2. Pay special attention to the context and text surrounding the Evidence within the Article Content, especially the sections immediately before and after the Evidence.
# 3. Based on the provided definition of Original Post, determine whether the Evidence is the Original Post.
# 4. Answer only with "yes" or "no".

# Is the Evidence the Original Post? Answer "yes" or "no".And provide detailed and specific analysis to support your answer."""


        prompt = f"""You will be given a Claim, Rating, reference material such as original post and evidence, and Article Content which are all extracted from a Snopes fact-checking article. Your task is to determine if the reference material is about the Original Post where the claim comes from or other evidence material used to reason about the factuality of the claim.
**Definition of Original Post:** The Original Post is the initial statement or information that was published, which often consists of a rumor, misleading information, or content that requires fact-checking. It is the main subject that Snopes analyzes and verifies. The Original Post typically originates from sources such as social media posts, online articles, news reports, or user submissions.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Reference material:** {evidence}
**Article Content:** {article_content}
**Task Requirements:**
1. Carefully read the Claim, Rating, and Article Content.
2. Pay special attention to the location, context and text surrounding the Reference material within the Article Content, especially the sections immediately before and after the Evidence.
3. Based on the provided definition of Original Post, determine whether the Reference material is the Original Post or other evidence used to reason the factuality of the claim.
4. Answer only with "yes" or "no". 
Is the Evidence the Original Post? Answer "yes" or "no".And provide detailed and specific analysis to support your answer."""



#         prompt = f"""You will be given a Claim, Rating, reference material which could be original post or evidence, and Article Content which are all extracted from a Snopes fact-checking article. Your task is to determine if the reference material is about the Original Post where the claim comes from or other evidence material used to reason about the factuality of the claim.
# **Definition of Original Post:** The Original Post is often described in the first part in the fact-checking article to state the source of the claim to be verifeid. The Original Post typically can originate from various sources such as social media posts, online articles, news reports, or other user submissions of various online platforms. 
# **Claim:** {claim_content}
# **Rating:** {rating_content}
# **Reference material:** {evidence}
# **Article Content:** {article_content}
# **Task Requirements:**
# 1. Carefully read the Claim, Rating, and Article Content.
# 2. Pay special attention to the location, context and text surrounding the Reference material within the Article Content, especially the sections immediately before and after the Evidence.
# 3. Based on the provided definition of Original Post, determine whether the Reference material is the Original Post or other evidence used to reason the factuality of the claim.
# 4. Answer only with "yes" or "no". 
# Is the Evidence the Original Post? Answer "yes" or "no".And provide detailed and specific analysis to support your answer."""

        relationship_with_evidence = gpt35_analysis(prompt)

        print(f"Is Evidence {i+1} an original post: {relationship_with_evidence}")
        print("------------------------------------------------")


url = "https://www.snopes.com/fact-check/ice-helix-polar-vortex-video/"

# url = "https://www.snopes.com/fact-check/video-scuba-diver-swimming-dinosaur/"

url = "https://www.snopes.com/fact-check/video-woman-attacked-paranormal-forces/"

fetch_relationship_with_evidence(url)


