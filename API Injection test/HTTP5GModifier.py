"""\
Tool name: 5GHTTPModifier

Version: 0.1

Author: Filippo Dolente (f.dolente@studenti.unipi.it)

License: GNU General Public License v3.0 (gpl-3.0)

Tool description:
    This tool transforms requests made to attempt API Injection attacks
    to Open Air Interface (HTTP/1.1), into HTTP/2 requests accepted
    for the server (127.0.0.10:7777) of Open5GS, for the NRF NF.
"""

import pycurl
from io import BytesIO
import xmltodict
import pprint
import sys
import os


# Global Variables
headers = {}
counter_request = 0                                             # Number of request modified
status_code_response = "no_status_code"                         # store the actual status code response for request
# c.setopt(pycurl.VERBOSE, 1) -> To enable response in cmd


def retrive_payload(header):
    payload = ""
    payload_start = -2
    payload_end = len(header)

    # To find start payload (offset)
    for idx, item in enumerate(header):
        if header[idx] == "" and header[idx+1] != "":
            payload_start = idx+1
            break
    payload = '\n'.join(header[payload_start:payload_end])

    return payload, payload_start


def print_response(header, b_obj, output_file):

    original_stdout = sys.stdout

    with open(output_file, "a") as f:
        sys.stdout = f                                              # all "print" will print in file
        pprint.pprint(header)
        print('-' * 20)
        if status_code_response != "no_status_code":
            print("Status Code: "+str(status_code_response))

        # Get the content stored in the BytesIO object (in byte characters)
        get_body = b_obj.getvalue()

        # Decode the bytes stored in get_body to HTML and print the result
        print(get_body.decode('iso-8859-1'))
        print('=' * 120)
        sys.stdout = original_stdout


def print_request(method, url, header, body, output_file):
    all_request = ""
    global counter_request
    counter_request += 1

    all_request += "\nRequest Number " + str(counter_request) +"\n\n"+method + " " + url+"\n"+'\n'.join(header)+"\n"

    print("Request Number " + str(counter_request)+"\n")
    print(method + " " + url)
    print('\n'.join(header))
    print("")

    if body != "no_body":
        print(body)
        all_request +="\n"+body

    all_request += "\n"+"-"*60+"\n"
    print("-" * 60)

    file1 = open(output_file, "a")  # append mode
    file1.write(all_request)
    file1.close()

    headers.clear()


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
    h_name = h_name.lower()                                                     # Convert header names to lowercase
    headers[h_name] = h_value                                                   # Header name and value


def set_curl_opt(c, url, header, b_obj):
    c.setopt(c.URL, url)                                                        # set the url
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE)   # Set HTTP2 protocol
    c.setopt(pycurl.HTTPHEADER, header)
    c.setopt(c.HEADERFUNCTION, display_header)
    c.setopt(c.WRITEDATA, b_obj)                                                # where curl will put the body


def GET_method_http2(url, header, output_file):
    global status_code_response
    b_obj = BytesIO()

    c = pycurl.Curl()
    set_curl_opt(c, url, header, b_obj)
    c.perform()
    status_code_response = c.getinfo(pycurl.HTTP_CODE)
    c.close()

    print_response(headers, b_obj, output_file)
    status_code_response = "no_status_code"

    b_obj.close()


def DELETE_method_http2(url_c, custom_header, output_file):
    b_obj = BytesIO()

    # set request data
    c = pycurl.Curl()
    set_curl_opt(c, url_c, custom_header, b_obj)
    c.setopt(c.CUSTOMREQUEST, 'DELETE')

    c.perform()
    c.close()

    # see response
    print_response(headers, b_obj, output_file)
    b_obj.close()


def POST_method_http2(url, custom_header, data_post, output_file):
    pf = data_post.encode('utf-8')
    b_obj = BytesIO()

    c = pycurl.Curl()
    set_curl_opt(c, url, custom_header, b_obj)
    if data_post != "no_body":
        c.setopt(c.POSTFIELDS, pf)                                              # Set Payload for POST, PUT, PATCH...

    c.perform()
    c.close()

    print_response(headers, b_obj, output_file)
    b_obj.close()


def PUT_method_http2(url, custom_header, data_post, output_file):
    pf = data_post.encode('utf-8')
    b_obj = BytesIO()

    c = pycurl.Curl()
    set_curl_opt(c, url, custom_header, b_obj)
    c.setopt(c.CUSTOMREQUEST, 'PUT')

    if data_post != "no_body":
        c.setopt(c.POSTFIELDS, pf)                                          # Set Payload for POST, PUT, PATCH...

    c.perform()
    c.close()

    print_response(headers, b_obj, output_file)
    b_obj.close()


def PATCH_method_http2(url, custom_header, output_file):
    b_obj = BytesIO()

    c = pycurl.Curl()
    set_curl_opt(c, url, custom_header, b_obj)
    c.setopt(c.CUSTOMREQUEST, 'PATCH')

    c.perform()
    c.close()

    print_response(headers, b_obj, output_file)
    b_obj.close()


