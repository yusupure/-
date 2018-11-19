import hashlib
def MD5_sh(text):
    if isinstance(text,str):
        text=text.encode('utf-8')
    md5=hashlib.md5()
    md5.update(text)
    return (md5.hexdigest())

