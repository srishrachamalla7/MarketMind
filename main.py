# import ast
# import requests
# import json
# from duckduckgo_search import DDGS
# import google.generativeai as genai
# from groq import Groq
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import markdown

# genai.configure(api_key='AIzaSyCootL_jwKI3YDb6cKRJV-Ad0N4oKlLXXE')
# client = Groq(api_key='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')

# def jina(url):
#     base_url= "https://r.jina.ai//"
#     url=base_url+url
#     response=requests.get(url)
#     return response.text

# def groq_inference(query):
  

#   # client = Groq()
#   completion = client.chat.completions.create(
#       model="llama3-groq-70b-8192-tool-use-preview",
#       messages=[
#           {
#               "role": "user",
#               "content": query
#           }
#       ],
#       temperature=0,
#       max_tokens=2040,
#       top_p=0.65,
#       # stream=True,
#       stop=None,
#   )

#   # for chunk in completion:
#       # print(chunk.choices[0].delta.content or "", end="")
#   # return completion.choices[0].delta.content
#   return completion.choices[0].message.content

# #Know about product
# def serper_prod(company):
#   url = "https://google.serper.dev/news"

#   payload = json.dumps({
#     "q": f"{company} info",
#   })
#   headers = {
#     'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
#     'Content-Type': 'application/json'
#   }

#   response = requests.request("POST", url, headers=headers, data=payload)

#   return json.loads(response.text)


# #Know about the competiton\competitiors
# def serper_compi(company):
#   url = "https://google.serper.dev/search"

#   payload = json.dumps({
#     "q": f"{company} competitors.",
#   })
#   headers = {
#     'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
#     'Content-Type': 'application/json'
#   }

#   response = requests.request("POST", url, headers=headers, data=payload)

#   return json.loads(response.text)

# def AI_Search_compi(text):
#   ans = DDGS().chat("Summarize the text and dont remove the important terms about products or applications which should be helped for planning market for a company " + text, model='claude-3-haiku')
#   return ans

# def AI_Search_compi(text,titles,name):
#   ans = groq_inference(f"""Summarize the text of the articles titles are {titles} and dont remove the important terms about products or applications which should be helped for knowing about the compititors for a company {name} and the data is: {text}""")
#   return ans
 
# def AI_Product_Analysis(text):
#     ans = DDGS().chat("Analyze the products mentioned in the following news article in 400 words or fewer. Focus on their features, market relevance, and potential impact for a company's market planning: " + text, model='claude-3-haiku')
#     return ans

# def AI_Product_Summary(news_summaries,product):
#     # combined_summaries = " ".join(news_summaries)
#     ans = groq_inference(f"""Create a comprehensive summary of the product {product} based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
#     # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')
#     return ans

# def AI_Product_Summary_prod(news_summaries):
#     # combined_summaries = " ".join(news_summaries)
#     ans = groq_inference(f"""Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
#     # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')
#     return ans
# # AI_Product_Summary_prod

# def AI_Search_extract_cmpy(text):
# #   prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles about VR headsets. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API.Don't give more than five names in the list.

# # Output Format:

# # The output should be a list in the following format:
# # ['company - product name', 'company - product name', 'product name', ...]
# # If the company name is unknown, only include the product name without the company name.
# # Do not include any introductory or explanatory text in the output; provide only the list in brackets.
# # Input Format:

# # The input will be a summary text containing product names, features, and key points."""
#   prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles about VR headsets. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API. Don't give more than five names in the list.

#   Output Format:

# Provide only the list in the following format, without any explanatory or introductory text:
# ['company - product name', 'company - product name', 'product name', ...]

# If the company name is unknown, only include the product name without the company name."""

#   ans = DDGS().chat(prompt+"the text is \n" + text, model='claude-3-haiku')
#   return ast.literal_eval(ans)


# def AI_Company_Summary(news_summaries):
#     ans = DDGS().chat("Analyze the following combined summaries about multiple products. Provide a detailed summary of each product individually, clearly outlining their features, market relevance, and competitive advantages, so this information can be used to analyze competitor products: " + news_summaries, model='claude-3-haiku')
#     return ans

