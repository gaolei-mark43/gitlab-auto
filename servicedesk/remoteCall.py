import requests
import json
import logging


def create_group():
    url = "http://172.30.94.147:7070/create_group"
    payload = json.dumps({
        "BGBU": BGBU,
        "group_name": group_name,
        "description": description,
        "isCreateSub": isCreateSub,
        "subgroup_name0": subgroup_name0,
        "subgroup_name1": subgroup_name1,
        "subgroup_name2": subgroup_name2,
        "subgroup_name3": subgroup_name3,
        "subgroup_name4": subgroup_name4,
        "subgroup_desc0": subgroup_desc0,
        "subgroup_desc1": subgroup_desc1,
        "subgroup_desc2": subgroup_desc2,
        "subgroup_desc3": subgroup_desc3,
        "subgroup_desc4": subgroup_desc4,
        "members": members
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    BGBU = '${BGBU}'
    group_name = '${parentGroupName}'
    description = '${groupdesc}'
    members = '${groupmaintainer}'
    subgroup_name0 = '${sonGroupName}'
    isCreateSub = '${isCreateSub}'
    subgroup_name1 = '${sonGroupName1}'
    subgroup_name2 = '${sonGroupName2}'
    subgroup_name3 = '${sonGroupName3}'
    subgroup_name4 = '${sonGroupName4}'
    subgroup_desc0 = '${subgroup_desc}'
    subgroup_desc1 = '${subgroup_desc1}'
    subgroup_desc2 = '${subgroup_desc2}'
    subgroup_desc3 = '${subgroup_desc3}'
    subgroup_desc4 = '${subgroup_desc4}'

    result = create_group()
    result_json = json.loads(result)
    code = result_json['code']
    message = result_json['message']
    if code == 200:
        logging.info("创建组成功，组名称为：{}，组描述为：{}".format(group_name, description))
    elif code == 500:
        logging.info("创建组失败，失败原因：{}".format(result_json))




