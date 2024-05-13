# Evidence-collection

#### 步骤 1: 使用Mocheg数据集方式，按照网页标签收集证据 (Evidence)

1. 发送 HTTP 请求并且解析网页内容，从blockquote标签内提取证据

#### 步骤 2: 使用 GPT 来找出理由 (Reason)

1. **提取原始理由 (Original Rationals)**：直接从网页中抽取与主张相关的原始理由，可能包括直接引用或陈述性内容。
2. **生成总结理由 (Summary Rationals)**：利用 GPT 模型根据文章内容生成一个精简的理由总结。这通常需要将相关内容作为提示文本（prompt）输入到模型中，并请求一个简短的总结。

#### 步骤 3: 用 GPT 寻找理由和证据之间的关系

1. **构建关系分析的 Prompt**：为每个证据项创建一个包含以下内容的 prompt：
   - **主张 (Claim)**：文章中的主张或论点。
   - **原始理由 (Original Rationals)** 和 **总结理由 (Summary Rationals)**。
   - **证据 (Evidence)**：当前正在分析的证据。
   - 请求模型分析并解释理由如何支持或反驳证据。
2. **模型分析**：将每个 prompt 发送到 GPT 模型。模型根据提供的信息分析并生成一个解释，说明理由与证据之间的关系。
3. **收集和存储分析结果**：将每个证据的分析结果存储在一个列表中，之后可以整理成 JSON 格式以便进一步使用或存档。





#### 以下是每一部分的Prompt的详细说明

System role: Allows you to specify the way the model answers questions. Classic example: “You are a helpful assistant.”

User role: Equivalent to the queries made by the user.


##### 提取原始理由 (Original Rationals)

这一部分我们主要是在System Message中强调了“提取理由：重点在文章中找到明确解释claim的Rating_content背后原因的句子。寻找直接说明如此评估的原因的句子，确保这些回答清楚地反映出rating——content的理由"

并且还在用户输入的Prompt中强调了Rational的定义：According to the definition, 'rationale' refers to a paragraph that summarizes the evidence based on the predicted truthfulness label and explains the ruling process. 

并且最重要的一点是：在两部分中都加以强调要是原文中的原字原句


System Message：

```
""""To effectively analyze the provided paragraphs from an article in relation to a specific claim and its assigned rating, you are tasked with identifying segments that serve as the 'rationale' for the rating. Each identified segment must be quoted directly from the text without any modification. Follow these detailed instructions for accomplishing this task:

- **Understanding the Claim and Rating**: Start by comprehending the claim and its corresponding rating. Grasping the context and rationale behind this rating is essential for identifying relevant text segments.

- **Extracting the Rationale**: Focus on finding sentences within the article that explicitly explain the reasoning behind the claim's rating. Look for sentences that directly address why the claim has been evaluated as such, ensuring these excerpts clearly reflect the rationale for the rating.

- **Adherence to Original Text**: It is crucial that all extracted text segments—representing the rationale—are quoted verbatim. Avoid any deviation from the original text such as paraphrasing or summarizing.

- **Presentation and Formatting**: Present your findings in a structured format. Each identified rationale should be clearly cited and presented as found in the original text.

- **Output Requirements**: Format your response in JSON, with fields labeled 'rationale1', 'rationale2', etc., depending on the number of rationales extracted. Each field should contain the exact sentence from the article that illustrates the rationale for the rating.

By following these guidelines, you will be able to provide a clear, structured, and precise analysis that reflects the reasons behind the claim's rating based on the original article text."
"""
```

用户输入Prompt：

```
        prompt = f"""Prompt:
"The objective is to analyze a series of paragraphs from an article to support or refute a given claim. This analysis requires identifying specific segments within the text classified as 'rationale' for the rating. These segments should be original, unaltered sentences from the article:
- 'Rationale': Please identify at least one paragraph in the article that serves as the 'rationale' for the rating. According to the definition, 'rationale' refers to a paragraph that summarizes the evidence based on the predicted truthfulness label and explains the ruling process. This paragraph should clearly demonstrate why, based on the provided evidence and analysis, the assertion has been assigned this specific truthfulness rating.
The task demands a meticulous extraction of text segments, ensuring they are presented in their original form as direct quotations from the article. This approach underscores the necessity for clarity and fidelity to the source material.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Paragraphs:** {article_content}
The rationale must be an exact quotation from the text, clearly distinguished in the response to demonstrate the foundation of the rating provided. It is imperative that the rationale provided in the JSON output is an exact, unaltered replica of the sentences found in the original text, without any alterations, rephrasing, or summarization.
**Specified output format in JSON:**
{{
"rationale1": "Exact original sentence from the text reflecting the rationale for the '{rating_content}' rating",
"rationale2": ············
}}
Reminder: The final output must strictly contain the original sentences for the rationale directly extracted from the paragraphs, exactly as they appear in the source, without any alterations, rephrasing, or summarization."
"""
```







##### 生成总结理由 (Summary Rationals)

这一部分基本就是通过给出Rational的定义，让GPT根据Claim、rating_content、article_content总结出当前的snopes post的Rational

System Message：