# def AI_Analysis(Product_analysis,Compitetiors_analysis):
#     prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
#     system_prompt =  "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership and remember that give the analyis of the compitiors only if they are related else dont give it: " + "Competitors: \n "+ prompt,

#     # ans = DDGS().chat(prompt, model='claude-3-haiku')
#     # if len(prompt) > 22000:
#     #     prompt = prompt[:22000]
#     # ans = DDGS().chat(
#     # "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership: " + "Competitors: \n "
#     # + prompt,
#     # model='claude-3-haiku')
#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#     response = model.generate_content(system_prompt)

#     return response.text

# def AI_Analysis(Product_analysis,Compitetiors_analysis):
#     prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
#     system_prompt =  "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership and remember that give the analyis of the compitiors only if they are related else dont give it: " + "Competitors: \n "+ prompt,

#     # ans = DDGS().chat(prompt, model='claude-3-haiku')
#     # if len(prompt) > 22000:
#     #     prompt = prompt[:22000]
#     # ans = DDGS().chat(
#     # "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership: " + "Competitors: \n "
#     # + prompt,
#     # model='claude-3-haiku')
#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#     response = model.generate_content(system_prompt)

#     return response.text

# # """ This takes input of company and return summary of the company"""
# def analysis_name(text):
#   compi_urls = [i['link'] for i in text['news']][0:4]
#   print(compi_urls)
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
#   # time.sleep(25)
#   summ = AI_Product_Summary_prod(ans[:21000])
#   return summ


# """" This is for knowing about the Product"""
# # 11
# # groq
# def know_prod(name):
#   ser = serper_prod(name)
#   compi_urls = [i['link'] for i in ser['news']]
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
#   summ = AI_Product_Summary(ans[:20000],name)
#   return summ

# """ This takes input of company and return list of the compi"""
# # 11
# def compi_main(name):
#   ret = serper_compi(name)
#   compi_urls = [i['link'] for i in ret['organic']]
#   title_list= [i['title'] for i in ret['organic']]
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Search_compi(i[:8000],title_list,name) for i in text if len(i)>1500)
#   lst = AI_Search_extract_cmpy(ans)
#   return lst

# """ This takes input of company list and return summary of the company"""
# #21
# def summary_name(otp):
#   names=[]
#   title=otp
#   for idx, i in enumerate(otp):
#       results = serper_prod(i)  # Call your function with the company name
#       globals()[f'compi_{chr(65 + idx)}'] = results
#       # print(i)
#       # print(f'compi_{chr(65 + idx)}')
#       names.append(f'compi_{chr(65 + idx)}')
#   text_data = [globals()[name] for name in names]
#   summ_data = [analysis_name(i) for i in text_data]
#   cmpy_summ = AI_Company_Summary(" ".join(summ_data))
#   return cmpy_summ

# """ This takes inputs of compi summary and product summary and return summary of the company"""
# #1
# def analysis_prod(prod_summ,cmpy_summ):
#   return AI_Analysis(prod_summ,cmpy_summ)


# def main(name,email_id):
#   start_time = time.time()
#   prod_info = know_prod(name)
#   end_prd_anal = time.time()
#   print(prod_info)
#   print(f"Time taken to analyze the product: {end_prd_anal - start_time} seconds")
#   print('*****************************************************************')
#   # print(prod_info)
#   print(len(prod_info))
#   otp = compi_main(name)
#   end_compi = time.time()
#   print(len(otp))
#   print(f"Time taken to analyze the competitors: {end_compi - end_prd_anal} seconds")
#   print('*****************************************************************')
#   # print(otp)
#   summpop = summary_name(otp)
#   print(len(summpop))
#   end_time_summary = time.time()
#   print(f"Time taken to analyze the summary: {end_time_summary - end_compi} seconds")
#   print('*****************************************************************')
#   # print(summpop)
#   print('*****************************************************************')
#   analysis_total = analysis_prod(prod_info,summpop)
#   end_time = time.time()
#   print(f"Analysis time taken: {end_time - end_time_summary} seconds")
#   print('*****************************************************************')
#   print(f"Total time taken: {end_time - start_time} seconds")
#   print('*****************************************************************')
#   # print(analysis(prod_info,summpop))
#   #Send emails
#   send_email_gmail(email_id,analysis_total)


