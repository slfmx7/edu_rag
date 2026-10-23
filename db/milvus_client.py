import random

from pymilvus import MilvusClient, DataType, AnnSearchRequest, RRFRanker, WeightedRanker


def init_milvus():
    milvus_client = MilvusClient(uri='http://localhost:19530')

    print(milvus_client.list_databases())

    # 判断db是否存在
    if "milvus_demo" not in milvus_client.list_databases():
        milvus_client.create_database('milvus_demo')

    return milvus_client

# 操作集合
def operate_collection():
    milvus_client = init_milvus()

    milvus_client.use_database(db_name="milvus_demo")

    schemas = milvus_client.create_schema(enable_dynamic_field=True)

    # 添加字段
    # 标量
    schemas.add_field(field_name='id',datatype=DataType.INT64,is_primary=True)
    # 向量
    schemas.add_field(field_name='vector',datatype=DataType.FLOAT_VECTOR,is_primary=False,dim=5)
    # 标量
    #schemas.add_field(field_name='score',datatype=DataType.FLOAT,nullable=True)
    schemas.add_field(field_name='color',datatype=DataType.VARCHAR,max_length=50)

    if milvus_client.has_collection('milvus_demo_collection'):
        print(f"检测到集合 '{'milvus_demo_collection'}' 已存在，正在删除以避免索引冲突...")
        milvus_client.drop_collection('milvus_demo_collection')

    # 创建集合
    if "milvus_demo_collection" not in milvus_client.list_collections():
        (milvus_client
         .create_collection(collection_name='milvus_demo_collection',schema=schemas))

    # 创建向量索引
    index_params_1 = milvus_client.prepare_index_params(field_name='vector',
                                                        metric_type="COSINE",
                                                        index_type="IVF_FLAT",
                                                        index_name="vector_index",
                                                        params={
        "nlist":128
    })

    milvus_client.create_index(collection_name='milvus_demo_collection', index_params=index_params_1)

    # 创建标量索引
    index_params_2 = milvus_client.prepare_index_params(field_name='color',index_type='INVERTED',index_name="color_index")

    milvus_client.create_index(collection_name='milvus_demo_collection', index_params=index_params_2)

    # 查看索引信息
    print(milvus_client.describe_index(collection_name='milvus_demo_collection',index_name="color_index"))
    print(milvus_client.describe_index(collection_name='milvus_demo_collection',index_name="vector_index"))


    # 删除集合
    # if "milvus_demo_collection" not in milvus_client.list_collections():
    #     milvus_client.use_database(db_name='default').drop_collection(collection_name='milvus_demo_collection')
    #
    # print(milvus_client.list_collections())

def operate_insert_entity():
    milvus_client = init_milvus()
    milvus_client.use_database(db_name="milvus_demo")
    data = [
        {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354,
                             0.9029438446296592], "color": "pink_8682"},
        {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501,
                             0.838729485096104], "color": "red_7025"},
        {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185,
                             0.20785793220625592], "color": "orange_6781"},
        {"id": 3, "vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995,
                             0.95791889146345], "color": "pink_9298"},
        {"id": 4, "vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184,
                             0.30337481143159106], "color": "red_4794"},
        {"id": 5, "vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383,
                             -0.1446277761879955], "color": "yellow_4222"},
        {"id": 6, "vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192,
                             -0.8984947637863987], "color": "red_9392"},
        {"id": 7, "vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709,
                             0.5378064918413052], "color": "grey_8510"},
        {"id": 8, "vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872,
                             -0.6140360785406336], "color": "white_9381"},
        {"id": 9, "vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717,
                             -0.6980531615588608], "color": "purple_4976"}
    ]
    milvus_client.insert(collection_name='milvus_demo_collection', data=data)

