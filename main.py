import ast
import requests
import json
from duckduckgo_search import DDGS
import google.generativeai as genai
from groq import Groq
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
import streamlit as st

genai.configure(api_key='AIzaSyCootL_jwKI3YDb6cKRJV-Ad0N4oKlLXXE')
client = Groq(api_key='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')

def jina(url):
    base_url= "https://r.jina.ai//"
    url=base_url+url
    response=requests.get(url)
    return response.text

def groq_inference(query):
  

  # client = Groq()
  completion = client.chat.completions.create(
      model="llama3-groq-70b-8192-tool-use-preview",
      messages=[
          {
              "role": "user",
              "content": query
          }
      ],
      temperature=0,
      max_tokens=2040,
      top_p=0.65,
      # stream=True,
      stop=None,
  )

  # for chunk in completion:
      # print(chunk.choices[0].delta.content or "", end="")
  # return completion.choices[0].delta.content
  return completion.choices[0].message.content

#Know about product
def serper_prod(company):
  url = "https://google.serper.dev/news"

  payload = json.dumps({
    "q": f"{company} info",
  })
  headers = {
    'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return json.loads(response.text)


#Know about the competiton\competitiors
def serper_compi(company):
  url = "https://google.serper.dev/search"

  payload = json.dumps({
    "q": f"{company} competitors.",
  })
  headers = {
    'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return json.loads(response.text)

def AI_Search_compi(text):
  ans = DDGS().chat("Summarize the text and dont remove the important terms about products or applications which should be helped for planning market for a company " + text, model='claude-3-haiku')
  return ans

def AI_Search_compi(text,titles,name):
  ans = groq_inference(f"""Summarize the text of the articles titles are {titles} and dont remove the important terms about products or applications which should be helped for knowing about the compititors for a company {name} and the data is: {text}""")
  return ans
 
def AI_Product_Analysis(text):
    ans = DDGS().chat("Analyze the products mentioned in the following news article in 400 words or fewer. Focus on their features, market relevance, and potential impact for a company's market planning: " + text, model='claude-3-haiku')
    return ans

def AI_Product_Summary(news_summaries,product):
    # combined_summaries = " ".join(news_summaries)
    ans = groq_inference(f"""Create a comprehensive summary of the product {product} based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
    # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')
    return ans

def AI_Product_Summary_prod(news_summaries):
    # combined_summaries = " ".join(news_summaries)
    ans = groq_inference(f"""Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
    # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')
    return ans
# AI_Product_Summary_prod

def AI_Search_extract_cmpy(text):
#   prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles about VR headsets. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API.Don't give more than five names in the list.

# Output Format:

# The output should be a list in the following format:
# ['company - product name', 'company - product name', 'product name', ...]
# If the company name is unknown, only include the product name without the company name.
# Do not include any introductory or explanatory text in the output; provide only the list in brackets.
# Input Format:

# The input will be a summary text containing product names, features, and key points."""
  prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles about VR headsets. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API. Don't give more than five names in the list.
  Output Format:

Provide only the list in the following format, without any explanatory or introductory text:
['company - product name', 'company - product name', 'product name', ...]
and remember dont give like this ['McDonald's - Big Mac'] becauses this will be given to pyhton this return error.
If the company name is unknown, only include the product name without the company name."""

  ans = DDGS().chat(prompt+"the text is \n" + text, model='claude-3-haiku')
  return ast.literal_eval(ans)


def AI_Company_Summary(news_summaries):
    ans = DDGS().chat("Analyze the following combined summaries about multiple products. Provide a detailed summary of each product individually, clearly outlining their features, market relevance, and competitive advantages, so this information can be used to analyze competitor products: " + news_summaries, model='claude-3-haiku')
    return ans

def AI_Analysis(Product_analysis,Compitetiors_analysis):
    prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
    system_prompt =  "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership and remember that give the analyis of the compitiors only if they are related else dont give it: " + "Competitors: \n "+ prompt,

    # ans = DDGS().chat(prompt, model='claude-3-haiku')
    # if len(prompt) > 22000:
    #     prompt = prompt[:22000]
    # ans = DDGS().chat(
    # "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership: " + "Competitors: \n "
    # + prompt,
    # model='claude-3-haiku')
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(system_prompt)

    return response.text

def AI_Analysis(Product_analysis,Compitetiors_analysis):
    prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
    system_prompt =  "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership and remember that give the analyis of the compitiors only if they are related else dont give it: " + "Competitors: \n "+ prompt,

    # ans = DDGS().chat(prompt, model='claude-3-haiku')
    # if len(prompt) > 22000:
    #     prompt = prompt[:22000]
    # ans = DDGS().chat(
    # "Analyze the following competitor and product details. Provide a thorough technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Offer actionable insights on how the product can be enhanced to increase sales and profitability. Compare the product with competitors, identifying gaps and opportunities for differentiation and market leadership: " + "Competitors: \n "
    # + prompt,
    # model='claude-3-haiku')
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(system_prompt)

    return response.text

# """ This takes input of company and return summary of the company"""
def analysis_name(text):
  compi_urls = [i['link'] for i in text['news']][0:4]
  print(compi_urls)
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
  # time.sleep(25)
  summ = AI_Product_Summary_prod(ans[:21000])
  return summ


# """" This is for knowing about the Product"""
# 11
# groq
def know_prod(name):
  ser = serper_prod(name)
  compi_urls = [i['link'] for i in ser['news']]
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
  summ = AI_Product_Summary(ans[:20000],name)
  return summ

# """ This takes input of company and return list of the compi"""
# 11
def compi_main(name):
  ret = serper_compi(name)
  compi_urls = [i['link'] for i in ret['organic']]
  title_list= [i['title'] for i in ret['organic']]
  text = [jina(url) for url in compi_urls]
  ans = ' '.join(AI_Search_compi(i[:8000],title_list,name) for i in text if len(i)>1500)
  lst = AI_Search_extract_cmpy(ans)
  return lst

# """ This takes input of company list and return summary of the company"""
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

# """ This takes inputs of compi summary and product summary and return summary of the company"""
#1
def analysis_prod(prod_summ,cmpy_summ):
  return AI_Analysis(prod_summ,cmpy_summ)


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

# def main(name, email_id):
#     start_time = time.time()
    
#     # Display the process in Streamlit
#     st.write("Analyzing product information...")
#     prod_info = know_prod(name)
#     end_prd_anal = time.time()
    
#     # Show product info and analysis time
#     st.write("Product Information:")
#     st.write(prod_info)
#     st.write(f"Time taken to analyze the product: {end_prd_anal - start_time} seconds")
    
#     st.write('*****************************************************************')
#     st.write(f"Number of websites analyzed: {len(prod_info)}")
    
#     # Competitor analysis
#     st.write("Analyzing competitors...")
#     otp = compi_main(name)
#     end_compi = time.time()
    
#     st.write(f"Number of competitors found: {len(otp)}")
#     st.write(f"Time taken to analyze the competitors: {end_compi - end_prd_anal} seconds")
    
#     st.write('*****************************************************************')
    
#     # Summary analysis
#     st.write("Generating summary...")
#     summpop = summary_name(otp)
#     end_time_summary = time.time()
    
#     # st.write('## Compititors Summary')
#     # st.write(f"len(summpop)")
#     st.write(f"Time taken to generate summary: {end_time_summary - end_compi} seconds")
    
#     st.write('*****************************************************************')
    
#     # Total analysis
#     analysis_total = analysis_prod(prod_info, summpop)
#     end_time = time.time()
    
#     st.write("## Total Analysis")
#     st.write(analysis_total)
#     # st.write(f"Analysis time taken: {end_time - end_time_summary} seconds")
#     # st.write(f"Total time taken: {end_time - start_time} seconds")
    
#     st.write('*****************************************************************')
    
#     # Send email
#     send_email_gmail(email_id, analysis_total)
    
#     return start_time, end_prd_anal, end_compi, end_time_summary, end_time, analysis_total
# def main(name, email_id):
#     start_time = time.time()

#     # Use container to group elements in a card-like style
#     with st.container():
#         st.markdown('---')  # Horizontal line before the section

#         with st.spinner("Analyzing product information..."):
#             prod_info = know_prod(name)
#         end_prd_anal = time.time()

#         # Show product info and analysis time
#         st.write("### Product Information:")
#         st.write(prod_info)
#         st.write(f"Time taken to analyze the product: {end_prd_anal - start_time:.2f} seconds")
#         st.write(f"Number of websites analyzed: {len(prod_info)}")
    
#         st.markdown('---')  # Horizontal line after the section

#     with st.container():
#         st.markdown('---')  # Horizontal line before the section

#         with st.spinner("Analyzing competitors..."):
#             otp = compi_main(name)
#         end_compi = time.time()

#         st.write("### Competitor Analysis:")
#         st.write(f"Number of competitors found: {len(otp)}")
#         st.write(f"Time taken to analyze the competitors: {end_compi - end_prd_anal:.2f} seconds")
    
#         st.markdown('---')  # Horizontal line after the section

#     with st.container():
#         st.markdown('---')  # Horizontal line before the section

#         with st.spinner("Generating summary..."):
#             summpop = summary_name(otp)
#         end_time_summary = time.time()

#         st.write("### Summary Analysis:")
#         st.write(f"Time taken to generate summary: {end_time_summary - end_compi:.2f} seconds")

#         st.markdown('---')  # Horizontal line after the section

#     with st.container():
#         st.markdown('---')  # Horizontal line before the section

#         st.write("### Total Analysis:")
#         analysis_total = analysis_prod(prod_info, summpop)
#         st.write(analysis_total)

#         end_time = time.time()

#         st.write(f"Analysis time taken: {end_time - end_time_summary:.2f} seconds")
#         st.write(f"Total time taken: {end_time - start_time:.2f} seconds")

#         st.markdown('---')  # Horizontal line after the section

#     # Email handling
#     if not email_id:
#         st.error("Email is not sent because it was not provided.", icon="🚫")
#     else:
#         # Call send_email_gmail and check if email is sent
#         if send_email_gmail(email_id, analysis_total):
#             st.success("Email sent successfully!", icon="✅")
#         else:
#             st.error("Failed to send email.", icon="❌")

#     return start_time, end_prd_anal, end_compi, end_time_summary, end_time, analysis_total


# # Streamlit UI
# st.title("Product and Competitor Analysis")

# # Inputs from user
# name = st.text_input("Enter the Product Name", "Cafe Coffee Day")
# email_id = st.text_input("Enter your Email", "kapishrachamalla32@gmail.com")

# if st.button("Start Analysis"):
#     t1, t2, t3, t4, t5, analysis = main(name, email_id)
    
#     # Time breakdown in minutes
#     st.write("Time taken to know about the product:", (t2 - t1) / 60, "minutes")
#     st.write("Time taken to know about the competitors:", (t3 - t2) / 60, "minutes")
#     st.write("Time taken to give analysis:", (t4 - t3) / 60, "minutes")
#     st.write("Time taken to generate summary:", (t5 - t4) / 60, "minutes")
#     st.write("Total time taken:", (t5 - t1) / 60, "minutes")
#$%$%$

def colored_container(color, content):
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 5px;">
        {content}
        </div>
        """, unsafe_allow_html=True
    )

def main(name, email_id):
    
    start_time = time.time()
#     colored_container("#A9DFBF", f"""
# <h4 style="color: black;">Total Analysis:</h4>
# <p style="color: black;">## Technical Analysis of McDonald's Chicken Big Mac</p>
# <p style="color: black;"><strong>Market Standing:</strong><br>The Chicken Big Mac represents a strategic move by McDonald's to tap into the growing demand for chicken-based menu items in the fast-food industry. This trend is driven by consumer interest in healthier options, a wider variety of protein sources, and the growing popularity of chicken sandwiches in general.</p>
# <p style="color: black;"><strong>Technical Strengths:</strong></p>
# <ul style="color: black;">
#     <li>Leveraging Existing Brand Equity: The Chicken Big Mac benefits from the strong brand equity of the iconic Big Mac, ensuring immediate recognition and consumer interest.</li>
#     <li>Innovation: The use of tempura-battered chicken patties represents an innovative approach to chicken preparation, adding a unique flavor profile and appealing to a broader customer base.</li>
#     <li>Meeting Consumer Preferences: The sandwich addresses the growing demand for chicken-based options, demonstrating McDonald's ability to adapt to changing consumer preferences.</li>
# </ul>
# <p style="color: black;"><strong>Areas for Improvement:</strong></p>
# <ul style="color: black;">
#     <li>Product Differentiation: While the Chicken Big Mac leverages the Big Mac's brand equity, it might benefit from more distinct features to differentiate itself further from other chicken sandwiches in the market.</li>
#     <li>Nutritional Profile: The tempura batter might raise concerns about the nutritional profile of the sandwich, potentially impacting its appeal to health-conscious consumers.</li>
#     <li>Marketing and Promotion: McDonald's needs to develop a comprehensive marketing strategy to effectively promote the Chicken Big Mac and highlight its unique selling points.</li>
# </ul>
# <p style="color: black;"><strong>Actionable Insights:</strong></p>
# <ul style="color: black;">
#     <li>Enhance Differentiation: Consider adding unique ingredients or flavor profiles to further distinguish the Chicken Big Mac from other offerings.</li>
#     <li>Promote Healthier Options: Explore lighter batter options or create a "healthier" version of the Chicken Big Mac with grilled chicken and lighter sauces.</li>
#     <li>Targeted Marketing: Focus marketing efforts on highlighting the innovation and appeal of the Chicken Big Mac, reaching target demographics interested in chicken-based options.</li>
# </ul>
# <p style="color: black;"><strong>Comparison to Competitors:</strong></p>
# <p style="color: black;">McDonald's needs to analyze the competitive landscape of chicken sandwiches. This includes identifying key competitors like Chick-fil-A, Wendy's, and Popeyes, and comparing their offerings in terms of flavor profiles, ingredients, and marketing strategies. This analysis will help McDonald's identify potential gaps and opportunities for differentiation.</p>
# <p style="color: black;"><strong>Opportunities for Market Leadership:</strong></p>
# <ul style="color: black;">
#     <li>Focus on Premium Quality: McDonald's can leverage its brand reputation to introduce a premium chicken sandwich with higher-quality ingredients and a unique flavor profile.</li>
#     <li>Create a Signature Chicken Experience: Develop a distinctive chicken sandwich experience that sets it apart from competitors, emphasizing its unique taste and texture.</li>
#     <li>Promote Chicken Innovation: Leverage the Chicken Big Mac's launch to position McDonald's as a leader in chicken innovation, showcasing a commitment to meeting evolving consumer demands.</li>
# </ul>
# <p style="color: black;"><strong>Conclusion:</strong></p>
# <p style="color: black;">The Chicken Big Mac holds significant potential for McDonald's to expand its market share in the growing chicken sandwich segment. By addressing its weaknesses, leveraging its strengths, and actively monitoring competitive offerings, McDonald's can create a successful product that drives sales and profitability.</p>
# <p style="color: black;">Analysis time taken: 4.51 seconds</p>
# <p style="color: black;">Total time taken: 368.86 seconds</p>
# """)

    # Product information section
    with st.container():
        st.markdown('---')  # Horizontal line before the section

        with st.spinner("Analyzing product information..."):
            prod_info = know_prod(name)
        end_prd_anal = time.time()

        # Display product info in a colored container
        # colored_container("#D6EAF8", f"""
        # <h4>Product Information:</h4>
        # <p>{prod_info}</p>
        # <p>Time taken to analyze the product: {end_prd_anal - start_time:.2f} seconds</p>
        # <p>Number of websites analyzed: {len(prod_info)}</p>
        # """)

        st.write("### Product Information:")
        st.write(prod_info)
        # st.write(f"Time taken to analyze the product: {end_prd_anal - start_time:.2f} seconds")
        st.write(f"Number of websites analyzed: {len(prod_info)}")
        st.markdown('---')  # Horizontal line after the section

    # Competitor analysis section
    with st.container():
        st.markdown('---')  # Horizontal line before the section

        with st.spinner("Analyzing competitors..."):
            otp = compi_main(name)
        end_compi = time.time()

        # Display competitor info in a different colored container
        # colored_container("#F9E79F", f"""
        # <h4>Competitor Analysis:</h4>
        # <p>Number of competitors found: {len(otp)}</p>
        # <p>Time taken to analyze the competitors: {end_compi - end_prd_anal:.2f} seconds</p>
        # """)

        st.write("### Competitor Analysis:")
        st.write(f"Number of competitors found: {len(otp)}")
        # st.write(f"The Competitors are: \n {otp}")
        # st.write(f"Time taken to analyze the competitors: {end_compi - end_prd_anal:.2f} seconds")

        # st.markdown('---')  # Horizontal line after the section

    # Summary analysis section
    # with st.container():
        # st.markdown('---')  # Horizontal line before the section

        with st.spinner("Generating summary..."):
            summpop = summary_name(otp)
        end_time_summary = time.time()

        # Display summary in a different color container
        # colored_container("#A9DFBF", f"""
        # <h4>Summary Analysis:</h4>
        # <p>Time taken to generate summary: {end_time_summary - end_compi:.2f} seconds</p>
        # """)

        st.write("### Summary Analysis:")
        st.write(summpop)
        # st.write(f"Time taken to generate summary: {end_time_summary - end_compi:.2f} seconds")

        st.markdown('---')  # Horizontal line after the section

    # Total analysis section
    with st.container():
        st.markdown('---')  # Horizontal line before the section

        # Display total analysis in another color container
        analysis_total = analysis_prod(prod_info, summpop)
        end_time = time.time()
        # colored_container("#F5B7B1", f"""
        # <h4>Total Analysis:</h4>
        # <p>{analysis_total}</p>
        # <p>Analysis time taken: {end_time - end_time_summary:.2f} seconds</p>
        # <p>Total time taken: {end_time - start_time:.2f} seconds</p>
        # """)

        st.write("### Total Analysis:")
        st.write(analysis_total)

        st.markdown('---')  # Horizontal line after the section

    # Email handling
    if not email_id:
        st.error("Email is not sent because it was not provided.", icon="🚫")
    else:
        # Call send_email_gmail and check if email is sent
        if send_email_gmail(email_id, analysis_total) == 'Email sent successfully!':
            st.success("Email sent successfully!", icon="✅")
        else:
            st.error("Failed to send email.", icon="❌")

    return start_time, end_prd_anal, end_compi, end_time_summary, end_time, analysis_total


# Streamlit UI
st.title("Market Mind 🧠")
# st.subheader("Empowering You with ")
st.markdown("<h7>Real-Time Market Intelligence</h1>", unsafe_allow_html=True)
 # Sidebar for developer profiles and hackathon info
st.sidebar.markdown(
        """
        <h1 style='color: #ff0000;'>🚀 Hackathon Project</h1>
        """, 
        unsafe_allow_html=True
    )
st.sidebar.markdown("Welcome to the MarketMind project, developed for the hackathon to showcase AI power in the product and competitor analysis. 🚀")

    # Add some icons/emojis to make it look more engaging
st.sidebar.markdown("### 🔧 Project Features")
    # st.sidebar.markdown("- Analyze product details using OpenFoodFacts API.")
st.sidebar.markdown("- Real-Time Market Intelligence: Offers real-time data updates for informed decision-making")
st.sidebar.markdown("- AI and Machine Learning: Helps analyze competitors and suggests improvement strategies based on data.")

    # Developer details with LinkedIn links
st.sidebar.markdown("### 👨‍💻 Developers")
st.sidebar.markdown("[Srish](https://www.linkedin.com/in/srishrachamalla/) - AI/ML Developer")
st.sidebar.markdown("[Sai Teja](https://www.linkedin.com/in/saiteja-pallerla-668734225/) - Data Analyst")

    # Add expander sections for additional content
with st.sidebar.expander("ℹ About MarketMind"):
    st.write("MarketMind is a platform focused on providing advanced data analytics, market intelligence, and AI-driven insights for businesses, investors, and market professionals. Its solutions are aimed at helping organizations make informed decisions by analyzing vast amounts of market data, consumer behavior, and industry trends in real-time")

with st.sidebar.expander("📚 Useful Resources"):
    st.write("[Google Gemini AI Documentation](https://ai.google.dev/gemini-api/docs)")
    st.write("[Streamlit Documentation](https://docs.streamlit.io/)")
    st.write("[Groq Documentation](https://console.groq.com/docs/quickstart)")

    # Add progress indicator for hackathon phases or development stages
st.sidebar.markdown("### ⏳ Hackathon Progress")
st.sidebar.progress(0.99)  # Set progress level (0 to 1)

    # Sidebar footer with final notes
st.sidebar.markdown("---")
st.sidebar.markdown(
        """
        <div style="text-align: center; font-size: 0.85em;">
            Developed by Srish & Sai Teja • Powered by Google Gemini AI
        </div>
        """, unsafe_allow_html=True
    )
# Inputs from user
name = st.text_input("Enter the Product Name", "Cafe Coffee Day")
email_id = st.text_input("Enter your Email", "")

if st.button("Start Analysis"):
    t1, t2, t3, t4, t5, analysis = main(name, email_id)
    
    # # Time breakdown in minutes
    # st.write("### Time Breakdown (in minutes)")
    # st.write(f"Time taken to analyze the product: {(t2 - t1) / 60:.2f} minutes")
    # st.write(f"Time taken to analyze competitors: {(t3 - t2) / 60:.2f} minutes")
    # st.write(f"Time taken to generate summary: {(t4 - t3) / 60:.2f} minutes")
    # st.write(f"Time taken for total analysis: {(t5 - t1) / 60:.2f} minutes")
    # Time breakdown in minutes
    st.write("### Time Breakdown (in minutes)")

    # Define colors for each breakdown
    total_color = "#FF5733"  # Red
    competitors_color = "#33C1FF"  # Blue
    summary_color = "#75FF33"  # Green
    product_color = "#FF33B5"  # Pink

    # Display each time taken in different colors
    st.markdown(f"<p style='color: {product_color};'>Time taken to analyze the product: {(t2 - t1) / 60:.2f} minutes</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {competitors_color};'>Time taken to analyze competitors: {(t3 - t2) / 60:.2f} minutes</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {summary_color};'>Time taken to generate summary: {(t4 - t3) / 60:.2f} minutes</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {total_color};'>Time taken for total analysis: {(t5 - t1) / 60:.2f} minutes</p>", unsafe_allow_html=True)
    st.markdown("---")
st.markdown("""
        <div style="text-align: center; font-size: 0.9em;">
        <p><i>MarketMind</i> was developed for a hackathon using <b>Streamlit</b> to showcase AI power in product and competitor analysis.</p>
        <p>Developed by Srish & Sai Teja </p>
        </div>
        """, unsafe_allow_html=True)
# if __name__ == "__main__":
#     t1,t2,t3,t4,t5,analysis = main('Cafe Coffee Day',"kapishrachamalla32@gmail.com")
#     print("time taken to Know about the product: ", (t2-t1)/60)
#     print("time taken to Know about the competitors: ", (t3-t2)/60)
#     print("time taken to Know about the give analysis: ", (t4-t3)/60)
#     print("time taken to Know about the summary: ", (t5-t4)/60)
#     print("total time taken: ", (t5-t1)/60)


# import ast
# import requests
# import json
# import time
# import streamlit as st
# from duckduckgo_search import DDGS
# import google.generativeai as genai
# from groq import Groq
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import markdown

# # Configure generative AI API key
# genai.configure(api_key='AIzaSyCootL_jwKI3YDb6cKRJV-Ad0N4oKlLXXE')
# client = Groq(api_key='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')

# # Function definitions as in your original code

# def jina(url):
#     base_url= "https://r.jina.ai//"
#     url=base_url+url
#     response=requests.get(url)
#     return response.text

# def groq_inference(query):
#     completion = client.chat.completions.create(
#         model="llama3-groq-70b-8192-tool-use-preview",
#         messages=[{"role": "user", "content": query}],
#         temperature=0,
#         max_tokens=2040,
#         top_p=0.65,
#         stop=None,
#     )
#     return completion.choices[0].message.content

# def serper_prod(company):
#     url = "https://google.serper.dev/news"
#     payload = json.dumps({"q": f"{company} info"})
#     headers = {
#         'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     return json.loads(response.text)

# def serper_compi(company):
#     url = "https://google.serper.dev/search"
#     payload = json.dumps({"q": f"{company} competitors."})
#     headers = {
#         'X-API-KEY': '7d6a39f71072f99cd421dbdd6cfebc73e2a66a07',
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     return json.loads(response.text)

# def AI_Search_compi(text, titles, name):
#     ans = groq_inference(f"""Summarize the text of the articles titles are {titles} and don't remove the important terms about products or applications which should help in knowing about the competitors for a company {name}. The data is: {text}""")
#     return ans

# def AI_Product_Analysis(text):
#     ans = DDGS().chat("Analyze the products mentioned in the following news article in 400 words or fewer. Focus on their features, market relevance, and potential impact for a company's market planning: " + text, model='claude-3-haiku')
#     return ans

# def AI_Product_Summary(news_summaries, product):
#     ans = groq_inference(f"""Create a comprehensive summary of the product {product} based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost, and you may add text from the articles as well: {news_summaries}""")
#     return ans

# def AI_Search_extract_cmpy(text):
#     prompt = """You will be given a dynamic text that summarizes key products, applications, and comparisons from articles. Your task is to extract relevant product names from the text and generate a list of search queries suitable for a search API. Don't give more than five names in the list. Output Format: ['company - product name', 'company - product name', 'product name', ...]."""
#     ans = DDGS().chat(prompt + "The text is \n" + text, model='claude-3-haiku')
#     print(ans)
#     return ast.literal_eval(ans)

# def AI_Company_Summary(news_summaries):
#     ans = DDGS().chat("Analyze the following combined summaries about multiple products. Provide a detailed summary of each product individually, clearly outlining their features, market relevance, and competitive advantages: " + news_summaries, model='claude-3-haiku')
#     return ans

# def AI_Product_Summary_prod(news_summaries):
#     # combined_summaries = " ".join(news_summaries)
#     ans = groq_inference(f"""Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost and remember that these are form the news articles so you may have add text also : """ + news_summaries)
#     # ans = DDGS().chat("Create a comprehensive summary of the product based on the following summaries of 10 or fewer news articles. Ensure no important product details are lost: " + news_summaries, model='gpt-4o-mini')

# def AI_Analysis(Product_analysis, Compitetiors_analysis):
#     prompt = Compitetiors_analysis + "Product Information: \n " + Product_analysis
#     system_prompt = f"""Analyze the following competitor and product details. Provide a technical analysis of each product, focusing on its market standing, technical strengths, and areas for improvement. Compare the product with competitors, identifying gaps and opportunities for differentiation: Competitors: {prompt}"""
    
#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#     response = model.generate_content(system_prompt)
#     return response.text

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

# # """ This takes input of company and return summary of the company"""
# def analysis_name(text):
#   compi_urls = [i['link'] for i in text['news']][0:4]
#   print(compi_urls)
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
#   # time.sleep(25)
#   summ = AI_Product_Summary_prod(ans[:21000])
#   return summ

# # """" This is for knowing about the Product"""
# # 11
# # groq
# def know_prod(name):
#   ser = serper_prod(name)
#   compi_urls = [i['link'] for i in ser['news']]
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Product_Analysis(i[:8000]) for i in text if len(i)>1500)
#   summ = AI_Product_Summary(ans[:20000],name)
#   return summ

# # """ This takes input of company and return list of the compi"""
# # 11
# def compi_main(name):
#   ret = serper_compi(name)
#   compi_urls = [i['link'] for i in ret['organic']]
#   title_list= [i['title'] for i in ret['organic']]
#   text = [jina(url) for url in compi_urls]
#   ans = ' '.join(AI_Search_compi(i[:8000],title_list,name) for i in text if len(i)>1500)
#   lst = AI_Search_extract_cmpy(ans)
#   return lst

# # """ This takes input of company list and return summary of the company"""
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

# # """ This takes inputs of compi summary and product summary and return summary of the company"""
# #1
# def analysis_prod(prod_summ,cmpy_summ):
#   return AI_Analysis(prod_summ,cmpy_summ)

# # Streamlit Interface

# def main():
#     st.title("Product and Competitor Analysis Tool")

#     # Input company name
#     company_name = st.text_input("Enter Company Name", value="Sample Company")
#     email = st.text_input("Enter your email (Optional)")

#     # Perform Analysis
#     if st.button("Analyze"):
#         start_time = time.time()
        
#         st.write(f"Analyzing {company_name}...")
        
#         # Analyze product
#         prod_info = know_prod(company_name)
#         st.write("### Product Information:")
#         st.write(prod_info)

#         end_prd_anal = time.time()
#         st.write(f"Time taken to analyze the product: {(end_prd_anal - start_time)/60} Mins")

#         # Analyze competitors
#         st.write("### Competitor Information:")
#         otp = compi_main(company_name)
#         print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#         print(otp)
#         st.write(otp)
#         end_compi = time.time()
#         st.write(f"Time taken to analyze the competitors: {end_compi - end_prd_anal} seconds")

#         # Summary
#         st.write("### Summary:")
#         cmpy_summ = summary_name(otp)
#         st.write(cmpy_summ)

#         end_time_summary = time.time()
#         st.write(f"Time taken to generate summary: {end_time_summary - end_compi} seconds")

#         analysis_total = analysis_prod(prod_info,cmpy_summ)
#         st.write("### Analysis:" + analysis_total)
#         # Send via email (Optional)
#         if email:
#             send_email_gmail(email, analysis_total)
#             st.write(f"Sending analysis to {email}...")
#             # (Implement email sending logic here)
#             # ...

# if __name__ == "__main__":
#     main()
