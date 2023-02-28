import pycurl
from io import BytesIO
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import xmltodict
import pprint
import sys

# c.setopt(pycurl.VERBOSE, 1)
headers = {}
counter_request = 0
FILENAME = "Delete_Subscription_open5gs.txt"
def print_response(header, b_obj):
    original_stdout = sys.stdout
    with open(FILENAME, "a") as f:
        sys.stdout = f
        pprint.pprint(header)
        print('-' * 20)

        # Get the content stored in the BytesIO object (in byte characters)
        get_body = b_obj.getvalue()

        # Decode the bytes stored in get_body to HTML and print the result
        print(get_body.decode('iso-8859-1'))
        print('='* 120)
        sys.stdout = original_stdout

def print_request(method, url, header, body):
    all_request = ""
    global counter_request
    counter_request += 1
    all_request += "Request Number " + str(counter_request) +"\n"+method + " " + url+"\n"+'\n'.join(header)+""

    print("Request Number " + str(counter_request))
    print("")
    print(method + " " + url)
    print('\n'.join(header))
    print("")

    if body != "no_body":
        print(body)
        all_request +="\n"+body

    all_request += "\n"+"-"*60+"\n"
    print("-" * 60)

    file1 = open(FILENAME, "a")  # append mode
    file1.write(all_request)
    file1.close()


def display_header(header_line):

    header_line = header_line.decode('iso-8859-1')

    # Ignore all lines without a colon
    if ':' not in header_line:
        return

    # Break the header line into header name and value
    h_name, h_value = header_line.split(':', 1)

    # Remove whitespace that may be present
    h_name = h_name.strip()
    h_value = h_value.strip()
    h_name = h_name.lower() # Convert header names to lowercase
    headers[h_name] = h_value # Header name and value.

## Method Calls

def GET_method_http2(url, header):
    b_obj = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)                                                                # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)           # Set HTTP2 protocol
    c.setopt(pycurl.HTTPHEADER, header)
    c.setopt(c.HEADERFUNCTION, display_header)                                          # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)                                                        # where curl will put the body

    c.perform()
    c.close()

    print_response(headers, b_obj)
    b_obj.close()
    headers.clear()

def POST_method_http2(url, custom_header ,data_post):
    pf = data_post.encode('utf-8')
    #pf = urlencode(data_post)
    b_obj = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, url)                                                        # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)   # Set HTTP2 protocol
    c.setopt(c.HEADERFUNCTION, display_header)                                  # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)                                                # where curl will put the body
    c.setopt(pycurl.HTTPHEADER, custom_header)
    c.setopt(c.POSTFIELDS, pf)                                                  # Set Payload for POST, PUT, PATCH...
    c.perform()
    c.close()

    print('Header values:-')
    print(headers)
    print('-' * 20)

    # Get the content stored in the BytesIO object (in byte characters)
    get_body = b_obj.getvalue()

    # Decode the bytes stored in get_body to HTML and print the result
    print('Output of GET request:\n%s' % get_body.decode('utf8'))

    b_obj.close()

def PUT_method_http2(data_post):
    b_obj = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)  # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)  # Set HTTP2 protocol
    c.setopt(c.HEADERFUNCTION, display_header)  # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)  # where curl will put the body
    # c.setopt(pycurl.VERBOSE, 1)
    c.perform()
    c.close()
    c.setopt(c.CUSTOMREQUEST, 'PUT')

def PATCH_method_http2():
    b_obj = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)  # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)  # Set HTTP2 protocol
    c.setopt(c.HEADERFUNCTION, display_header)  # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)  # where curl will put the body
    # c.setopt(pycurl.VERBOSE, 1)
    c.perform()
    c.close()
    c.setopt(c.CUSTOMREQUEST, 'PATCH')

def OPTIONS_method_http2():
    b_obj = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)                                                                # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)           # Set HTTP2 protocol
    c.setopt(c.HEADERFUNCTION, display_header)                                          # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)                                                        # where curl will put the body
    # c.setopt(pycurl.VERBOSE, 1)
    c.perform()
    c.close()
    c.setopt(c.CUSTOMREQUEST, 'OPTIONS')


def DELETE_method_http2(url_c, custom_header):
    b_obj = BytesIO()
    global headers

    # set request data
    c = pycurl.Curl()
    c.setopt(c.URL, url_c)
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)       # Set HTTP2 protocol
    c.setopt(pycurl.HTTPHEADER, custom_header)
    c.setopt(c.CUSTOMREQUEST, 'DELETE')

    # set response data
    c.setopt(c.HEADERFUNCTION, display_header)                             # where curl will put the header
    c.setopt(c.WRITEDATA, b_obj)                                           # where curl will put the body

    c.perform()
    c.close()

    # see response
    print_response(headers, b_obj)
    b_obj.close()
    headers.clear()

### MAIN ##


# Reading the data inside the xml file to a variable under the name "data"
with open('1. DELETE Subscription ID (Document)/oai_test', 'r') as f:
    doc = xmltodict.parse(f.read())

ctr = 0
for item in doc['items']['item']:
    ctr += 1

    # body
    data = "no_body"

    # url
    url = item['url']
    url = url.replace("192.168.70.130", "127.0.0.10:7777")              # Substitute with IP of Open5GS

    #method
    method = item['method']

    #header
    header = item['request']['#text']
    header = header.split("\n")
    del header[0]                                                        # delete first element: METHOD and path API
    header = [x for x in header if "Content-Length: " not in x]          # delete Content-Lenght
    for item2 in header:                                                  # substitute with IP of Open5GS
        idx = header.index(item2)
        header[idx] = header[idx].lstrip()
        if "Host: 192.168.70.130" in item2:
            header[idx] = header[idx].replace("Host: 192.168.70.130","Host: 127.0.0.10")

    print_request(method, url, header, data)

    if method == "POST":
        data_post = data                                                  # {'field': 'value'}
        POST_method_http2(url, header, data_post)

    elif method == "GET":
        GET_method_http2(url, header)

    elif method == "DELETE":
        DELETE_method_http2(url, header)

    else:
        print("method not found")

exit(0)




