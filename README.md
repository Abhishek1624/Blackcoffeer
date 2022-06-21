# BlackCoffeer

BlackCoffeer is a data scrapping project written in python to scrape a list of URLs given in an Excel file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages from requirements.txt.

```bash
pip install -r requirements.txt
```

## Flow of the project
```python
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}
response = requests.get(url,headers=headers)
# Returns the HTML of the URL
```
Here I am using [requests](https://pypi.org/project/requests/) to get the URL content.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.content, 'html5lib')
# Return the HTML in a structured manner
```
Here I am using the response from the request and making it beautiful and using a parsing library [html5lib](https://pypi.org/project/html5lib/) in [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). It makes it easy to get data from the raw HTML.

```python
import openpyxl

srcfile = openpyxl.load_workbook('Output Data Structure.xlsx', read_only=False, keep_vba=True)
sheetname = srcfile['Sheet1']
sheetname.cell(row=index, column=3).value = data['positiveScore']
sheetname.cell(row=index, column=4).value = data['negativeScore']
# Write back to the output Excel file 
srcfile.save('Output Data Structure.xlsx')
#save the file
```
At last, I am using the [openpyxl](https://pypi.org/project/openpyxl/) library to write data into the existing Excel file
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