def OPTIONS_method_http2(url, custom_header, output_file):
    b_obj = BytesIO()

    c = pycurl.Curl()
    set_curl_opt(c, url, custom_header, b_obj)
    c.setopt(c.CUSTOMREQUEST, 'OPTIONS')

    c.perform()
    c.close()

    print_response(headers, b_obj, output_file)
    b_obj.close()


def main():
    global counter_request

    print("Welcome to 5GHTTPModifier\n")
    print("This tool will help you to send automatic request in HTTP/2\n")
    print("")
    print("Parameters need to start the script (keyboard-interact): ")
    print(" 1. Path input files \n 2. Input filename \n 3. Output filename \n 4. IP Source in the input files \n"
          " 5. Target IP and/or Port\n")

    print("Path with all the files XML to analyze:")
    # path = "/home/corenetwork/PycharmProjects/API_Injection_Open5GS/ToTest/"
    path_c = input()

    print("What are filename to be searched?")
    # filename = oai_test
    filename_c = input()

    print("Define the output filename")
    # filename_output = open5gs_test
    filename_output_c = input()

    print("IPSource")
    # ip_source = 192.168.70.130
    ip_source_c = input()

    print("You need to specify a target port? (Y/N)")
    portYN_c = input()

    if portYN_c == "Y":
        print("IPTarget:Port")
        # ipPort = 127.0.0.10:7777
        ipPort_c = input()
        ip_target_c = ipPort_c.split(":")[0]
        port_target_c = ipPort_c.split(":")[1]
    else:
        print ("IPTarget")
        ip_target_c = input()
        port_target_c = "noPort"

    path = path_c
    IpHeader_target = "Host: " + ip_target_c        # ie. Host: 127.0.0.10
    IPHeader_source = "Host: " + ip_source_c        # ie. Host: 192.168.70.130

    for filename in os.listdir(path):                                                       # scan each directory
        fpath = path + filename
        if os.path.isdir(fpath):
            for files in os.listdir(fpath):                                                 # scan each file
                # is the name of the file to test
                if files == filename_c:
                    file_test = fpath+"/"+files                                             # file to test
                    output_file = fpath+"/"+str(filename_output_c)
                    counter_request = 0

                    with open(file_test, 'r') as f:
                        doc = xmltodict.parse(f.read())

                    ctr = 0                                                                 # counter for requests
                    for item in doc['items']['item']:
                        ctr += 1

                        # body initialization
                        data = "no_body"

                        # url
                        url = item['url']
                        if port_target_c == "noPort":
                            url = url.replace(ip_source_c, ip_target_c)            # Substitute with IP of Open5GS
                        else:
                            url = url.replace(ip_source_c, ipPort_c)            # Substitute with IP of Open5GS

                        # method
                        method = item['method']

                        # header
                        header = item['request']['#text']
                        header = header.split("\n")
                        del header[0]                                              # delete first element: METHOD + PATH
                        header = [x for x in header if "Content-Length: " not in x]              # delete Content-Lenght

                        for item2 in header:                                             # substitute with IP of Open5GS
                            idx = header.index(item2)
                            header[idx] = header[idx].lstrip()
                            if IPHeader_source in item2:
                                header[idx] = header[idx].replace(IPHeader_source, IpHeader_target)

                        try:
                            if method == "POST":

                                # retrive body data: {'field': 'value'} - all data after last backspace
                                payload, header_end = retrive_payload(header)
                                header = header[:header_end]

                                print_request(method, url, header, payload, output_file)  # print sent request
                                POST_method_http2(url, header, payload, output_file)

                            elif method == "GET":
                                print_request(method, url, header, data, output_file)  # print sent request
                                GET_method_http2(url, header, output_file)

                            elif method == "DELETE":
                                print_request(method, url, header, data, output_file)  # print sent request
                                DELETE_method_http2(url, header, output_file)

                            elif method == "PUT":
                                print_request(method, url, header, data, output_file)  # print sent request
                                PUT_method_http2(url, header, data, output_file)

                            elif method == "OPTIONS":
                                print_request(method, url, header, data, output_file)  # print sent request
                                OPTIONS_method_http2(url, header, output_file)

                            elif method == "PATCH":
                                print_request(method, url, header, data, output_file)  # print sent request
                                PATCH_method_http2(url, header, output_file)

                            else:
                                print("Method not found")

                        except pycurl.error as e:
                            print("An error occurred - probably some request crashed your server, \
                            do you want to continue? Y/N")

                            user_action = input()
                            if user_action == "Y":
                                continue
                            else:
                                print("Your last request is the Request number " + str(counter_request))
                                break

                    print("next file ready to analyze. Press any key to continue")
                    input()

if __name__ == "__main__":
    main()




