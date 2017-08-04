#! /usr/bin/python env
# -*- coding: utf-8 -*-
#
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os.path
import time
import xlwt as ExcelWrite

standard_file = r"xlwt/standard"
spark_file = r"xlwt/spark"
zookeeper_file = r"xlwt/zookeeper"
kafka_file = r"xlwt/kafka"
config_file = "../file"
xls = ExcelWrite.Workbook(encoding="utf-8", style_compression=0)
safe_excel = xls.add_sheet("safe")
alert_excel = xls.add_sheet("alert")
# 设置表头
safe_excel.write(0, 0, "级别")
safe_excel.write(0, 1, "核查结果")
safe_excel.write(0, 2, "配置项")
safe_excel.write(0, 3, "配置值")
safe_excel.write(0, 4, "被核查的配置文件")
alert_excel.write(0, 0, "级别")
alert_excel.write(0, 1, "核查结果")
alert_excel.write(0, 2, "配置项")
alert_excel.write(0, 3, "配置值")
alert_excel.write(0, 4, "被核查的配置文件")
# 设置表宽度
safe_excel.col(1).width = 256 * 100
safe_excel.col(2).width = 256 * 36
safe_excel.col(3).width = 256 * 25
safe_excel.col(4).width = 256 * 20
alert_excel.col(1).width = 256 * 125
alert_excel.col(2).width = 256 * 36
alert_excel.col(3).width = 256 * 25
alert_excel.col(4).width = 256 * 20

s_c = 1  # safe行号
a_c = 1  # alert行号
start = time.time()
component_names = ["hadoop", "hdfs", "yarn", "mapreduce", "hive", "hbase",
                   "spark" + "kafka" + "tez" + "pig" + "sqoop" + "zookeeper" + "flum" + "slider" + "storm"]
configs = []
safe_number = 0
alert_number = 0


# all_number = 0


# 遍历file文件夹下的所有xml文件
def load_config(file):
    for dirpath, dirnames, filenames in os.walk(file):
        for filename in filenames:
            file = dirpath + '/' + filename
            file = file.replace("\\", "/")
            if file.endswith("xml"):
                root = ET.parse(file).getroot()
                properties = root.findall('property')
                for propertys in properties:
                    # global all_number
                    try:
                        d = {}
                        d['file'] = filename
                        d['name'] = propertys.find('name').text
                        d['value'] = propertys.find('value').text
                        if d not in configs:
                            configs.append(d)
                            # all_number = all_number + 1
                    except Exception, e:
                        print Exception, ":", e


# 将安全级别转化为汉语
def tagtochinese(tag):
    if "safe" == tag:
        return "安全"
    elif "warning" == tag:
        return "警告"
    elif "dangerous" == tag:
        return "高危"
    else:
        return "警告"


