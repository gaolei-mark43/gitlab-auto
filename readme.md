# GitLab API 工具项目介绍

该项目是一个使用 Python 编写的 GitLab API 工具，旨在帮助管理 GitLab 上的组和成员。以下是项目主要功能：

## 1. 创建组

通过 `create_group` 函数，可以创建一个新的组。需要提供组的名称、描述、是否需要创建子组以及子组的相关信息。

## 2. 添加成员到组

通过 `add_member_to_group` 函数，可以将指定的成员添加到指定的组中。需要提供成员的ID和组的ID。

## 3. 获取组ID

通过 `get_group_id` 函数，可以获取指定组的ID。需要提供组的名称。

## 4. 创建父组和子组

通过 `create_father_group` 和 `create_son_group` 函数，可以创建父组和子组。需要提供组的名称、描述以及父组的ID（如果是创建子组）。

## 5. 检查组是否已创建

通过 `checkGroupIsCreate` 函数，可以检查指定的组是否已经创建。需要提供组的名称。

此外，项目还包含一个启动脚本 `start.sh`，用于在 Linux 服务器上启动项目。

项目使用了 FastAPI 框架，这是一个现代、快速（高性能）的 web 框架，基于 Python 3.6+ 类型提示。

## 项目文件

- `main.py`：项目的主要入口，包含了所有的 API 定义和业务逻辑。
- `getGroupID.py`：包含了获取组ID的函数。
- `addMembersToFatherGroup.py`：包含了添加成员到组的函数。
- `start.sh`：项目的启动脚本，用于在 Linux 服务器上启动项目。

## 运行环境

项目的运行环境是 Python，需要在机器上安装 Python 环境才能运行该项目。
