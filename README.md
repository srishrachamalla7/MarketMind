# 🧠 **MarketMind**

**MarketMind** is a Python-based tool designed to analyze a company's product and its market position relative to its competitors. It gathers information about the product and the competition, summarizes the findings, and generates insights to help assess whether the product is well-positioned in the market. The tool also offers a detailed analysis of the competitors and provides actionable recommendations.

## 🚀 **Features**

- **📊 Competitor Analysis:** Fetches competitor data for the given product/company and provides a summary of their products.
- **📈 Product Evaluation:** Analyzes the market standing of the company's product and highlights areas of strength and improvement.
- **📝 Comprehensive Report:** Generates a detailed report, summarizing key insights about the company's product, its competitors, and market positioning.
- **📧 Gmail Integration:** Sends the final analysis report via email in an HTML format, converting Markdown content into a well-structured email.

---

## ⚙️ **Prerequisites**

Before running the project, ensure you have:

- A Gmail account with an **App Password** enabled for secure access.
- Python 3.11 installed on your machine.
- Access to external APIs for fetching competitor and product data.

---

## 🛠️ **Installation**

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/srishrachamalla7/MarketMind.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The key dependencies include:
   - `requests`
   - `google.generativeai`
   - `markdown`
   - `Groq`


3. Set up your environment variables for the Gmail App Password and API keys required for data extraction.

---

## 📂 **Usage**

1. Modify the script with the company's product you want to analyze. Update the Gmail credentials and API keys as required.
   
2. Run the script by providing the company name and product:

   ```bash
   python app.py
   ```

3. The script will:
   - Fetch product details from relevant sources.
   - Analyze the product’s market position.
   - Gather competitor information.
   - Create a comprehensive summary and send an email with the analysis.

---

### 💡 **Example**

If you want to analyze the **Nothing Phone 2** product, you would update the input in the script and run it like so:

```python
if __name__ == '__main__':
    t1, t2, t3, t4, t5, analysis = main('Nothing Phone 2')
    print("Total time taken: ", (t5-t1)/60, "minutes")
```

---

### 📧 **Email Report**

The final analysis will be sent via email in an HTML format, converted from Markdown. The report will cover:

- **Product Analysis:** Detailed insights into the product's strengths and weaknesses.
- **Competitor Analysis:** A breakdown of competitors in the market and how they compare.
- **Overall Summary:** A high-level overview of the company's position in the market.

---

## ⚙️ **How It Works**

1. **Data Gathering:** Uses APIs like Groq models and Serper to extract information about the product and competitors.
   
2. **Product and Competitor Analysis:** The tool uses AI models to summarize articles and provide insights into market performance and competitive positioning.

3. **Email Integration:** After generating the report, it is converted into HTML and sent via Gmail using Python's `smtplib`.

---

## 👨‍💻 **Developers**

This project was developed by:

- **[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)**  
  Role: AI/ML Engineer  
  Responsible for integrating AI models and performing analysis.  

- **[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)**  
  Role: Data Analyst  
  Responsible for data extraction, competitor analysis, and report generation.

---

## 📦 **Requirements**

- Python 3.11
- External APIs for product and competitor information.
- Gmail credentials with App Password enabled.

