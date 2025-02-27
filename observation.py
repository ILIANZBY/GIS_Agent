import geopandas as gpd
import ast
import matplotlib.pyplot as plt

file_path = '/share/home/wuqingyao_zhangboyang/GIS_Agent2/gis_data/镇安镇建筑矢量.shp'
gdf = gpd.read_file(file_path)

def observate(command_str):
    """
    执行地理数据处理命令，支持计算与绘图功能
    :param command_str: 包含数据处理、计算和绘图命令的字符串
    :param gdf: geopandas GeoDataFrame 输入数据
    :return: 计算结果列表（排除绘图语句的结果）
    """
    lines = [line.strip() for line in command_str.strip().split('\n') if line.strip()]
    local_vars = {
        'gdf': gdf,
        'plt': plt,  # 注入 matplotlib 模块
        'gpd': gpd,  # 注入 geopandas 模块
        'Figure': plt.Figure  # 允许创建图形对象
    }
    results = []
    
    # 自动关闭已有图形防止内存泄漏
    plt.close('all')

    for line in lines:
        try:
            # 语法分析判断是否为表达式
            ast.parse(line, mode='eval')
            is_expression = True
        except SyntaxError:
            is_expression = False

        try:
            if is_expression:
                # 执行并收集计算结果
                result = eval(
                    line,
                    {"__builtins__": {}},  # 保持安全沙箱
                    local_vars
                )
                results.append(result)
            else:
                # 执行绘图等副作用语句
                exec(
                    line,
                    {"__builtins__": {}},  # 保持安全沙箱
                    local_vars
                )
        except Exception as e:
            plt.close('all')  # 发生错误时清理图形
            raise RuntimeError(f"执行失败: {line}\n错误类型: {type(e).__name__}\n错误详情: {str(e)}")

    # 自动清理图形资源
    plt.close('all')
    return results