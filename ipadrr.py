from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

# 假设 GeoLite2-City.mmdb 文件位于项目的根目录
GEOIP_DATABASE = './GeoLite2-City.mmdb'

def get_location(ip):
    try:
        with Reader(GEOIP_DATABASE) as reader:
            response = reader.city(ip)
            country = response.country.name
            city = response.city.name
            return country, city
    except AddressNotFoundError:
        # 如果数据库中找不到IP地址，返回未知
        return 'Unknown', 'Unknown'
    except Exception as e:
        # 处理其他可能的异常
        print(f"Error while looking up {ip}: {e}")
        return 'Error', 'Error'