#   return start_time, end_prd_anal, end_compi, end_time_summary , end_time, analysis_total


# def send_email_gmail(receiver_email,markdown_content):
#     sender_email = "srishnotebooks@gmail.com"
#     sender_password = "zoge jatp yaib qtsz"# replace with the app password generated
#     # receiver_email = "recipient_email@example.com"
#     subject = "Product Analysis Report"

#     # Create the email message container
#     msg = MIMEMultipart('alternative')
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Convert markdown to HTML
#     html_content = markdown.markdown(markdown_content)

#     # Attach the HTML content
#     msg.attach(MIMEText(html_content, 'html'))

#     try:
#         # Set up the server using Gmail's SMTP
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()  # Encrypt the connection
#         server.login(sender_email, sender_password)  # Use App Password instead of Gmail password
        
#         # Send the email
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()

#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {str(e)}")


# if __name__ == "__main__":
#     t1,t2,t3,t4,t5,analysis = main('Cafe Coffee Day',"kapishrachamalla32@gmail.com")
#     print("time taken to Know about the product: ", (t2-t1)/60)
#     print("time taken to Know about the competitors: ", (t3-t2)/60)
#     print("time taken to Know about the give analysis: ", (t4-t3)/60)
#     print("time taken to Know about the summary: ", (t5-t4)/60)
#     print("total time taken: ", (t5-t1)/60)
import ast
import requests
import json
import time
import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown

# Configure generative AI API key
genai.configure(api_key='AIzaSyCootL_jwKI3YDb6cKRJV-Ad0N4oKlLXXE')
client = Groq(api_key='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')

# Function definitions as in your original code

def jina(url):
    base_url= "https://r.jina.ai//"
    url=base_url+url
    response=requests.get(url)
    return response.text

def groq_inference(query):
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[{"role": "user", "content": query}],
        temperature=0,
        max_tokens=2040,
        top_p=0.65,
        stop=None,
    )
    return completion.choices[0].message.content

