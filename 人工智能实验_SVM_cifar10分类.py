

if __name__=='__main__':
    #分类标签
    name={'airplane':0,'automobile':1,'bird':2, 'cat':3, 'deer':4,'dog':5,'frog':6,'horse':7,'ship':8,'truck':9}
    #导入数据路径
    path='C:/Users/11215/Desktop/data2/cifar'

    split='train'
    num=50000
    X_train,Y_train=get_data(name,path,split,num)

    split='test'
    num=10000
    X_test,Y_test=get_data(name,path,split,num)