def operate_partition_insert_entity():
    collection_name = "milvus_demo_collection"
    partition_name = "partition_demo_1"
    database_name = "milvus_demo"
    data = [
        {"id": 0, "vector": [-0.619954382375778, 0.4479436794798608, -0.17493894838751745, -0.4248030059917294,
                             -0.8648452746018911], "color": "black_9898"},
        {"id": 1, "vector": [0.4762662251462588, -0.6942502138717026, -0.4490002642657902, -0.628696575798281,
                             0.9660395877041965], "color": "red_7319"},
        {"id": 2, "vector": [-0.8864122635045097, 0.9260170474445351, 0.801326976181461, 0.6383943392381306,
                             0.7563037341572827], "color": "white_6465"},
        {"id": 3, "vector": [0.14594326235891586, -0.3775407299900644, -0.3765479013078812, 0.20612075380355122,
                             0.4902678929632145], "color": "orange_7580"},
        {"id": 4, "vector": [0.4548498669607359, -0.887610217681605, 0.5655081329910452, 0.19220509387904117,
                             0.016513983433433577], "color": "red_3314"},
        {"id": 5, "vector": [0.11755001847051827, -0.7295149788999611, 0.2608115847524266, -0.1719167007897875,
                             0.7417611743754855], "color": "black_9955"},
        {"id": 6, "vector": [0.9363032158314308, 0.030699901477745373, 0.8365910312319647, 0.7823840208444011,
                             0.2625222076909237], "color": "yellow_2461"},
        {"id": 7, "vector": [0.0754823906014721, -0.6390658668265143, 0.5610517334334937, -0.8986261118798251,
                             0.9372056764266794], "color": "white_5015"},
        {"id": 8, "vector": [-0.3038434006935904, 0.1279149203380523, 0.503958664270957, -0.2622661156746988,
                             0.7407627307791929], "color": "purple_6414"},
        {"id": 9, "vector": [-0.7125086947677588, -0.8050968321012257, -0.32608864121785786, 0.3255654958645424,
                             0.26227968923834233], "color": "brown_7231"}
    ]
    # 创建分区
    milvus_client = init_milvus()
    milvus_client.use_database(database_name)
    milvus_client.create_partition(collection_name=collection_name,partition_name=partition_name)
    # 分区插入
    milvus_client.insert(collection_name=collection_name,
                         partition_name=partition_name,
                         data=data)

# query 是 “按标量条件捞数据（可包含向量）”，search 是 “按向量算相似度找数据”
def operate_query_base_entity():
    milvus_client = init_milvus()
    collection_name = "milvus_demo_collection"
    partition_name = "partition_demo_1"
    database_name = "milvus_demo"
    milvus_client.use_database(database_name)
    data = [[0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104]]
    # 添加标量过滤条件
    data_1 = milvus_client.query(collection_name=collection_name,
                        search_params={
                            "metric_type": "L2",
                        },
                        limit=3,
                        filter='color like "%red%"',
                        output_fields=["id", 'vector','color']
                        )
    # 指定分区查询
    data_2 = milvus_client.query(collection_name=collection_name,
                                 search_params={
                                     "metric_type": "COSINE",
                                 },
                                 limit=3,
                                 partition_names=[partition_name],
                                 output_fields=["id", 'vector','color']
                                 )
    print(data_1)
    print(data_2)
    # 使用search metric_type参数必须和建表的相似度计算算法一致
    # 如果使用余弦相似度或者内积相似度算法 radius表示下限 range_filter表示上限，而如果使用欧氏距离 radius表示上限 range_filter表示下限
    data_3 = milvus_client.search(collection_name=collection_name,
                                  data=data,
                                  limit=3,
                                  search_params={
        "params":{
            "radius": 0.8,  # 搜索圆的半径
            "range_filter": 1
        }
    },
                                  output_fields=["id", 'vector', 'color']
    )
    print(data_3)

