# 数学建模国赛 + 美赛存档

本仓库用于整理和归档全国大学生数学建模竞赛及美国大学生数学建模竞赛的题目、论文、代码、数据与解题思路，方便团队复盘、经验沉淀与后续参赛备赛。主要使用的编程语言为 Python，MATLAB 针对 A 题等涉及物理类建模时以及涉及机器学习时使用，每个题目均尽可能提供 Python 与 MATLAB 实现。所有代码均经过测试，论文均经过二次审核，尽力确保所有表述、公式、图表正确。如果您发现任何错误，或认为有更好的模型，欢迎提交 issue 或 PR。

## 软件版本

- Python：3.13
- MATLAB：R2025a
- Typst：0.13.1

## 题目文件说明

每个题目文件夹中：

- `附件` 文件夹存放题目所给数据。对于部分较大的 Excel 表，压缩为 parquet 格式。对于其他格式文件，如图片文件、视频文件等，请前往全国大学生数学竞赛或美国大学生数学竞赛官网下载完整附件。
- `数据` 文件夹存放代码生成的图表及数据。为尽可能减小仓库大小，此部分数据不上传，请自行运行代码生成。
- `论文.typ` 文件是论文 PDF 生成源代码文件，使用 Typst 编写，如需编译成 PDF 文件，请自行下载 Typst CLI 工具进行编译。此外，每个 Release 均会上传编译好的论文 PDF 版本。
- `requirements.txt` 文件是当前题目所使用的 Python 第三方包版本。如需运行代码，请按照该文件所列软件包进行环境配置。

## Typst 编译说明

> [!IMPORTANT]
> 论文中使用的字体为思源宋体，若您的电脑中没有安装该字体，会导致编译失败。如未安装，请访问链接：<https://github.com/adobe-fonts/source-han-serif>，按照说明下载对应字体。

首先，前往 [Typst 官网](https://github.com/typst/typst) 下载 Typst。下载完成后，使用如下命令进行编译：

```bash
# Creates `file.pdf` in working directory.
typst compile file.typ

# Creates PDF file at the desired path.
typst compile path/to/source.typ path/to/output.pdf
```

所有命令行帮助可通过以下命令查看：

```bash
# Prints available subcommands and options.
typst help

# Prints detailed usage of a subcommand.
typst help watch
```

## 目录结构

- 2022 数模国赛
  - C 题：古代玻璃制品的成分分析与鉴别

## 许可协议

本项目内所有代码基于[MIT](LICENSE)协议发布，其余材料如论文、数据等，基于[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)协议发布。除代码外，其余资料不可用于商业用途。
