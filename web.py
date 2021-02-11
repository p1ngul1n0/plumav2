import requests

class Scan:
    def __init__(self,url,proxy):
        self.url = url
        self.proxy = proxy
        self.response = requests.get(url=self.url,verify=False)
        self.headers  = self.response.headers
    def heads(self):
        secure = ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict Transport Security', 'X-Content-Type-Options', 'X-Permitted-Cross-Domain-Policies', 'Referrer-Policy', 'Expect-CT', 'Feature-Policy']
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
            response = requests.request(method,self.url,verify=False)
            returnMethods[method] = '['+str(response.status_code)+'] '+response.reason
        return returnMethods
    def enum(self,payload_file):
        with open('payload_files/'+payload_file) as payloads:
            returnDirectories = []
            i = 0
            for payload in payloads:
                directory = {}
                response = requests.get(url=self.url+'/'+payload.strip())
                directory['id'] = i
                directory['payload'] = payload.strip()
                directory['status'] = str(response.status_code)
                directory['reason'] = response.reason
                directory['size'] = len(response.content)
                returnDirectories.append(directory)
                i += 1
            return returnDirectories