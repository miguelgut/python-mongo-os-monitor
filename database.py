## Arquivo de configuração do banco de dados
import pymongo
from pymongo import MongoClient
import numpy as np
import bsonnumpy

# Dicionário que relaciona os campos do mongo com tipos de dados 
global dtype
dtype = np.dtype([
    ('_id', 'S12'), 
    ('disk_usage', np.double), 
    ('date', np.int64), 
    ('cpu_percent', np.double)
])

class Mongo(object):

    # Inicia o cliente
    def __init__(self):
        cliente = MongoClient('mongodb://app:ucpel_2020@ucpelpivi-shard-00-00.h3o8t.gcp.mongodb.net:27017,ucpelpivi-shard-00-01.h3o8t.gcp.mongodb.net:27017,ucpelpivi-shard-00-02.h3o8t.gcp.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-13yvxa-shard-0&authSource=admin&retryWrites=true&w=majority', 27017)
        banco = cliente.pc_data
        Mongo.colecao = banco.pi_vi

    # Retorna todos os registros dado um periodo
    def findAll(self, start, end):
        filter = {"date":{"$gte": start, "$lt":end}}
        global dtype
        
        return bsonnumpy.sequence_to_ndarray(
            self.colecao.find_raw_batches(filter).limit(100).batch_size(100),
            dtype,
            self.colecao.count(filter)
        )

    # Retorna informações de CPU dado um período
    def findCpuUsage(self, start, end):
        filter = {"date":{"$gte": start, "$lt":end}}
        projection = {{"_id": True},{"cpu_usage": True}}
        global dtype
        
        return bsonnumpy.sequence_to_ndarray(
            self.colecao.find_raw_batches(filter,projection).limit(100).batch_size(100),
            dtype,
            self.colecao.count(filter)
        )
    
    # Retorna informações de uso de disco
    def findDiskUsage(self, start, end):
        filter = {"date":{"$gte": start, "$lt":end}}
        projection = {"disk_usage": True}
        global dtype
        
        return bsonnumpy.sequence_to_ndarray(
            self.colecao.find_raw_batches(filter,projection).limit(100).batch_size(100),
            dtype,
            self.colecao.count(filter)
        )

