import pymongo
import json

class MongoDB:
    # 初始化连接MongoDB数据库
    def __init__(self, host, port, db_name, username=None, password=None):
        self._client = pymongo.MongoClient(host, port, username=username, password=password)
        self._db = self._client[db_name]

    # 插入单个文档
    def insert_one(self, collection_name, document):
        return self._db[collection_name].insert_one(document)

    # 查询单个文档
    def find_one(self, collection_name, filter=None):
        return self._db[collection_name].find_one(filter)

    # 查询多个文档
    def find_many(self, collection_name, filter=None):
        return self._db[collection_name].find(filter)

    # 更新单个文档
    def update_one(self, collection_name, filter, update):
        return self._db[collection_name].update_one(filter, update)

    # 更新多个文档
    def update_many(self, collection_name, filter, update):
        return self._db[collection_name].update_many(filter, update)

    # 删除单个文档
    def delete_one(self, collection_name, filter):
        return self._db[collection_name].delete_one(filter)

    # 删除多个文档
    def delete_many(self, collection_name, filter):
        return self._db[collection_name].delete_many(filter)

    # 断开与MongoDB的连接
    def close(self):
        self._client.close()


if __name__ == '__main__':
    # 创建一个MongoDB实例
    mongo = MongoDB(host='localhost', port=27017, db_name='mydb')

    # 插入一条数据
    with open("../json_data_sample/activities.json",'r',encoding='utf-8') as f:
        result = mongo.insert_one(collection_name='activity', document=json.load(f))
    print(result)

    # 查询一条数据
    # result = mongo.find_one(collection_name='users', filter={'data': 0})
    # print(result)

    # 查询多条数据
    result = mongo.find_many(collection_name='activity')
    for r in result:
        print(r)

    # # 更新数据
    result = mongo.update_one(collection_name='users', filter={'user': 'Tom'}, update={'$set': {'age': 35}})
    print(result)

    # 删除数据
    result = mongo.delete_one(collection_name='users', filter={'name': 'Tom'})
    print(result)

    # 关闭连接
    mongo.close()
