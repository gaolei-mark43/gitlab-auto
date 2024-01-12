# -*- coding: utf-8 -*-
# 部署linux服务器上要放开注释，路径为部署路径
# import sys
# sys.path.append('/root/GiTee/fastapi/GitProject')
import GiTee.config.API
import GiTee.groupAPI.getGroupID as getGroupID
import GiTee.groupAPI.createFatherGroup as FG
import GiTee.groupAPI.createSonGroup as SG
import GiTee.config.departs as departs
import logging
from GiTee.memberAPI import getMemberID
from GiTee.memberAPI.addMembersToFatherGroup import add_member_to_group
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from GiTee.memberAPI.getGroupMembers import get_group_members

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s -line: %(lineno)d- %(message)s')


# 定义组信息
class GroupInfo(BaseModel):
    BGBU: str
    group_name: str
    description: str
    isCreateSub: str
    subgroup_name0: str
    subgroup_name1: str
    subgroup_name2: str
    subgroup_name3: str
    subgroup_name4: str
    subgroup_desc0: str
    subgroup_desc1: str
    subgroup_desc2: str
    subgroup_desc3: str
    subgroup_desc4: str
    members: str


@app.post("/create_group")
async def create_group(group_info: GroupInfo):
    BGBU = getBgBu(group_info.BGBU)
    group_name = group_info.group_name
    description = group_info.description
    isCreateSub = group_info.isCreateSub
    subgroup_name0 = group_info.subgroup_name0
    subgroup_name1 = group_info.subgroup_name1
    subgroup_name2 = group_info.subgroup_name2
    subgroup_name3 = group_info.subgroup_name3
    subgroup_name4 = group_info.subgroup_name4
    subgroup_desc0 = group_info.subgroup_desc0
    subgroup_desc1 = group_info.subgroup_desc1
    subgroup_desc2 = group_info.subgroup_desc2
    subgroup_desc3 = group_info.subgroup_desc3
    subgroup_desc4 = group_info.subgroup_desc4
    members = group_info.members

    # 拼接子组名称和描述为一个字典
    subgroup_dict = {}
    for i in range(0, 5):
        subgroup_name = locals()["subgroup_name{}".format(i)]
        subgroup_desc = locals()["subgroup_desc{}".format(i)]
        if subgroup_name != '':
            subgroup_dict[subgroup_name] = subgroup_desc

    # 判断父组是否已创建，未创建则创建父组再创建子组，已创建则不创建，直接创建子组
    if checkGroupIsCreate(group_name):
        logging.info("父组{}已创建，不需创建".format(group_name))
        father_group_id = get_group_id(group_name, *get_config(), logger=logging)
        create_subgroups(subgroup_dict, father_group_id, isCreateSub)
    else:
        logging.info("父组{}未创建，开始创建".format(group_name))
        group_name = checkFirstGroupName(group_name, BGBU)
        create_father_group(group_name, *get_config(), description=description, logger=logging)
        father_group_id = get_group_id(group_name, *get_config(), logger=logging)
        create_subgroups(subgroup_dict, father_group_id, isCreateSub)

    # 调试-成员添加父组为管理角色
    members = members.split(",")
    for member in members:
        if member != '':
            logging.info("开始添加成员{}到父组{}为管理角色".format(member, group_name))
            # 获取成员ID
            member_ID = getMemberID.get_member_id(member, *get_config(), logger=logging)
            logging.info("成员{}的ID为{}".format(member, member_ID))
            # 添加成员到组
            add_member_to_group(member_ID, father_group_id, *get_config(), logger=logging)
        else:
            logging.info("成员名称为空，不需添加")

    # 判断远程调用结果，通过判断父组是否已创建、子组是否已创建、成员是否已添加到组
    result, fail_list = check_remote_call_result(group_name, subgroup_dict.keys(), members)
    if result:
        logging.info("远程调用成功")
        return {"code": 200, "msg": "远程调用成功"}
    else:
        logging.info("远程调用失败")
        return {"code": 500, "msg": "远程调用失败", "fail_list": fail_list}


