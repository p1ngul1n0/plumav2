import requests
import warnings

warnings.filterwarnings('ignore')

class Scan:
    def __init__(self,url,proxy):
        self.url = url
        if proxy != '':
            self.proxy = { 'http'  : 'http://'+proxy, "https" : 'https://'+proxy, "ftp" : 'ftp://'+proxy }
            self.response = requests.get(url=self.url,verify=False,proxies=self.proxy)
        else:
            self.proxy = ''
            self.response = requests.get(url=self.url,verify=False)
        self.headers  = self.response.headers
    def heads(self):
        secure = ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options', 'X-Permitted-Cross-Domain-Policies', 'Referrer-Policy', 'Expect-CT', 'Feature-Policy']
        sensitive = ['Server', 'X-Powered-By', 'X-Aspnet-Version', 'X-AspNetMvc-Version']
        returnSecureHeaders = {}
        returnSensitiveHeaders = {}
        for header in secure:
            if header in self.headers:
                returnSecureHeaders[header] = self.headers[header]
        for header in sensitive:
            if header in self.headers:
                returnSensitiveHeaders[header] = self.headers[header]
        return returnSecureHeaders,returnSensitiveHeaders
    def method(self):
        methods = ['GET','POST','DELETE','TRACE','CONNECT','PUT','HEAD','BOB']
        returnMethods = {}
        for method in methods:
            if self.proxy != '':
                response = requests.request(method,self.url,verify=False,proxies=self.proxy)
            else:
                response = requests.request(method,self.url,verify=False)
            returnMethods[method] = '['+str(response.status_code)+'] '+response.reason
        return returnMethods
    def enum(self,payload_file):
        with open('payload_files/'+payload_file) as payloads:
            returnDirectories = []
            i = 0
            for payload in payloads:
                directory = {}
                if self.proxy != '':
                    response = requests.get(url=self.url+'/'+payload.strip(),verify=False,proxies=self.proxy)
                else:
                    response = requests.get(url=self.url+'/'+payload.strip(),verify=False)
                directory['id'] = i
                directory['payload'] = payload.strip()
                directory['status'] = str(response.status_code)
                directory['reason'] = response.reason
                directory['size'] = len(response.content)
                directory['content'] = response.text
                returnDirectories.append(directory)
                i += 1
            return returnDirectories
