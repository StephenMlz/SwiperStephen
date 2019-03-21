from qiniu import Auth,put_file

from  swiper import config

def upload_qncloud(filename,filepath):
    '''上传文件到七牛云服务器'''

    #构建鉴权对象
    qn_auth = Auth(config.QN_ACCESSKEY,config.QN_SECRETKEY)


    #生成上传token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET,filename,3600)


    #执行上传过程
    ret,info = put_file(token,filename,filepath)
    return ret,info
