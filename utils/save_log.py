import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# ==== Logger Utils ====
def Logger_Days(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                    datefmt='%Y/%m/%d %H:%M:%S')
    handler = TimedRotatingFileHandler(filename = '%s.log' %(file_name), when="D", backupCount=20, encoding='utf-8')
    log_obj = logging.getLogger(file_name)
    log_obj.setLevel(logging.INFO)
    # Tránh add nhiều handler khi gọi lại nhiều lần
    if not log_obj.hasHandlers():
        handler.setFormatter(formatter)
        log_obj.addHandler(handler)
        log_obj.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log_obj.info("Logger object created successfully..")
    return log_obj

def Logger_maxBytes(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                    datefmt='%Y/%m/%d %H:%M:%S')
    handler = RotatingFileHandler(filename = '%s.log' %(file_name), mode = 'a', maxBytes=1024*1024, backupCount=5, 
                                  encoding='utf-8', delay=0)
    log_obj = logging.getLogger(file_name)
    log_obj.setLevel(logging.INFO)
    if not log_obj.hasHandlers():
        handler.setFormatter(formatter)
        log_obj.addHandler(handler)
        log_obj.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log_obj.info("Logger object created successfully..")
    return log_obj

# File này chỉ dùng để ghi log ra file (logging), không thay thế được chức năng của Kafka.
# - Logging: chỉ ghi lại sự kiện, lỗi, thông tin hệ thống để kiểm tra/debug.
# - Kafka: dùng để truyền thông điệp (event/message) giữa các thành phần hệ thống, hỗ trợ realtime, phân tán, mở rộng.
# Nếu bạn chỉ cần ghi log, dùng file này là đủ.
# Nếu cần truyền dữ liệu realtime giữa các service, phải dùng Kafka hoặc message queue khác.

# Bạn có thể sử dụng Logger_Days hoặc Logger_maxBytes ở bất kỳ đâu trong dự án để ghi log ra file.
# Ví dụ:
# from utils.save_log import Logger_Days
# logger = Logger_Days("mylog")
# logger.info("Some message")
# logger.error("Some error")

# Chức năng của file log (save_log.py):
# - Ghi lại các sự kiện, thông báo, lỗi, hoặc thông tin hoạt động của hệ thống vào file log trên ổ đĩa.
# - Hỗ trợ kiểm tra, giám sát, và debug ứng dụng khi cần thiết.
# - Có thể cấu hình ghi log theo ngày (Logger_Days) hoặc theo dung lượng tối đa (Logger_maxBytes).
# - Không truyền dữ liệu giữa các thành phần hệ thống, chỉ lưu lại lịch sử hoạt động để người quản trị hoặc lập trình viên xem lại.

# Ví dụ sử dụng:
# from utils.save_log import Logger_Days
# logger = Logger_Days("mylog")
# logger.info("Ứng dụng đã khởi động")
# logger.error("Có lỗi xảy ra khi đăng nhập")