from langchain.prompts import PromptTemplate

#given information放rag检索到的审核要求

PLAN = """
你是一个土地审核的规划者，把任务分为多个子任务。
***** Example *****

Query: 请审核第3个建筑是否符合建筑要求,并画出该建筑的图片
Plan:要完成审核建筑超级机器人研究院是否符合建筑要求，需要审核它的建筑面积是否符合要求。把任务分为以下几个子任务：1.选择目标建筑的数据。2.计算目标建筑的面积。3.计算建筑高度。4.画出建筑的图片。5.保存图片。

***** Example Ends *****
Given information: {text}
Query: {query}{scratchpad}
Plan:
"""


ACT = """你是一个土地审核的geopandas工具调用专家，你需要根据提供的信息，每一个子任务需要调用什么函数。你可以调用以下函数：
(1)building = gdf.iloc[i]# 选择第i个建筑
(2)building.geometry.area # 计算面积（单位：平方米 ）
(3)gpd.building[['ELEVATION']]  # 获取建筑的高度
(3)GeoSeries([building.geometry]).plot() # 画出建筑的图片
(4)plt.savefig('building_i.png', bbox_inches='tight', dpi=300) # 保存图片
***** Example *****

Query: 请审核第3个建筑是否符合建筑要求,并画出该建筑的图片\nPlan:要完成审核建筑超级机器人研究院是否符合建筑要求，需要审核他的建筑面积是否符合要求。把任务分为以下几个子任务：1.选择目标建筑的数据。2.计算目标建筑的面积。3.计算建筑高度。4.画出建筑的图片。5.保存图片。
Act: building = gdf.iloc[3] \n building.geometry.area \n building[['ELEVATION']] \n gpd.GeoSeries([building.geometry]).plot() \n plt.savefig('building_3.png', bbox_inches='tight', dpi=300)

***** Example Ends *****
注意：在回答问题时智能调用上述的函数，不需要给注释，不需要输出其他的信息，不需要将结果与允许高度进行比较。
Given information: {text}
Query: {query}{scratchpad}
Act:
"""

SUM="""你是一个土地规划的总结者，你需要根据前面的子任务以及子任务的完成结果来做出总结，给出最后的审核结果和建议。
***** Example *****

Given information:建筑的占地面积要求在500平方米以下，高度在10米以下。
Query: 请审核第3个建筑是否符合建筑要求,并画出该建筑的图片\nPlan:要完成审核建筑超级机器人研究院是否符合建筑要求，需要审核他的建筑面积是否符合要求。把任务分为以下几个子任务:1.选择目标建筑的数据。2.计算目标建筑的面积。3.计算建筑高度。4.画出建筑的图片。5.保存图片。\nAct: building = gdf.iloc[3] \n building.geometry.area \n building[['ELEVATION']] \n gpd.GeoSeries([building.geometry]).plot() \n plt.savefig('building_3.png', bbox_inches='tight', dpi=300)\nObservation: [600*e-6，5]
Summary:
审核结果：第三个建筑面积为600平方米，大于要求最大允许面积500平方米，建筑的高度为5米，小于最大允许高度10米。综上所述，不符合建筑要求。
审核建议：建议减少第三个建筑的面积，以符合建筑要求。
***** Example Ends *****
Given information: {text}
Query: {query}{scratchpad}
Summary:
"""

SUM2="""你是一个土地规划的总结者，你需要根据前面的子任务以及子任务的完成结果来做出总结，给出最后的审核结果和建议。
如果前面做出的计划不合理或者有行动没有完成，你需要继续制定计划，指导行动。
***** Example *****

Given information:研究院要求面积在1500平方米以下。
Query: 请审核建筑超级机器人研究院是否符合建筑要求\nPlan:要完成审核建筑超级机器人研究院是否符合建筑要求，需要审核他的建筑面积是否符合要求。把任务分为以下几个子任务1.选择目标建筑的数据。2.计算目标建筑的面积。\nAct: country_data = gdf[gdf["NAME_CHN"] == '超级机器人研究院'] \n country_data.geometry.area.values[0] \n country_data.plot() \n plt.savefig('超级机器人研究院.png', bbox_inches='tight', dpi=300)\nObservation: [1000]
Summary: 审核建筑超级机器人研究院是否符合建筑要求的结果是：面积为1000平方米，符合建筑要求。

***** Example Ends *****
Given information: {text}
Query: {query}{scratchpad}
Summary:
"""



plan_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = PLAN,
                        )

act_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = ACT,
                        )

summary_agent_prompt = PromptTemplate(
                        input_variables=["text","query", "scratchpad"],
                        template = SUM,
                        )