# 传入配置，进行对比
def comparison_config(line, configs):
    s_name = None
    describe = None
    tag = None
    s_name = line[0]
    s_values = line[1].split(';')
    tmp = "false"
    global alert_number, safe_number
    for config in configs:
        if config['name'] == s_name:
            # print "name相同" + s_name
            tmp = "true"
            tmpp = "only_same_name"
            for v in s_values:
                value = []
                value = v.split(":")
                s_value = value[0].strip().lstrip().rstrip()
                describe = value[1]
                tag = value[2]
                if s_value == config['value']:
                    tmpp = "same_namevalues"
                    tag = tag.strip().lstrip().rstrip()
                    global a_c, s_c
                    if "safe" == tag:
                        safe.write(tag + ":" + config[
                            'file'] + ":\t" + s_name + ":" + s_value + ":" + describe + "\n")
                        safe_number = safe_number + 1
                        s_r = 0
                        safe_excel.write(s_c, s_r, tagtochinese(tag));
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, describe.decode('utf-8'))
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, s_name)
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, s_value)
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, config['file'])
                        s_c = s_c + 1
                    else:
                        alter.write(tag + ":" + config[
                            'file'] + ":\t" + s_name + ":" + s_value + ":" + describe + "\n")
                        alert_number = alert_number + 1
                        a_r = 0
                        alert_excel.write(a_c, a_r, tagtochinese(tag))
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, describe.decode('utf-8'))
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, s_name)
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, s_value)
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, config['file'])
                        a_c = a_c + 1
            if tmpp == "only_same_name":
                v = s_values[0]
                value = v.split(":")
                tag = value[2].strip().lstrip().rstrip()
                if value[0] == "":
                    if tag == "safe":
                        safe.write(
                            tag + ":" + config['file'] + ":\t" + config['name'] + ":" + config['value'] + "\t" + value[
                                1] + "\n")
                        safe_number = safe_number + 1
                        s_r = 0
                        safe_excel.write(s_c, s_r, tagtochinese(tag))
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, value[1].decode('utf-8'))
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, config['name'])
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, config['value'])
                        s_r = s_r + 1
                        safe_excel.write(s_c, s_r, config['file'])
                        s_c = s_c + 1
                    else:
                        alter.write(
                            tag + ":" + config['file'] + ":\t" + config['name'] + ":" + config['value'] + "\t" + value[
                                1] + "\n")
                        alert_number = alert_number + 1
                        a_r = 0
                        alert_excel.write(a_c, a_r, tagtochinese(tag))
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, value[1].decode('utf-8'))
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, config['name'])
                        a_r = a_r + 1
                        alert_excel.write(a_c, a_r, config['value'])
                        a_r = a_r + 1
                        alert_excel.write(a_c, +a_r, config['file'])
                        a_c = a_c + 1
                else:
                    alter.write("警告" + ":" + config['file'] + ":\t" + config['name'] + ":" + config['value'] + "\n")
                    alert_number = alert_number + 1
                    a_r = 0
                    alert_excel.write(a_c, a_r, "警告")
                    a_r = a_r + 1
                    alert_excel.write(a_c, a_r, "没有找到适配项")
                    a_r = a_r + 1
                    alert_excel.write(a_c, a_r, config['name'])
                    a_r = a_r + 1
                    alert_excel.write(a_c, a_r, config['value'])
                    a_r = a_r + 1
                    alert_excel.write(a_c, a_r, config['file'])
                    a_c = a_c + 1
    # 没有找到相关配置项
    if tmp == "false":
        value = s_values[0].split(":")
        # print s_values
        # print value
        s_value = value[0]
        describe = value[1]
        tag = value[2]
        if s_value == "":
            alter.write("warning:" + "没有找到" + s_name + "此配置的含意是" + describe + "\n")
            alert_number = alert_number + 1
            a_r = 0
            alert_excel.write(a_c, a_r, "警告")
            a_r = a_r + 1
            alert_excel.write(a_c, a_r, u"没有找到".encode('utf-8') + s_name + u"此配置的含意是".encode('utf-8') + describe)
            a_r = a_r + 1
            alert_excel.write(a_c, a_r, s_name)
            a_c = a_c + 1
        else:
            alter.write(tag + ":" + "没有找到" + s_name + "相关配置，则为默认值" + s_value + ":" + describe + "\n")
            alert_number = alert_number + 1
            a_r = 0
            alert_excel.write(a_c, a_r, tagtochinese(tag))
            a_r = a_r + 1
            alert_excel.write(a_c, a_r, "没有找到" + s_name + "相关配置，则为默认值" + s_value + ":" + describe)
            a_r = a_r + 1
            alert_excel.write(a_c, a_r, s_name)
            a_c = a_c + 1


safe = open('../output_safe.txt', 'w')
alter = open('../output_alter.txt', 'w')
load_config(config_file)
for line in open(standard_file):
    if line.startswith("#"):
        line = "" + line[1:]
        line = line.strip().lstrip().rstrip()
        if line in component_names:
            alter.write(line + ":" + "\n")
            safe.write(line + ":" + "\n")
            alert_excel.write(a_c, 1, line)
            a_c = a_c + 1
        else:
            continue
    else:
        s_config = line.split('=')
        comparison_config(s_config, configs)

# 生成探测工具的配置文件：
# prop = open('prop.properties', 'w')
# properties = []
# for config in configs:
#     if "fs.defaultFS" == config['name'] and config['name'] not in properties:
#         prop.write("hdfsURI" + "=" + config['value'] + "\n")
#         properties.append("fs.defaultFS")
#     if "yarn.resourcemanager.webapp.address" == config['name'] and config['name'] not in properties:
#         prop.write("yarnRestUrl" + "=" + config['value'] + "\n")
#         properties.append("yarn.resourcemanager.webapp.address")
#     if "zookeeper.znode.parent" == config['name'] and config['name'] not in properties:
#         prop.write("hbaseZnode" + "=" + config['value'] + "\n")
#         properties.append("zookeeper.znode.parent")
#     if "hbase.master.port" == config['name'] and config['name'] not in properties:
#         prop.write("hbaseport" + "=" + config['value'] + "\n")
#         properties.append("hbase.master.port")
#     if "hbase.zookeeper.quorum" == config['name'] and config['name'] not in properties:
#         prop.write("hbaseZKQuorum" + "=" + config['value'] + "\n")
#         properties.append("hbase.zookeeper.quorum")
#     if "hbase.zookeeper.property.clientPort" == config['name'] and config['name'] not in properties:
#         prop.write("zookeeperPort" + "=" + config['value'] + "\n")
#         properties.append("hbase.zookeeper.property.clientPort")
# prop.close()

