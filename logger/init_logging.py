import logging
import os

# 日志为什么要输出到控制台的原因是,如果使用容器化docker部署不做任何处理（不添加挂载），
# 日志会写在容器里面，当容器重启那么就会丢失日志数据，因此输出到控制台是最好的选择
def init_logger(log_name, log_file='./logging.logger'):

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # level 设定日志级别 不会显示低级别的日志信息
    # filename 文件存储目录
    # filemode 表示写入方式 a表示追加
    logger = logging.getLogger(log_name)
    # 必须设置 logger 自身级别，否则默认继承 root 的 WARNING，debug/info 会被过滤掉
    logger.setLevel(logging.DEBUG)

    # 同时打印到控制台
    consle_log=logging.StreamHandler()
    consle_log.setLevel(logging.DEBUG)

    # 设置格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consle_log.setFormatter(formatter)

    file_hd = logging.FileHandler(log_file, encoding="utf-8")
    file_hd.setLevel(logging.DEBUG)
    file_hd.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(consle_log)
        logger.addHandler(file_hd)
    return logger

logger = init_logger('edu_rag', log_file='../logger/edu_rag.log')

if __name__ == "__main__":
    logger = init_logger('edu_rag', log_file='./edu_rag.log')

    # 记录不同级别的日志
    logger.debug("这是调试信息，通常用于开发")
    logger.info("程序运行正常")
    logger.warning("注意，可能有小问题")
    logger.error("发生错误")
    logger.critical("严重错误，程序可能崩溃")