def operate_complex_insert_data():
    milvus_client = init_milvus()
    collection_name = "milvus_complex_demo_collection"
    database_name = "milvus_demo"
    milvus_client.use_database(database_name)
    # # 定义schema
    schema = milvus_client.create_schema(enable_dynamic_field=False)
    schema.add_field(field_name='film_id', datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name='filmVector', datatype=DataType.FLOAT_VECTOR, dim=5)  # 向量字段
    schema.add_field(field_name="posterVector", datatype=DataType.FLOAT_VECTOR, dim=5)  # 向量字段
    # #
    # 定义索引
    index_params = milvus_client.prepare_index_params()
    # 使用倒排索引 nlist 表示聚类中心数量
    index_params.add_index(field_name='filmVector', index_type="IVF_FLAT",
                           metric_type="L2", params={"nlist": 128})
    # 使用暴力搜索
    index_params.add_index(field_name='posterVector', index_type="",
                           metric_type="COSINE")
    # 创建集合
    milvus_client.create_collection(collection_name=collection_name, schema=schema, index_params=index_params)
    # 创建实体
    datas = []
    for _ in range(1000):
        film_id = random.randint(1,1000)
        filmVector = [random.random() for _ in range(5)]
        posterVector = [random.random() for _ in range(5)]
        datas.append({"film_id": film_id, "filmVector": filmVector, "posterVector": posterVector})
    # 插入数据
    milvus_client.insert(collection_name=collection_name,data=datas)


def operate_rrf_rank_search_data():
    milvus_client = init_milvus()
    collection_name = "milvus_complex_demo_collection"
    database_name = "milvus_demo"
    milvus_client.use_database(database_name)

    query_posterVector = [
        [0.02550758562349764, 0.006085637357292062, 0.5325251250159071, 0.7676432650114147, 0.5521074424751443]]

    query_filmVector = [
        [0.8896863042430693, 0.370613100114602, 0.23779315077113428, 0.38227915951132996, 0.5997064603128835]]

    posterVector_search = {
        "data": query_posterVector,
        "limit": 3,
        "anns_field":"posterVector",
        "param":{
            "metric_type": "COSINE"
        }
    }
    request_1=AnnSearchRequest(**posterVector_search)
    # nprobe 表示访问聚类中心数量
    filmVector_search = {
        "data": query_filmVector,
        "limit": 3,
        "anns_field":"filmVector",
        "param":{
            "metric_type": "L2",
            "nprobe":10
        }
    }
    request_2 = AnnSearchRequest(**filmVector_search)
    request = [request_1,request_2]
    rrf_ranker = RRFRanker(100)
    data = milvus_client.hybrid_search(collection_name=collection_name,
                                reqs=request,
                                ranker=rrf_ranker,
                                limit=2)
    print(data)

def operate_weight_search_data():
    milvus_client = init_milvus()
    collection_name = "milvus_complex_demo_collection"
    database_name = "milvus_demo"
    milvus_client.use_database(database_name)

    query_posterVector = [
        [0.02550758562349764, 0.006085637357292062, 0.5325251250159071, 0.7676432650114147, 0.5521074424751443]]

    query_filmVector = [
        [0.8896863042430693, 0.370613100114602, 0.23779315077113428, 0.38227915951132996, 0.5997064603128835]]

    WeightedRanker()
    posterVector_search = {
        "data": query_posterVector,
        "limit": 3,
        "anns_field": "posterVector",
        "param": {
            "metric_type": "COSINE"
        }
    }
    request_1 = AnnSearchRequest(**posterVector_search)
    # nprobe 表示访问聚类中心数量
    filmVector_search = {
        "data": query_filmVector,
        "limit": 3,
        "anns_field": "filmVector",
        "param": {
            "metric_type": "L2",
            "nprobe": 10
        }
    }
    request_2 = AnnSearchRequest(**filmVector_search)
    request = [request_1, request_2]
    rrf_ranker = WeightedRanker(0.7,0.3)
    data = milvus_client.hybrid_search(collection_name=collection_name,
                                       reqs=request,
                                       ranker=rrf_ranker,
                                       limit=2)
    print(data)

if __name__ == "__main__":
    # operate_collection()
    # operate_insert_entity()
    # operate_partition_insert_entity()
    # operate_query_base_entity()
    # operate_complex_insert_data()
    # operate_rrf_rank_search_data()
    operate_weight_search_data()