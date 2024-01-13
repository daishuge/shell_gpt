# shell_gpt

在 Linux 中用自然语言执行命令！

# 效果展示

![image](https://github.com/daishuge/shell_gpt/assets/122254868/41268e7d-732c-4697-93b1-28f944ebb9ee)

# 使用方法

## 1:安装所需库

```shell
pip install openai
```

## 2：加入环境变量

- 首先，需要知道gpt的完整路径。假设位于 /home/daishuge 目录下，那么它的完整路径就是 /home/daishuge/gpt。
- 编辑 .bashrc 或 .profile 文件, 加入 `export PATH="$PATH:<脚本所在目录>"`
- 应用更改 `source ~/.bashrc`

## 3:赋予执行权限

```shell
chmod +X /path/to/gpt
```

## 4:更改文件中的api_key为你自己的openai api key

如果你使用免费版本，那么请把模型改为 `gpt-3.5-turbo`

## 5:开始享受！

```shell
gpt write a hello world py cpp and run it
```

# 正在开发终端记录给gpt的功能···