def serper_prod(company):
    url = "https://google.serper.dev/news"
    payload = json.dumps({"q": f"{company} info"})
    headers = {
        'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

def serper_compi(company):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"{company} competitors."})
    headers = {
        'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

def AI_Search_compi(text, titles, name):
    ans = groq_inference(f"""Summarize the text of the articles titles are {titles} and don't remove the important terms about products or applications which should help in knowing about the competitors for a company {name}. The data is: {text}""")
    return ans

def AI_Product_Analysis(text):
    ans = DDGS().chat("Analyze the products mentioned in the following news article in 400 words or fewer. Focus on their features, market relevance, and potential impact for a company's market planning: " + text, model='claude-3-haiku')
    return ans

def AI_Product_Summary(news_summaries, product):
    ans = groq_inference(f"""Create a comprehensive summary of the product {product} based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost, and you may add text from the articles as well: {news_summaries}""")
    return ans

def AI_Search_extract_cmpy(text):
    prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API. Don't give more than five names in the list. Output Format: ['company - product name', 'company - product name', 'product name', ...]."""
    ans = DDGS().chat(prompt + "The text is \n" + text, model='claude-3-haiku')
    return ast.literal_eval(ans)

def AI_Company_Summary(news_summaries):
    ans = DDGS().chat("Analyze the following combined summaries about multiple products. Provide a detailed summary of each product individually, clearly outlining their features, market relevance, and competitive advantages: " + news_summaries, model='claude-3-haiku')
    return ans

def AI_Product_Summary_prod(news_summaries):
    # combined_summaries = " ".join(news_summaries)
    ans = groq_inference(f"""Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
    # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')

def AI_Analysis(Product_analysis, Compitetiors_analysis):
    prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
    system_prompt = f"""Analyze the following competitor and product details. Provide a technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Compare the product with competitors, identifying gaps and opportunities for differentiation: Competitors: {prompt}"""
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(system_prompt)
    return response.text

def send_email_gmail(receiver_email,markdown_content):
    sender_email = "srishnotebooks@gmail.com"
    sender_password = "zoge jatp yaib qtsz"# replace with the app password generated
    # receiver_email = "recipient_email@example.com"
    subject = "Product Analysis Report"

    # Create the email message container
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Set up the server using Gmail's SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encrypt the connection
        server.login(sender_email, sender_password)  # Use App Password instead of Gmail password
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

""" This takes input of company and return summary of the company"""
def analysis_name(text):
  compi_urls = [i['link'] for i in text['news']][0:4]
  print(compi_urls)
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
  # time.sleep(25)
  summ = AI_Product_Summary_prod(ans[:21000])
  return summ

"""" This is for knowing about the Product"""
# 11
# groq
def know_prod(name):
  ser = serper_prod(name)
  compi_urls = [i['link'] for i in ser['news']]
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
  summ = AI_Product_Summary(ans[:20000],name)
  return summ

""" This takes input of company and return list of the compi"""
# 11
def compi_main(name):
  ret = serper_compi(name)
  compi_urls = [i['link'] for i in ret['organic']]
  title_list= [i['title'] for i in ret['organic']]
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Search_compi(i[:8000],title_list,name) for i in text if len(i)>1500)
  lst = AI_Search_extract_cmpy(ans)
  return lst

""" This takes input of company list and return summary of the company"""
#21
def summary_name(otp):
  names=[]
  title=otp
  for idx, i in enumerate(otp):
      results = serper_prod(i)  # Call your function with the company name
      globals()[f'compi_{chr(65 + idx)}'] = results
      # print(i)
      # print(f'compi_{chr(65 + idx)}')
      names.append(f'compi_{chr(65 + idx)}')
  text_data = [globals()[name] for name in names]
  summ_data = [analysis_name(i) for i in text_data]
  cmpy_summ = AI_Company_Summary(" ".join(summ_data))
  return cmpy_summ

""" This takes inputs of compi summary and product summary and return summary of the company"""
#1
def analysis_prod(prod_summ,cmpy_summ):
  return AI_Analysis(prod_summ,cmpy_summ)

# Streamlit Interface

def main():
    st.title("Product and Competitor Analysis Tool")

    # Input company name
    company_name = st.text_input("Enter Company Name", value="Sample Company")
    email = st.text_input("Enter your email (Optional)")

    # Perform Analysis
    if st.button("Analyze"):
        start_time = time.time()
        
        st.write(f"Analyzing {company_name}...")
        
        # Analyze product
        prod_info = know_prod(company_name)
        st.write("### Product Information:")
        st.write(prod_info)

        end_prd_anal = time.time()
        st.write(f"Time taken to analyze the product: {end_prd_anal - start_time} seconds")

        # Analyze competitors
        st.write("### Competitor Information:")
        otp = compi_main(company_name)
        st.write(otp)
        end_compi = time.time()
        st.write(f"Time taken to analyze the competitors: {end_compi - end_prd_anal} seconds")

        # Summary
        st.write("### Summary:")
        cmpy_summ = summary_name(otp)
        st.write(cmpy_summ)

        end_time_summary = time.time()
        st.write(f"Time taken to generate summary: {end_time_summary - end_compi} seconds")

        analysis_total = analysis_prod(prod_info,cmpy_summ)
        st.write("### Analysis:" + analysis_total)
        # Send via email (Optional)
        if email:
            send_email_gmail(email, analysis_total)
            st.write(f"Sending analysis to {email}...")
            # (Implement email sending logic here)
            # ...

if __name__ == "__main__":
    main()
