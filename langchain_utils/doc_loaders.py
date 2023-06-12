from typing import List

from langchain.document_loaders import PDFMinerLoader
from langchain.schema import Document


def pdf_to_page_docs(pdf_path: str,
                     insert_str: str = '') -> List[Document]:
    """
    Given a PDF, return it as a series of pages.

    Args:
        pdf_path: Path to the PDF document.
        append_str: Add this string to the beginning of every document.
                    Helpful for maintaining parent document information.

    Returns:
        List of the pages in the pdf, as Documents
    """
    # Load the given document
    doc = PDFMinerLoader(pdf_path).load()[0]

    # Split into pages based on the unicode linefeed char.
    pages = doc.page_content.split('\x0c')

    # Iterate over the pages
    ret_docs = []

    for page_index, page_text in enumerate(pages):
        if insert_str:
            page_text = insert_str + page_text
        page_doc = Document(page_content=page_text,
                            metadata={'source':pdf_path,
                                      'page_num':page_index+1})
        ret_docs.append(page_doc)
    return ret_docs
