from weasyprint import HTML


def generate_pdf(content: bytes, output_path: str):
    with open(output_path, "wb") as f:
        HTML(string=content.decode("utf-8")).write_pdf(f)
