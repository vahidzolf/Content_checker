import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def perform_curl(site):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, site)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()

    # HTTP response code, e.g. 200.
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    # Elapsed time for the transfer.
    dns_time = c.getinfo(c.NAMELOOKUP_TIME)
    print('DNS Time: %.4f' % dns_time)
    tcp_time = c.getinfo(c.CONNECT_TIME) - dns_time
    print('TCP Time: %.4f' % tcp_time)
    ssl_time = c.getinfo(c.APPCONNECT_TIME)
    print('SSL Time: %.4f' % ssl_time)
    STT_time = c.getinfo(c.STARTTRANSFER_TIME)
    print('Start Transfer Time: %.4f' % STT_time)
    # getinfo must be called before close.
    c.close()
    return [dns_time,tcp_time,ssl_time,STT_time]

output = open('cdn_output.csv','w')
sites =  open('cdn_support.txt','r')
flag = False

for cdn in sites.readlines():
    if cdn[-1] == '\n':
        cdn = cdn[:-1]
    res = perform_curl(cdn)
    print ('[' + cdn  + str(res) + ']')
    output.write(cdn + ',' + str(res[0]) + ',' + str(res[1])+ ',' + str(res[2]) + ',' + str(res[3]) + '\n' )
