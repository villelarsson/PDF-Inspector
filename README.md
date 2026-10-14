# PDF Inspector

A small Streamlit app that shows what is actually inside a PDF's text layer. Upload a PDF and it lists the document metadata (title, author, subject, keywords), then goes through each page and shows every text span with its font name, font size, style (bold/italic), colour as RGB, and position (top-left of the span, in points and millimetres). Extraction is done with PyMuPDF (`page.get_text("dict")`), so the values are what the PDF contains, not an estimate from a rendered image.

I built this at Morningstar while working on client reports. We generated PDF reports, and checking them by eye wasn't catching formatting drift: a heading that was 11pt instead of 12pt, a colour that was slightly off from the brand value, text that looked right but used the wrong font. Those are easy to miss on screen and easy to confirm once you can see the exact values, so this tool pulls them out for you to check against the spec. My old team still uses it.

To run it:

```
pip install -r requirements.txt
streamlit run pdf_font_inspector.py
```

Then open the local URL Streamlit prints and upload a PDF.

If I rebuilt it, I would make the output something you can compare rather than only read: export spans to CSV or JSON, and add a way to diff a report against a reference PDF or a style spec, which is what we were really doing by hand. I would also add a command-line mode so the check could run in a pipeline, open the upload from memory instead of writing it to the working directory, read bold/italic from PyMuPDF's span flags rather than guessing from the font name, and escape the extracted text before putting it into HTML.