# spark 配置核查
spark_configs = []
for dirpath, dirnames, filenames in os.walk(config_file):
    for filename in filenames:
        if filename.startswith("spark") and filename.endswith("conf"):
            sparkFile = dirpath + '/' + filename
            sparkFile = sparkFile.replace("\\", "/")
            for line in open(sparkFile):
                if line.startswith("#") or not line.split():
                    continue
                else:
                    line = line.split("=")
                    s = {'file': filename, 'name': line[0].strip(), 'value': line[1].strip()}
                    if s not in spark_configs:
                        spark_configs.append(s)
# choice = raw_input("是否要检查spark组件（请输入y/n)? \n")
# while choice != "y" and choice != "n" :
#     choice = raw_input("是否要检查spark组件（请输入y/n)? \n")
# if "y" == choice:
alert_excel.write(a_c, 1, "spark")
a_c = a_c + 1
for line in open(spark_file):
    if line.startswith("#"):
        line = "" + line[1:]
        line = line.strip().lstrip().rstrip()
        if line in component_names:
            alter.write(line + ":" + "\n")
            safe.write(line + ":" + "\n")
        else:
            continue
    else:
        spark_conf = line.split("=")
        comparison_config(spark_conf, spark_configs)

# .properties 配置文件。其中包含：kafka
properties_configs = []
for dirpath, dirnames, filenames in os.walk(config_file):
    for filename in filenames:
        # if filename.endswith("properties") and "log4j" not in filename:
        if filename == "server.properties" or filename == "producer.properties" or filename == "consumer.properties":
            propertiesFile = dirpath + '/' + filename
            propertiesFile = propertiesFile.replace("\\", "/")
            for line in open(propertiesFile):
                if line.startswith("#") or not line.split():
                    continue
                else:
                    line = line.split("=")
                    s = {'file': filename, 'name': line[0].strip(), 'value': line[1].strip()}
                    if s not in properties_configs:
                        properties_configs.append(s)
print properties_configs
alert_excel.write(a_c, 1, "kafka")
a_c = a_c + 1
for line in open(kafka_file):
    if line.startswith("#"):
        line = "" + line[1:]
        line = line.strip().lstrip().rstrip()
        if line in component_names:
            alter.write(line + ":" + "\n")
            safe.write(line + ":" + "\n")
        else:
            continue
    else:
        kafka_conf = line.split("=")
        comparison_config(kafka_conf, properties_configs)

# zookeeper配置核查
# zookeeper_configs = []
# for dirpath, dirnames, filenames in os.walk(config_file):
#     for filename in filenames:
#         if filename.startswith("zoo") and filename.endswith("cfg"):
#             sparkfile = dirpath + '/' + filename
#             sparkfile = sparkfile.replace("\\", "/")
#             for line in open(sparkfile):
#                 if line.startswith("#") or not line.split():
#                     continue
#                 else:
#                     line = line.split("=")
#                     z = {'file': filename, 'name': line[0], 'value': line[1].strip().lstrip().rstrip()}
#                     zookeeper_configs.append(z)
# alert_excel.write(a_c, 1, "zookeeper")
# a_c = a_c + 1
# for line in open(zookeeper_file):
#     if line.startswith("#"):
#         line = "" + line[1:]
#         line = line.strip().lstrip().rstrip()
#         if line in component_names:
#             alter.write(line + ":" + "\n")
#             safe.write(line + ":" + "\n")
#         else:
#             continue
#     else:
#         zookeeper_conf = line.split('=')
#         comparison_config(zookeeper_conf, zookeeper_configs)


end = time.time()
t = end - start
# safe.write("安全配置个数为：" + str(safe_number) + "\n")
safe.write("耗时" + str(t) + "秒" + "\n")
# alter.write("alert配置个数为：" + str(alert_number) + "\n")
alter.write("耗时" + str(t) + "秒" + "\n")
alter.close()
safe.close()
xls.save("../result" + str(time.time()) + ".xls")
