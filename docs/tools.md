
- [Gmail](#gmail)
- [Arxiv](#arxiv)
- [Search Engine](#search-engine)
- [PDFReader](#pdfreader)
- [ScrapTool](#scraptool)

## Gmail

Before using the Gmail tool, you need to set up SMTP access. Please follow the instructions in this [blog post](https://www.gmass.co/blog/gmail-smtp/) or this [Chinese blog](https://www.cnblogs.com/jiyuwu/p/16313476.html) to obtain a device password.

**Use Case**
```python
from miniagent.tools import EmailTool

tool = EmailTool(user_email='your_email', password='your_device_password', recipient=["your_recipient"])

tool.invoke(subject="Hello World!", contents="Hello World!", email="Other recipients desired to send")
```

## Arxiv
This tool allows you to search for relevant papers on Arxiv.

**Use Case**
```python
from miniagent.tools import ArxivTool

arxivtool = ArxivTool(sort_criterion="submittedDate")
output = arxivtool.invoke("language agent")
```

## Search Engine

NOTE: We use the [Search-Engines-Scraper](Search-Engines-Scraper) to get the searched results.
However, the searched results are very limited and not the intact information. A searched sample is:

```python
{'host': 'healthline.com',                                                                                                                                             
 'link': 'https://www.healthline.com/health/staying-healthy',
 'text': 'Learn how to improve your physical and mental well-being with '
         'science-backed advice on exercise, nutrition, smoking, sleep, '
         'hydration, and more. Find out how to lower your risk of chronic '
         'diseases, improve your mood, and live a long, productive life.',
 'title': 'Staying Healthy: Top 10 Tips for Good Health'}
```
The `text` is a short description for the url. So, it is better to scraped detailed information from the `link` or url according to the interested content of the LLM.


## PDFReader

This tool is designed to parse PDF files into text format.

**Use Case**
```python
from miniagent.tools import PDFReaderTool

pdftool = PDFReaderTool()
filepath = "examples/example.pdf"
parsed_text = pdftool.invoke(filepath)
```

## ScrapTool
The ScrapTool is intended for extracting and returning textual content from a specified URL.

**Use Case**
```python
from miniagent.tools import ScrapTool

scraptool = ScrapTool()
output = scraptool.invoke(url="https://www.langchain.com")
print(output)
```
This tool will return the main content of a given HTML page. It can be extended to create a ScrapAgent that scrapes raw text from a URL and summarizes it.
