# Super LLM: Unleashing the Power of Language Models ![super.AI logo](https://assets-global.website-files.com/615aeb2789c3f08cb6e2186e/615aeb2789c3f00527e218ed_super-ai-logo.svg)


📺 Watch our [welcome video](https://www.loom.com/share/e372299f12c340ce8866ef2f070721ba) to see Super LLM in action.
https://www.loom.com/share/e372299f12c340ce8866ef2f070721ba

🚀 **[Quick Start]()**  |  💼 **[Examples]()** | 📚 **[Documentation]()** | 💬 **[Community]()** | 🌐 **[Website]()**  

## 1 Quick Start 🚀
Install: 
```bash
git clone https://github.com/mysuperai/superai-sdk.git
cd superai-sdk
pip install -r requirements_dev.txt
python setup.py install
pip install -e .
```
Run the hello world example
```python
from superai.llm import AI
llm = AI(input_schema=Text(), output_schema=Text(), prompt="Say ")
result = llm.process("What is the capital of France?")
print(result)
```

## 2 Principles 
1. **Context aware**  - Use your own data and other external data 
2. **Recursive**  - Work fast in a constantly improving multi-step feedback loop 
3. **Actions**  - Employ external tools and actions to complement LLMs 
4. **Build off existing work**  - Leverage other people's latest ideas and contributions

## 3 Anti-Principles

## 4 Key Concepts 
1. [Prompts]() : Management, Optimization, Generation, Evaluation 
2. [Models]() : Use OpenAI, Cohere, AWS, Midjourney, etc. 
3. [Learning]() : In-context learning, fine-tuning, foundation model training
4. [Data Management]() : Multimodal database of all your data 
5. [Context]() : Add your own Google Drive, Notion, images, presentations, webpages, Twitter 
6. [Actions]() : Access to actions and external tools like search, Python compiler, Wolfram Alpha 
7. [Agents]() : Integrate with ReAct, AutoGPT, BabyAGI, or create your own agent 
8. [Workflows]() : Go beyond a single call, AI compiler, tasks, router, combiner, QA, training 
9. [Memory]() : Persist state between calls of an agent 
10. [Hub]() : Find and contribute models, data, prompts, agents, actions from the community 
11. [Integrations]() : Integrate with Hugging Face, Zapier, email, Google Sheets, Twitter, Figma 
12. [Chat]() : Chat with your models or data to improve them and learn about them

## 5 Examples

Super LLM can be used for a wide range of applications: 
- [Document extraction]() - Extract tables, key-value pairs, signatures, stamps, handwriting
- [Document Q&A and chat]() - Chat with and ask questions to documents
- [Document summarization]() - summarize Arxiv papers, podcasts, etc.

For a full list of examples, visit our [examples page](https://chat.openai.com/c/examples_url) .
## 6 Contributors

Super LLM wouldn't be possible without our amazing contributors
- marius@super.ai
- alexander@super.ai 
- brad@super.ai 

## 7 Next Steps

Ready to dive in? Here's what to do next: 
- **[Join the community]()** : Connect with other users and contributors 
- **[Contribute]()** : Make money by sharing your work on the hub 
- **[View documentation]()** : Learn more about Super LLM and its features

Get ready to unleash the true power of language models with Super LLM!
