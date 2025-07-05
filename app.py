import time

import markdown
import streamlit as st
from jinja2 import Template
from weasyprint import HTML


def html_to_pdf(html_string, output_file="resume.pdf"):
    HTML(string=html_string).write_pdf(output_file)


def md_to_html(md_text: str) -> str:
    return markdown.markdown(md_text)


def main():
    st.set_page_config(page_title="Markdown to Resume", layout="wide")
    st.title("📝 Markdown → Resume Generator")

    uploaded_file = st.file_uploader("Upload your Markdown Resume", type="md")
    download_flag = False

    if uploaded_file:
        md_text = uploaded_file.read().decode("utf-8")
        html_body = md_to_html(md_text)

        with open("templates/resume_template.html") as f:
            template = Template(f.read())

        rendered_resume = template.render(content=html_body)
        st.components.v1.html(rendered_resume, height=1000, scrolling=True)

        col1, col2, _ = st.columns([1, 1, 6])
        with col1:
            if st.download_button(
                "📥 Download as HTML",
                data=rendered_resume,
                file_name="resume.html",
                mime="text/html",
            ):
                download_flag = True

        with col2:
            html_to_pdf(rendered_resume)
            with open("resume.pdf", "rb") as pdf_file:
                if st.download_button(
                    "📥 Download PDF", pdf_file, file_name="resume.pdf"
                ):
                    download_flag = True

        if download_flag:
            success_msg = st.success("Downloaded Successfully.", icon="✅")
            time.sleep(1)
            success_msg.empty()


if __name__ == "__main__":
    main()
