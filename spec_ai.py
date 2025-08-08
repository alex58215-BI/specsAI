import streamlit as st
import openai
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY environment variable not set.")
    st.stop()


# Load and embed documents (run once or cache)
@st.cache_resource
def load_vectorstore(folder_path):
    loader = DirectoryLoader(folder_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

st.title("Design Specification Generator with RAG")

# Dropdown menus
series = st.selectbox("Select Altivar Process Series", ["630", "930"])
application = st.selectbox("Select Application", ["Pumping", "HVAC"])
format = st.selectbox("Select Specification Format", ["MasterSpec", "NBS Chorus"])
folder_path = st.text_input("Folder with reference documents", "/workspaces/specsAI/docs")

if st.button("Generate Specification"):
    vectorstore = load_vectorstore(folder_path)
    query = f"Altivar {series} for {application} in {format} format"
    docs = vectorstore.similarity_search(query, k=4)
    context = "\n\n".join([d.page_content for d in docs])
    
    st.text_area("Design Specification Context", context, height=300)


    prompt = f"""
    Use the following context to generate a comprehensive technical design specification for the Altivar {series} VSD ({application} application) in {format} format.

    Context:
    {context}

    Specification requirements:
    - Brief description of the Altivar {series} series and its relevance
    - Key technical parameters
    - Application-specific features
    - Environmental ratings, certifications, and compliance
    - Installation requirements
    - Relevant options or modules
    - Ensure technical accuracy and concise, professional format.
    """

    st.text_area("Design Specification Prompt", prompt, height=300)

    with st.spinner("Generating..."):
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        spec = response.choices[0].message.content
        st.success("Done!")
        st.text_area("Design Specification", spec, height=900)