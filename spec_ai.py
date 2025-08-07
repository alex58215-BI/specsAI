import streamlit as st
import openai
# from dotenv import load_dotenv
# import os

# Load environment variables from .env file
# load_dotenv()


# Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Design Specification Generator")

# Dropdown menus
series = st.selectbox("Select Altivar Process Series", ["600", "900"])
application = st.selectbox("Select Application", ["Pumping", "HVAC"])
format = st.selectbox("Select Specification Format", ["MasterSpec", "NBS Chorus"])

if st.button("Generate Specification"):
    prompt = f"""
    Generate a comprehensive technical design specification for the Altivar {series} variable speed drive (VSD), intended for a {application} application.
    The output should be structured in a formal {format} format suitable for inclusion in engineering design documentation, with the goal of locking in this drive model for procurement and implementation.

    The specification must include:

    A brief description of the Altivar {series} series and its relevance to the application
    Key technical parameters (power range, voltage class, control modes, communication protocols, etc.)
    Application-specific features or benefits of this drive series
    Environmental ratings, certifications, and compliance standards (e.g., IEC, UL, CE)
    Installation requirements and considerations (enclosure type, cooling, space, EMC, wiring)
    Any options or modules relevant to the application (e.g., braking units, filters, HMI)
    Ensure the content is specific to the {series} series, technically accurate, and presented in a concise, professional format ready for inclusion in a design package."""
  
    st.text_area("Design Specification Prompt", prompt, height=300)

    with st.spinner("Generating..."):
        client = openai.OpenAI(api_key = OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        spec = response.choices[0].message.content
        st.success("Done!")
        st.text_area("Design Specification", spec, height=900)