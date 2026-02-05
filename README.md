# 🕸️ Instant Knowledge Graph Generator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Llama--3-purple)
![Groq](https://img.shields.io/badge/Inference-Groq_LPU-orange)

> **"Text is linear. Knowledge is a network."**

## 💡 The Story
As a Junior Data Scientist, I often felt overwhelmed by linear learning materials. Syllabuses and articles are just lists of bullet points, making it hard to see the "Big Picture".
I wanted a way to turn raw text into a visual map. So, I engineered this tool.

It takes any technical text (syllabus, article, notes) and instantly generates an interactive **Knowledge Graph** using **Llama-3** on **Groq**.

## 📸 Demo
*(Here is the app visualizing the Generative AI Ecosystem)*
![Graph Demo](demo_graph.png)

## 🚀 Key Features
* **Instant Visualization:** Uses **Groq's LPU** engine for sub-second inference.
* **Smart Extraction:** Leverages **Llama-3-70b** to understand context (JSON Mode).
* **Interactive Physics:** Built with `PyVis` for dynamic graph exploration.

## 🛠️ Tech Stack
* **LLM Engine:** Llama-3 (via Groq API)
* **Frontend:** Streamlit
* **Graph Logic:** NetworkX
* **Visualization:** PyVis

## 📦 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone [https://github.com/edenmrv/knowledge-graph-generator.git](https://github.com/edenmrv/knowledge-graph-generator.git)
   cd knowledge-graph-generator
