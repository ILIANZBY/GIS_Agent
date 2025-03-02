import geopandas as gpd
import matplotlib.pyplot as plt

# 读取建筑物shp文件
gdf = gpd.read_file('/share/home/wuqingyao_zhangboyang/GIS_Agent2/gis_data/镇安镇建筑矢量.shp')  # 请替换为实际的shp文件路径

# 创建输出文本文件
with open('buildings_info.txt', 'w', encoding='utf-8') as f:
    # 遍历每个建筑物
    for i in range(len(gdf)):
        # 获取当前建筑物
        building = gdf.iloc[i]
        
        # 计算面积（平方米）
        area = building.geometry.area * 10**10
        
        # 获取高度
        elevation = building['ELEVATION']  # 假设高度字段名为'ELEVATION'
        
        # 生成输出字符串
        output_str = f"建筑{i}的面积为{area:.2f}平方米。高度为{elevation}\n"
        
        # 写入文件
        f.write(output_str)
        

        # 打印进度
        print(f"已处理建筑 {i+1}/{len(gdf)}")