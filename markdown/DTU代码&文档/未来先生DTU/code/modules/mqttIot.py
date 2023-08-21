# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :mqttIot.py
@author    :elian.wang@quectel.com
@brief     :universal mqtt iot inferface
@version   :0.1
@date      :2022-05-18 13:28:53
@copyright :Copyright (c) 2022
"""
import uos
import ujson
import utime
import _thread
import fota
import request
import ql_fs
from checksum import file_crc32
from misc import Power
from umqtt import MQTTClient
from usr.modules.logging import getLogger
from usr.modules.common import CloudObservable
from usr.modules.crc16 import gen_crc16
from usr.modules.ymodem_sender import send_file

log = getLogger(__name__)


class MqttIot(CloudObservable):
    """This is a class for universal mqtt iot.

    This class extend CloudObservable.

    This class has the following functions:
        1. Cloud connect and disconnect
        2. Publish data to cloud
        3. Subscribe data from cloud

    Attribute:
        pub_topic_dict: topic dict for publish dtu through data
        sub_topic_dict: topic dict for subscribe cloud through data
        conn_type:cloud name

    Run step:
        1. cloud = MqttIot(server, qos, port, clean_session, client_id, pub_topic, sub_topic)
        2. cloud.addObserver(RemoteSubscribe)
        3. cloud.init()
        4. cloud.post_data(data)
        5. cloud.close()
    """
    # mqtt ota升级主题
    UPDATE_PLAN_TOPIC_PREFIX = "/ota/device/upgrade/"
    UPDATE_STATUS_TOPIC_PREFIX = "/ota/upgrade/status/"

    MCU_UPGRADE_FILE_PATH = "/usr/mcu_upgrade_file.bin"
    MCU_UPGRADE_URL_PATH = "/usr/mcu_upgrade_url.txt"

    def __init__(self, server, qos, port, clean_session,
                 client_id, user, pass_word, pub_topic=None, sub_topic=None, life_time=120,
                 device_fw_name='', device_fw_version='', ymodem=False):
        """
        1. Init parent class CloudObservable
        2. Init cloud connect params and topic
        """
        super().__init__()
        self.conn_type = "mqtt"
        self.__pk = None
        self.__ps = None
        self.__dk = user
        self.__ds = None
        self.__server = server
        self.__qos = qos
        self.__port = port
        self.__mqtt = None
        self.__clean_session = clean_session
        self.__life_time = life_time
        self.__client_id = client_id
        self.__password = pass_word
        self.device_fw_name = device_fw_name
        self.device_fw_version = device_fw_version
        self.ymodem = ymodem
        self.__ota_info = {}
        self.__serial = None
        self.__up_transaction = None
        self.UPDATE_PLAN_TOPIC = self.UPDATE_PLAN_TOPIC_PREFIX + self.__client_id
        self.UPDATE_STATUS_TOPIC = self.UPDATE_STATUS_TOPIC_PREFIX + self.__client_id

        if pub_topic == None:
            self.pub_topic_dict = {"0": "/python/mqtt/pub"}
        else:
            self.pub_topic_dict = pub_topic
        if sub_topic == None:
            self.sub_topic_dict = {"0": "/python/mqtt/sub"}
        else:
            self.sub_topic_dict = sub_topic

    def __subscribe_topic(self):
        # 订阅ota升级主题
        if self.__mqtt.subscribe(self.UPDATE_PLAN_TOPIC, qos=0) == -1:
            log.error("Topic [%s] Subscribe Failed." % self.UPDATE_PLAN_TOPIC)
        else:
            log.info("Topic [%s] Subscribe Successfully." % self.UPDATE_PLAN_TOPIC)

        # 订阅用户主题
        for topic_id, usr_sub_topic in self.sub_topic_dict.items():
            if self.__mqtt.subscribe(usr_sub_topic, qos=0) == -1:
                log.error("Topic [%s] Subscribe Failed." % usr_sub_topic)
            else:
                log.info("Topic [%s] Subscribe Successfully." % usr_sub_topic)

    def __sub_cb(self, topic, data):
        """mqtt subscribe topic callback

        Parameter:
            topic: topic info
            data: response dictionary info
        """
        topic = topic.decode()
        try:
            data = ujson.loads(data)
        except Exception:
            pass

        try:
            if topic == self.UPDATE_PLAN_TOPIC:
                log.info('ota update plan call back')
                # TODO: 取消订阅
                # TODO: 进入升级流程
                self.__ota_info = data
                self.notifyObservers(self, *("ota_plain", {"topic": topic, "data": data}))
            else:
                self.notifyObservers(self, *("raw_data", {"topic": topic, "data": data}))
        except Exception as e:
            log.error("{}".format(e))

    def __listen(self):
        while True:
            self.__mqtt.wait_msg()
            utime.sleep_ms(100)

    def __start_listen(self):
        """Start a new thread to listen to the cloud publish 
        """
        _thread.start_new_thread(self.__listen, ())

    def init(self, enforce=False):
        """mqtt connect and subscribe topic

        Parameter:
            enforce:
                True: enfore cloud connect and subscribe topic
                False: check connect status, return True if cloud connected

        Return:
            Ture: Success
            False: Failed
        """
        log.debug("[init start] enforce: %s" % enforce)
        if enforce is False and self.__mqtt is not None:
            log.debug("self.get_status(): %s" % self.get_status())
            if self.get_status():
                return True

        if self.__mqtt is not None:
            self.close()

        log.debug("mqtt init. self.__client_id: %s, self.__password: %s, self.__dk: %s, self.__ds: %s" % (
        self.__client_id, self.__password, self.__dk, self.__ds))
        self.__mqtt = MQTTClient(client_id=self.__client_id, server=self.__server, port=self.__port,
                                 user=self.__dk, password=self.__password, keepalive=self.__life_time, ssl=False)
        try:
            self.__mqtt.connect(clean_session=self.__clean_session)
        except Exception as e:
            log.error("mqtt connect error: %s" % e)
        else:
            self.__mqtt.set_callback(self.__sub_cb)
            self.__subscribe_topic()
            self.__start_listen()
            log.debug("mqtt start.")

        log.debug("self.get_status(): %s" % self.get_status())
        if self.get_status():
            return True
        else:
            return False

    def close(self):
        self.__mqtt.disconnect()

    def get_status(self):
        """Get mqtt connect status

        Return:
            True -- connect success
            False -- connect falied
        """
        try:
            return True if self.__mqtt.get_mqttsta() == 0 else False
        except:
            return False

    def through_post_data(self, data, topic_id):
        try:
            self.__mqtt.publish(self.pub_topic_dict[topic_id], data, self.__qos)
        except Exception:
            log.error("mqtt publish topic %s failed. data: %s" % (self.pub_topic_dict[topic_id], data))
            return False
        else:
            return True

    def post_data(self, data):
        pass

    def ota_request(self):
        pass

    def ota_action(self, action, module=None):
        log.info('start ota upgrade!')
        log.info('self.__ota_info: ', self.__ota_info)
        # {'file_checksum': '56', 'type': 'mcu', 'url': 'https://www.baidu.com', 'new_ver': 'version2.0'}

        type_ = self.__ota_info.get('type')
        if type_ == 'lte':
            # TODO: 模组固件升级
            _thread.start_new_thread(self.__lte_ota_upgrade, ())
        elif type_ == 'mcu':
            # TODO: 设备固件升级
            _thread.start_new_thread(self.__mcu_ota_upgrade, ())

    def __lte_ota_upgrade(self):
        log.info('start lte ota upgrade!')
        data = {
            "type": 'lte',
            "current_ver": self.device_fw_version,
            "status": {
                "code": 10000,
                "desc": "firmware downloading"
            }
        }
        self.__mqtt.publish(self.UPDATE_STATUS_TOPIC, ujson.dumps(data), self.__qos)

        fota_obj = fota(reset_disable=1)
        rv = fota_obj.httpDownload(url1=self.__ota_info.get('url'), callback=self.__fw_download_cb)
        if rv == 0:
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'lte',
                    "current_ver": self.device_fw_version,
                    "status": {
                        "code": 12000,
                        "desc": "firmware downloading success"
                    }
                }),
                self.__qos
            )
            Power.powerRestart()
        else:
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'lte',
                    "current_ver": self.device_fw_version,
                    "status": {
                        "code": 11000,
                        "desc": "firmware downloading error"
                    }
                }),
                self.__qos
            )

    def __fw_download_cb(self, args):
        pass

    def add_up_transaction(self, up_transaction):
        self.__up_transaction = up_transaction

    @property
    def up_transaction(self):
        return self.__up_transaction

    def add_serial(self, serial):
        self.__serial = serial

    @property
    def serial(self):
        if self.__serial is None:
            raise TypeError('pls add serial for Mqtt object.')
        return self.__serial

    def __download_mcu_upgrade_file(self, url):

        # 判断升级url是否一致
        try:
            with open(self.MCU_UPGRADE_URL_PATH, 'r') as f:
                if f.read() == url and ql_fs.path_exists(self.MCU_UPGRADE_FILE_PATH):
                    log.info('upgrade url is same, we do not download. use the fw file already existed.')
                    # 固件下载成功状态上报
                    log.info('download file successfully! continue...')
                    self.__mqtt.publish(
                        self.UPDATE_STATUS_TOPIC,
                        ujson.dumps({
                            "type": 'mcu',
                            # "current_ver": self.device_fw_version,
                            "status": {
                                "code": 12000,
                                "desc": "firmware downloading success"
                            }
                        }),
                        self.__qos
                    )
                    return True
        except Exception:
            pass

        log.info('start to download fw file.')
        try:
            # {'file_checksum': '56', 'type': 'lte', 'url': 'https://www.baidu.com', 'new_ver': 'version2.0'}
            response = request.get(url, decode=False)
        except Exception as e:
            # 固件下载失败
            log.error("http download err: {}".format(str(e)))
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 11000,
                        "desc": "firmware downloading error"
                    }
                }),
                self.__qos
            )
            return False
        else:
            log.info('http download get content bytes length: {}'.format(int(response.headers['Content-Length'])))
            # 固件下载成功
            log.info('download file successfully! continue...')
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 12000,
                        "desc": "firmware downloading success"
                    }
                }),
                self.__qos
            )

        # TODO: write fw file to file system
        with open(self.MCU_UPGRADE_FILE_PATH, 'wb') as f:
            for content in response.content:
                f.write(content)
        log.info('save upgrade data into file \"{}\"'.format(self.MCU_UPGRADE_FILE_PATH))

        # TODO: save url
        with open(self.MCU_UPGRADE_URL_PATH, 'w') as f:
            f.write(url)
        log.info('save url data into file \"{}\"'.format(self.MCU_UPGRADE_URL_PATH))

        return True

    def __mcu_ota_upgrade(self):
        log.info('start mcu ota upgrade!')

        # 透传数据线程退出
        self.__up_transaction.stop_uplink_main()
        log.info('stop uplink main thread.')
        utime.sleep_ms(100)  # 等待透传线程退出

        self.__mcu_ota_upgrade_process()

        # 新建透传数据线程
        log.info('restart uplink main thread.')
        self.__up_transaction.start_uplink_main()

    def __mcu_ota_upgrade_process(self):
        # 固件下载中
        self.__mqtt.publish(
            self.UPDATE_STATUS_TOPIC,
            ujson.dumps({
                "type": 'mcu',
                # "current_ver": self.device_fw_version,
                "status": {
                    "code": 10000,
                    "desc": "firmware downloading"
                }
            }),
            self.__qos
        )

        url = self.__ota_info.get('url')
        if not self.__download_mcu_upgrade_file(url):
            log.info('mcu fw upgrade progress exited...')
            return

        if not self.__check_file_crc32(
            self.MCU_UPGRADE_FILE_PATH,
            self.__ota_info.get('file_checksum')
        ):
            log.info('file crc32 check failed.')
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 11000,
                        "desc": "firmware downloading error"
                    }
                }),
                self.__qos
            )
            log.info('remove upgrade bin and url file.')
            # 文件校验失败，删除
            uos.remove(self.MCU_UPGRADE_FILE_PATH)
            uos.remove(self.MCU_UPGRADE_URL_PATH)
            log.info('mcu fw upgrade progress exited...')
            return

        # mcu固件传输协商
        if not self.__check_mcu_transaction_status():
            log.info('mcu transaction check failed...')

            log.info('fw file transfer failed!')
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 21000,
                        "desc": "firmware transferring error"
                    }
                }),
                self.__qos
            )
            return

        # 固件传输中
        log.info('start transfer fw files to mcu...')
        self.__mqtt.publish(
            self.UPDATE_STATUS_TOPIC,
            ujson.dumps({
                "type": 'mcu',
                # "current_ver": self.device_fw_version,
                "status": {
                    "code": 20000,
                    "desc": "firmware transferring"
                }
            }),
            self.__qos
        )

        if self.ymodem:
            # Ymodem协议传输固件
            is_ok = send_file(self.serial, [(self.MCU_UPGRADE_FILE_PATH, self.MCU_UPGRADE_FILE_PATH.split('/')[-1])])
        else:
            # 自定义协议传输固件
            is_ok = self.__transfer_mcu_upgrade_fw()

        # 固件传输成功或失败
        if is_ok:
            log.info('fw file transfer successfully!')
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 22000,
                        "desc": "firmware transferring success"
                    }
                }),
                self.__qos
            )
        else:
            log.info('fw file transfer failed!')
            self.__mqtt.publish(
                self.UPDATE_STATUS_TOPIC,
                ujson.dumps({
                    "type": 'mcu',
                    # "current_ver": self.device_fw_version,
                    "status": {
                        "code": 21000,
                        "desc": "firmware transferring error"
                    }
                }),
                self.__qos
            )

    def __check_mcu_transaction_status(self):
        for i in range(10):
            self.serial.write(b'+++++')
            response = self.serial.read(5, timeout=200, decode=False)
            log.info('get check response: {}'.format(response))
            if response == b'+++++':
                log.info('check mcu transaction status successfully.')
                return True
        return False

    def __check_file_crc32(self, path, checksum):
        file_crc32_value = file_crc32.calc(path)
        log.debug('file crc32 value: {}; checksum: {}'.format(file_crc32_value, checksum))
        return file_crc32_value == checksum

    def __send_packet_data(self, msg, timeout=20000):

        for i in range(1, 4):  # try 3 times at most, interval is 20s
            log.info('send fw data, try {} times(s), len: {}, packet_id: {}'.format(i, len(msg.args), msg.packet_id))
            self.serial.write(msg.dump())

            # >>> 读串口应答数据，并解析
            res_bytes = self.serial.read(8, timeout, decode=False)
            if not res_bytes:
                log.info('read no content from serial for packet id: {}'.format(msg.packet_id))
                continue

            try:
                res_packet_type = res_bytes[0]
                res_packet_id = int.from_bytes(res_bytes[1:5], 'little')
                res_cmd_type = res_bytes[5]
                res_length = int.from_bytes(res_bytes[6:8], 'little')

                # read enough bytes according to length
                res_bytes += self.serial.read(res_length + 2, decode=False)
                res_args = res_bytes[8:-2]
                res_crc16 = int.from_bytes(res_bytes[-2:], 'little')

            except Exception as e:
                log.info('parse error: {}, packet id: {} res_bytes: {}'.format(str(e), msg.packet_id, res_bytes))
                continue

            if res_packet_type == 1 \
                    and Message.crc16_check(res_bytes[:-2], res_crc16) \
                    and res_packet_id == msg.packet_id \
                    and res_cmd_type == msg.cmd_type:
                log.info('ack for packet id: {}'.format(msg.packet_id))
                return True
            else:
                log.info('format err, res_packet_type: {}, res_packet_id: {}, '
                         'packet_type: {}'.format(res_packet_type, res_packet_id, res_packet_type))
            # <<<

        return False

    def __transfer_mcu_upgrade_fw(self):
        # TODO: read fw file from file system
        is_ok = True
        with open(self.MCU_UPGRADE_FILE_PATH, 'rb') as f:

            packet_id = 0
            while True:
                content = f.read(1024)
                if not content:
                    log.info('read all content from mcu_upgrade_temp_file.bin')
                    break

                msg = Message(0, packet_id, 0x01, content)
                if not self.__send_packet_data(msg):
                    log.error('send packet data error after 3 try times for packet id: {}'.format(packet_id))
                    is_ok = False
                    break

                packet_id += 1

        msg = Message(0, packet_id, 0x02, b'\x00' if is_ok else b'\xff')
        return self.__send_packet_data(msg)

    def device_report(self):
        data = {
            "type": 'lte',
            "current_ver": self.device_fw_version
        }

        try:
            self.__mqtt.publish(self.UPDATE_STATUS_TOPIC, ujson.dumps(data), self.__qos)
        except Exception:
            log.error("mqtt publish topic %s failed. data: %s" % (self.UPDATE_STATUS_TOPIC, data))
            return False
        else:
            return True


class Message(object):

    def __init__(self, packet_type, packet_id, cmd_type, args):
        self.packet_type = packet_type
        self.packet_id = packet_id
        self.cmd_type = cmd_type
        self.args = args
        self.length = len(self.args)
        self.crc16 = None

        self.__dump_data = b''

    def __str__(self):
        return "packet_type: {}\n" \
               "packet_id: {}\n" \
               "cmd_type: {}\n" \
               "args: {}\n" \
               "length: {}\n" \
               "crc16: {}".format(self.packet_type, self.packet_id, self.cmd_type, self.args, self.length, self.crc16)

    @classmethod
    def crc16_check(cls, data, checksum):
        return gen_crc16(data) == int(checksum)

    @classmethod
    def gen_crc16(cls, bytes_data):
        return gen_crc16(bytes_data)

    def dump(self):
        data = bytearray()
        data.append(self.packet_type)
        data.extend(self.packet_id.to_bytes(4, 'little'))
        data.append(self.cmd_type)
        data.extend(self.length.to_bytes(2, 'little'))
        if self.length != 0:
            data.extend(self.args)
        self.crc16 = self.gen_crc16(data)
        data.extend(self.crc16.to_bytes(2, 'little'))
        return data
