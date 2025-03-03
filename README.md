用于GIS数据交互的多智能体推理框架

整体流程图：

![image](https://github.com/user-attachments/assets/c34df420-7ebb-4ff9-b16f-da9acbddbf97)

效果演示：


<img width="884" alt="570453dd8d977d709ec44c77f76037a" src="https://github.com/user-attachments/assets/f1992b76-27e5-42c7-8ec1-8ec91b021b36" />

## 配置环境

克隆本项目
```shell
git clone https://github.com/ILIANZBY/GIS_Agent.git
cd GIS_Agent
```

推理端环境配置
```shell
conda create -n xinference python=3.9
conda activate xinference
pip install "xinference[all]"
pip install "xinference[vllm]"
```

gis端环境配置
```shell
conda env create -f environment.yml
```

推理端启动
```shell
xinference-local --host 0.0.0.0 --port 9876
```
然后再webui上launch模型qwen2-vl-instruct


启动webui
```shell
python webui.py
```
