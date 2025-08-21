import streamlit as st
import fitz
import os

st.set_page_config(page_title="PDF Font Inspector", layout="wide")
st.title("PDF Inspector")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

def font_styles(font_name):
    styles = []
    font_lower = font_name.lower()
    if "bold" in font_lower:
        styles.append("bold")
    if "italic" in font_lower or "oblique" in font_lower:
        styles.append("italic")
    return styles or ["normal"]

def int_to_rgb(color_int):
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return f"rgb({r}, {g}, {b})"

def pt_to_mm(pt):
    return round(pt * 0.3528, 2)

if uploaded_file:
    # Save uploaded file temporarily to get file name
    temp_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Open PDF
    doc = fitz.open(temp_path)

    # Display metadata at the very top
    metadata = doc.metadata
    st.markdown("## PDF Metadata")
    st.write(f"**File:** {uploaded_file.name}")
    st.write(f"**Title:** {metadata.get('title', 'N/A')}")
    st.write(f"**Author:** {metadata.get('author', 'N/A')}")
    st.write(f"**Subject:** {metadata.get('subject', 'N/A')}")
    st.write(f"**Keywords:** {metadata.get('keywords', 'N/A')}")

    st.markdown("---")  # Separator line

    # Loop through pages and extract font details
    for page_num in range(len(doc)):
        page = doc[page_num]
        st.markdown(f"## Page {page_num + 1}")
        
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = span["size"]
                    font = span["font"]
                    text = span["text"].strip()
                    color = int_to_rgb(span["color"])
                    bbox = span["bbox"]
                    x, y = round(bbox[0], 2), round(bbox[1], 2)
                    x_mm, y_mm = pt_to_mm(x), pt_to_mm(y)
                    styles = font_styles(font)

                    if not text:
                        continue

                    st.markdown(
                        f'<div style="color:white; background-color:#111; padding:6px; border-radius:6px; margin-bottom:4px;">'
                        f'{text}<br>'
                        f'<span style="font-size:small;">'
                        f'Size: <code>{size}</code> | Font: <code>{font}</code> | Style: <code>{", ".join(styles)}</code> | '
                        f'Color: <code>{color}</code> | '
                        f'Position: <code>x={x} pt / {x_mm} mm</code>, <code>y={y} pt / {y_mm} mm</code>'
                        f'</span></div>',
                        unsafe_allow_html=True
                    )

    doc.close()

    os.remove(temp_path)
