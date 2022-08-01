# 【7-8暑期赛】中文文本语义纠错问题

&emsp;&emsp;用户问句的正确性、合法性是自然语言理解任务的基石。无论是语音输入还是手动输入都可能会引入文本语法错误，丢失文本中的重要信息。ASR转写错误或键盘录入错误是非常普遍的，对这类错误的纠正往往需要借助一些常识和语法知识，甚至推理的能力。

&emsp;&emsp;本算法主要应用于对话系统、外呼机器人等场景：（1）每一个业务场景的文本都有很强的领域特性，即，话语的范围（词，句的范围）是有限的，通常会有很多领域内词汇。（2） 我们期望通过基于领域相关的语料，训练一个纠错模型提高语言纠正的精度同时具有较快的速度。

- 本代码是该赛题的一个基础demo，仅供参考学习。
- 比赛地址：http://contest.aicubes.cn/
- 时间：2022-07 ~ 2022-08



## 如何运行Demo

- clone代码
- 准备其他模型
  - 下载模型： [chinese-bert-wwm](https://huggingface.co/hfl/chinese-bert-wwm)
- 准备环境
  - cuda10.0以上
  - python3.8以上
  - 安装python依赖
  ```
  python -m pip install -r requirements.txt
  ```
- 调整参数配置，参考[模板项目](https://github.com/10jqka-aicubes/project-de6o)的说明
  - 修改`gector/setting.conf`的路径，比如`TRAIN_FILE_DIR`的值为你存放训练集的位置
  - `gector/train/run.sh`，修改`BASE_MODEL`的值为下载预训练模型的位置
  - `gector/predict/run.sh` 同理
- 运行
  - 训练
  ```
  bash gector/train/run.sh
  ```
  - 预测
  ```
  bash gector/predict/run.sh
  ```
  - 计算结果指标
  ```
  bash gector/metrics/run.sh
  ```

## 反作弊声明

1）参与者不允许在比赛中抄袭他人作品、使用多个小号，经发现将取消成绩；

2）参与者禁止在指定考核技术能力的范围外利用规则漏洞或技术漏洞等途径提高成绩排名，经发现将取消成绩；

3）在A榜中，若主办方认为排行榜成绩异常，需要参赛队伍配合给出可复现的代码。



## 赛事交流

![同花顺比赛小助手](http://speech.10jqka.com.cn/arthmetic_operation/245984a4c8b34111a79a5151d5cd6024/客服微信.JPEG)