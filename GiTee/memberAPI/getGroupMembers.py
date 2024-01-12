import requests


# 获取组成员列表
def get_group_members(group_name, baseurl, PRIVATE_TOKEN, logger=None):
    url = baseurl + "/groups/" + group_name + "/members?is_all=true"
    headers = {"Private-Token": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        if logger:
            logger.error("获取组成员列表失败，状态码为{}".format(response.status_code))
        else:
            print("获取组成员列表失败，状态码为{}".format(response.status_code))
        return None