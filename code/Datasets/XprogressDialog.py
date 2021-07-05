import requests

from contextlib import closing
class ProgressBar(object):
    def __init__(self,thread_name,
                 title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.thread_name = thread_name
        self.info = "【%s】%s %s  %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        rate = (self.count/self.chunk_size)/(self.total/self.chunk_size)*100
        _info = self.info % (self.title, self.status,str('{:.2f}'.format(rate)+'%'),
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info,rate

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        info,rate = self.__get_info()
        self.thread_name.str_float.emit(str(info),rate)
        print('\r'+ str(info), end="")

def download_rate(thread_name,filepath,url):
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        progress = ProgressBar(thread_name,url.split('/')[-1], total=content_size,
                               unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(filepath, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


if __name__ == '__main__':
    filepath = './a.gz'
    u = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    download_rate('sad',filepath,u)