# 判断远程调用结果，通过判断父组是否已创建、子组是否已创建、成员是否已添加到组
def check_remote_call_result(father_group_name, subgroup_names, member_names):
    baseurl, PRIVATE_TOKEN = get_config()
    fail_list = []
    father_group_id = get_group_id(father_group_name, baseurl, PRIVATE_TOKEN, logger=logging)
    # 检查父组是否已创建
    if father_group_id is None:
        logging.error("父组{}未创建".format(father_group_name))
        fail_list.append(father_group_name+"未创建")
        return False, fail_list
    # 检查子组是否已创建
    for subgroup_name in subgroup_names:
        subgroup_id = get_group_id(subgroup_name, baseurl, PRIVATE_TOKEN, logger=logging)
        if subgroup_id is None:
            logging.error("子组{}未创建".format(subgroup_name))
            fail_list.append(subgroup_name+"未创建")
            return False, fail_list
    # 检查成员是否已添加到组
    for member_name in member_names:
        response = get_group_members(father_group_name, baseurl, PRIVATE_TOKEN, logger=logging)
        if member_name not in str(response):
            logging.error(f"成员 {member_name} 未添加到组 {father_group_name}")
            fail_list.append(f"成员 {member_name} 未添加到组 {father_group_name}")
            return False, fail_list
    return True, fail_list


# 获取Git接口配置
def get_config():
    baseurl, PRIVATE_TOKEN = GiTee.config.API.get_config()
    return baseurl, PRIVATE_TOKEN


# 获取组ID
def get_group_id(group_name, baseurl, PRIVATE_TOKEN, logger=None):
    group_ID = getGroupID.get_group_id(group_name, baseurl, PRIVATE_TOKEN, logger=logger)
    return group_ID


# 创建父组
def create_father_group(group_name, baseurl, PRIVATE_TOKEN, description=None, logger=None):
    group_ID = FG.create_father_group(group_name, baseurl, PRIVATE_TOKEN, description=description, logger=logger)
    return group_ID


# 创建子组
def create_son_group(son_group_name, baseurl, PRIVATE_TOKEN, father_group_id, description=None, logger=None):
    group_ID = SG.create_son_group(son_group_name, baseurl, PRIVATE_TOKEN, father_group_id, description=description,
                                   logger=logger)
    return group_ID


# 校验组是否已创建
def checkGroupIsCreate(group_name):
    logging.info("校验组是否已创建")
    baseurl, PRIVATE_TOKEN = get_config()
    group_ID = get_group_id(group_name, baseurl, PRIVATE_TOKEN, logger=logging)
    if group_ID is None:
        logging.info("{}组不存在，需要创建组".format(group_name))
        return False
    else:
        logging.info("{}组已存在，不需创建组".format(group_name))
        return True


# 获取组织名称
def getBgBu(bgbu):
    BgBuName = ""
    if bgbu in departs.departs:
        BgBuName = departs.departs[bgbu]
    return BgBuName


# 校验父组名称合法性
def checkFirstGroupName(frist_Name, BGBU):
    if checkGroupIsCreate(frist_Name):
        return frist_Name
    else:
        logging.info("父组{}未创建".format(frist_Name))
        logging.info("开始校验父组名称合法性")
        # 判断是否需要添加前缀
        if any(frist_Name.startswith(value) for value in departs.departs.values()):
            logging.info("父组名称合法")
            frist_Name = frist_Name
        else:
            logging.info("父组名称不合法，开始添加前缀")
            frist_Name = BGBU + "_" + frist_Name
        logging.info("父组名称添加前缀后为:{}".format(frist_Name))
        return frist_Name


# 批量创建子组
def create_subgroups(subgroup_dict, father_group_id, isCreateSub):
    if isCreateSub == '是':
        logging.info("开始创建子组")
        for i in subgroup_dict:
            if i != '':
                subgroup_desc = subgroup_dict[i]
                logging.info("开始创建子组{}".format(i))
                create_son_group(i, *get_config(), father_group_id, subgroup_desc, logger=logging)
            else:
                logging.info("{}子组名称为空，不需创建".format(i))
    else:
        logging.info("不需创建子组")


if __name__ == '__main__':
    # 部署机器为 172.30.94.147
    uvicorn.run(app=app, host="127.0.0.1", port=7070)