```
""""To effectively analyze the provided paragraphs from an article in relation to a specific claim and its assigned rating, you are tasked with summarizing a 'rationale' that supports or refutes the claim based on the information presented. This task involves synthesizing the key points into a concise rationale rather than quoting directly from the text. Follow these detailed instructions for accomplishing this task:

- **Understanding the Claim and Rating**: Start by comprehending the claim and its corresponding rating. Understanding the context of the claim and the reasons provided in the text for this rating is essential for synthesizing a valid rationale.

- **Synthesizing the Rationale**: Focus on integrating various points within the article that collectively explain the reasoning behind the claim's rating. Derive a coherent summary that encapsulates why the claim has been evaluated in such a manner, based on the evidence and arguments presented throughout the text.

- **Adherence to the Essence of the Text**: While direct quotations are not required, it is crucial that the synthesized rationale accurately reflects the arguments and evidence found in the text. Ensure that the summary remains true to the original content’s intent and factual basis.

- **Presentation and Formatting**: Present your synthesized findings in a clear and structured format. The rationale should be concise and reflect a comprehensive understanding of the text.

- **Output Requirements**: Format your response in plain text or JSON, labeling the field as 'synthesized_rationale'. This field should contain a synthesized summary that clearly articulates the rationale for the rating based on the analysis of the text.

By following these guidelines, you will be able to provide a clear, structured, and insightful synthesis that captures the essence of the reasons behind the claim's rating based on the article's content."""

```

用户输入的Prompt：

```
        prompt = f""""The objective is to analyze a series of paragraphs from an article to support or refute a given claim. This analysis requires synthesizing a 'rationale' from the content that supports the given rating, rather than directly quoting sentences from the article:
- 'Rationale': Based on the entire content provided, synthesize a rationale that explains why the claim has been assigned this specific truthfulness rating. Consider the key arguments, evidence, and data presented throughout the text and integrate them into a comprehensive rationale that articulates the judgment process.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Paragraphs:** {article_content}
The response should demonstrate a clear and insightful understanding of the text, forming a synthesized rationale that aligns with the overall content and intent of the article. This summary should reflect a high level of analytical thought and provide a well-rounded explanation of why the claim has been rated as it has.
**Specified output format in JSON (or text, if preferred):**
{{
"synthesized_rationale": "A synthesized summary that clearly articulates the rationale for the '{rating_content}' rating based on a comprehensive analysis of the text."
}}
Reminder: The final output must present a synthesized summary that captures the essence of the rationale without directly quoting from the article. The summary should be original, yet closely aligned with the content and analysis provided in the text."
"""
```





##### 用 GPT 寻找理由和证据之间的关系

这一部分本来也是分为找到原文和使用GPT总结两种方式的，但是试了不同的Prompt发现，让GPT找到跟Evidence和所有Rational有关联的原文比较困难，遂采用使用GPT总结的方法



这一部分的Prompt主要强调的就是：综合和解释基本原理和证据之间的关系，创建一个全面的解释，整合证据如何支持或反驳理由。



System Message：

```
"""To effectively manage the task at hand, you are tasked with synthesizing the relationship between the provided rationale and associated evidence concerning a specific claim, based on the content provided by the user. This involves understanding the essence of the article and articulating how the evidence supports or refutes the synthesized rationale. Follow these instructions:

- **Understanding User Inputs**: Prepare to receive pre-defined inputs concerning a claim's rationale and related external evidence directly from the user.

- **Synthesizing Relationships**: Your main task is to synthesize and explain the relationships between the rationale and the evidence. This involves creating a comprehensive explanation that integrates how the evidence supports or refutes the rationale, based on your understanding of the content.

- **Presentation and Formatting**: Present these relationships in a structured format. Clearly articulate the synthesized connection between the rationale and the evidence.

- **Output Requirements**: Format the response in JSON, organizing the information into a single field that corresponds to the synthesized relationship. The field should contain a comprehensive explanation that articulates the relationship between the rationale and the evidence.

By adhering to these guidelines, you will ensure that the relationships between the rationale and the evidence are displayed clearly and accurately, reflecting the synthesized connections as they are derived from the understanding of the source material. This approach is crucial for maintaining the clarity and integrity of the information."""

```



5.13更新：

用户输入Prompt：

```
                prompt = f"""The objective is to rigorously analyze the direct relationship between a claim or rationale and provided evidence. Here's the specific task:
- **Input Information**: Provide the claim, its rating, a rationale detail, and the relevant evidence.
- **Synthesizing Relationships**: Evaluate whether the relationship between the claim or rationale and the evidence is exceptionally direct:
- If the evidence directly supports the content of the claim or matches the rationale detail, classify this as 'Relevant' and provide a detailed explanation of how the evidence supports the claim or rationale.
- If the evidence does not directly support the claim or does not match the rationale detail, classify this as 'Irrelevant'. Remember to just answer with the word "Irrelevant" without any additional content.
- Any case where the evidence and rationale do not address the same topic or their meanings do not directly contradict should be classified as 'irrelevant'.
**Claim:** {claim_content}
**Rating:** {rating_content}
**Rationale Detail:** {rationale_text}
**Evidence:** {evidence}
The response should classify the relationship between the claim or rationale and the evidence with absolute precision:
- 'Relevant' if the evidence directly supports the claim or matches the rationale.
- 'Irrelevant' if the content or the topic addressed by the claim or rationale and the evidence is different, or if their connection is not directly supportive.
Ensure to avoid any classification based on indirect, vague, or ambiguous relationships.
**Specific output requirement**: For responses classified as 'Irrelevant', only the word "Irrelevant" should be used, with no further explanation. For 'Relevant', first state the classification followed by a detailed explanation.
**Specified output format in JSON:**
{{
"<{rationale_key},evidence{i+1}>": "First and foremost, summarize as 'Relevant' or 'Irrelevant', answer one of these two words. Provide an explanation only if the relationship is 'Relevant'. If 'Irrelevant', no further details should be provided."
}}
Example of final output content:
{{
"<reason1,evidence1>": "Relevant. ······..."
}}
Reminder: Focus strictly on very direct and explicit connections. Classify all other relationships as 'Irrelevant' and provide explanations only for very direct 'Relevant' relationships.
"""
```

