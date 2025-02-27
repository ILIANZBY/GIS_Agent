

import geopandas as gpd
import matplotlib.pyplot as plt

# 读取文件
gdf = gpd.read_file('/share/home/wuqingyao_zhangboyang/GIS_Agent2/gis_data/镇安镇建筑矢量.shp')
building = gdf.iloc[1000]
area = building.geometry.area
elevation = building[['ELEVATION']]
print(f"建筑5的面积: {area}, 高度: {elevation}")

geometry = gpd.GeoSeries([building.geometry])
geometry.plot()
plt.savefig('building_1000.png', bbox_inches='tight', dpi=300)
# # 绘图设置
# fig, ax = plt.subplots(figsize=(15, 10))
# gdf.plot(

# )



# # 保存图片
# plt.savefig('镇安镇建筑矢量.png', bbox_inches='tight', dpi=300)
