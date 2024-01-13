#!/usr/bin/env python3
import openai
import sys
import subprocess

client = openai.OpenAI(api_key="sk-xxx")

role='''
你是一个终端助手，你放在shell markdown块中的内容将在arm64 raspbian系统的沙盒环境中中运行，所以不用担心安全问题。
用户在这个系统中使用你，所以默认为linux指令
如果想运行多条指令，用&&分割，如：
```shell
sudo apt update && sudo apt upgrade -y
```
这样，将会在用户当前目录下，运行apt update和apt upgrade两条指令。
如果你想要了解信息，可以使用各种获得信息的指令，在终端上的输出将被你看到
你的一个回答中只能带有一个代码块，但能有多条指令
你的指令必须是明确的，如果你有不了解的信息，可以先了解，或者使用echo指令询问用户
你无需说明你的命令
'''

def get_last_300_lines(file_path):
    try:
        output = subprocess.check_output(['tail', '-n', '300', file_path])
        return output.decode()
    except Exception as e:
        print(f"读取文件时出现错误: {e}")
        return ""
log_file_path = '/home/daishuge/log.txt'
last_300_lines = get_last_300_lines(log_file_path)

def gpt(query, md="gpt-4-1106-previe", rol=role, if_print=True):

    messages = [
        {"role": "system", "content": rol},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        # model='gpt-4-1106-preview',
        # model="gpt-3.5-turbo",
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=1,
        max_tokens=1000,
        stream=True
    )

    result = ""

    for part in response:
        content = part.choices[0].delta.content if part.choices[0].delta and part.choices[0].delta.content else ""
        result += content
        if if_print:
            print(content, end='', flush=True)

    return result

# 处理命令行输入
if len(sys.argv) > 1:
    input_query = ' '.join(sys.argv[1:])
    # 将终端历史内容添加到查询中
    input_query = last_300_lines + "\n" + input_query
else:
    print("请输入一个查询")
    sys.exit(1)

# 调用gpt函数
gpt_response = gpt(input_query)

# 提取和执行命令
commands = gpt_response.split("```")
if len(commands) >= 3:
    shell_command = commands[1].strip()
    if shell_command.startswith("shell"):
        shell_command = shell_command[5:].strip()  # 去除 "shell" 标识符

    try:
        subprocess.run(shell_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误: {e}")
else:
    print("未能解析出有效的shell代码块")

print("\n\n")
