import serial
import serial.tools.list_ports as seriallp
import time
import binascii
import keyboard

class Hreader:
    # 初始化类属性
    def __init__(self, com, *port_ante):
        self.ser = serial.Serial()
        self.OK = b'\x00\x00'
        self.Moduletech = b'\x4D\x6F\x64\x75\x6C\x65\x74\x65\x63\x68'
        self.com = com
        self.port_ante = port_ante
        self.data = dict()

    # 计算CRC-16码
    @classmethod
    def CRC_calcCrc8(cls, crcReg, poly, u8Data):
        for i in range(8):
            xorFlag = crcReg & 0x8000
            crcReg <<= 1
            bit = (u8Data & 0x80) == 0x80
            crcReg |= bit
            if xorFlag:
                crcReg ^= poly
            u8Data <<= 1
        return crcReg & 0xFFFF  # 确保CRC值不超过16位

    def __CalcCRC(self, msg):
        MSG_CRC_INIT = 0xFFFF
        MSG_CCITT_CRC_POLY = 0x1021
        calcCrc = MSG_CRC_INIT
        for i in range(1, len(msg)):
            calcCrc = self.CRC_calcCrc8(calcCrc, MSG_CCITT_CRC_POLY, msg[i])
        return calcCrc

    # 打开串口
    def __port_open(self):
        self.ser.port = self.com
        self.ser.baudrate = 115200
        self.ser.open()
        if self.ser.isOpen():
            print("串口打开成功！")
        else:
            print("串口打开失败！")

    # 关闭串口
    def __port_close(self):
        self.ser.close()
        if self.ser.isOpen():
            print("串口关闭失败！")
        else:
            print("串口关闭成功！")

    # 发送命令
    def __send_command(self, command):
        msg = bytes.fromhex(command)
        crc_value = self.__CalcCRC(msg)
        crc16 = crc_value.to_bytes(length=2, byteorder='big')
        command_code = msg + crc16
        self.ser.write(command_code)
        time.sleep(0.5)

    # 启动bootloader层
    def __Bootloader(self):
        self.__send_command('ff 00 09')
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        if boot_status != self.OK:
            print("返回boot失败")
        else:
            print("返回boot成功")

    # 启动firmware层
    def __Firmware(self):
        self.__send_command('ff 00 04')
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        if boot_status != self.OK:
            print("返回firmware失败")
        else:
            print("返回firmware成功")

    # 设置当前操作使用的标签协议为GEN2
    def __SetGEN2(self):
        self.__send_command('ff 02 93 0005')
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        if boot_status != self.OK:
            print("设置GEN2失败")
        else:
            print("设置GEN2成功")

    # 设置天线端口
    # 设置单端口作为标签访问天线
    def __Setantennaport_0(self):
        port_ante = self.port_ante[0]
        # 判断天线端口是否有误
        if port_ante not in ['01', '02', '03', '04']:
            print('天线端口错误！')
            return
        a = bytes.fromhex(port_ante)
        # 生成指令
        command_bytes = b'\xff\x03\x91\x00' + a + a
        command_str = ' '.join([f'{b: 03X}' for b in command_bytes])
        # 发送指令
        self.__send_command(command_str)
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        print(boot_data)
        if boot_status != self.OK:
            print("设置天线端口失败")
        else:
            print("设置天线端口成功")

    # 设置若干天线作为标签盘存的天线
    def __Setantennaport_2(self):
        # 判断天线端口是否有误
        for i in self.port_ante:
            if i not in ['01', '02', '03', '04']:
                print('天线端口错误！')
                return
        # 计算数据端长度
        data_length = bytes.fromhex('0'+str(len(self.port_ante)*2+1))
        # 生成指令
        command_bytes = b'\xff' + data_length + b'\x91\x02'
        for i in self.port_ante:
            command_bytes += bytes.fromhex(i)
            command_bytes += bytes.fromhex(i)
        command_str = ''.join([f'{b: 03x}'for b in command_bytes])
        # 发送指令
        self.__send_command(command_str)
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        if boot_status != self.OK:
            print("设置天线端口失败")
        else:
            print("设置天线端口成功")

    '''
    # 设置天线功率
    def Setantennaport_3(port_ante):
        pass
    
    
    # 设置天线功率和定时间
    def Setantennaport_4(port_ante):
        pass
    '''

    # 计算SubCRC
    @classmethod
    def SubCRC(cls, Subcommand) -> str:
        subcrc = hex(sum(Subcommand) & 0xff)[2:]
        return subcrc

    # 开始异步盘存
    def __startinventory(self):
        # 定义指令data段各部分值
        subcommand_code = b'\xaa\x48'
        metadata_flags = (0x0001 | 0x0002 | 0x0008 | 0x0020).to_bytes(length=2, byteorder='big')
        option = b'\x00'
        search_flag = b'\x00\x00'
        access_password = b''
        select_content = b''
        embedded_command_content = b''
        # 链接子命令
        subcommand_data = (metadata_flags + option + search_flag
                           + access_password + select_content + embedded_command_content)
        subcommand = subcommand_code + subcommand_data
        # 计算subcrc
        subcrc = self.SubCRC(subcommand)
        terminator = b'\xbb'
        # 计算data_length
        datalength = (len(self.Moduletech + subcommand + bytes.fromhex(subcrc) + terminator)).to_bytes(1,'big')
        # 链接command
        command = (b'\xff' + datalength + b'\xaa' + self.Moduletech
                   + subcommand + bytes.fromhex(subcrc) + terminator).hex()
        # 发送指令
        self.__send_command(command)
        boot_wait = self.ser.inWaiting()
        boot_data = self.ser.read(boot_wait)
        boot_status = boot_data[3:5]
        if boot_status != self.OK:
            print("启动异步盘存失败")
        else:
            print("启动异步盘存成功")

    # 结束异步盘存
    def __stopinventory(self):
        # 清空串口缓冲区数据
        _ = self.ser.read(self.ser.inWaiting())
        # 发送指令
        self.__send_command('FF 0E AA 4D6F64756C6574656368 AA49 F3 BB')
        # 将缓冲区数据读出，可能有残余数据包
        boot_wait = self.ser.inWaiting()
        # 以\xff为分隔符分割数据
        boot_data = (self.ser.read(boot_wait)).split(b'\xff')
        # 分辨数据中是否有成功结束异步盘存的返回指令
        for data in boot_data:
            if data == b'\x0c\xaa\x00\x00\x4d\x6f\x64\x75\x6c\x65\x74\x65\x63\x68\xaa\x49\x0f\x22':
                print("结束异步盘存成功")
                return
        print("结束异步盘存失败")

    # 标签数据包解码
    def __print_data(self, buffer):
        buffer = bytes.fromhex(buffer)
        # 确保是正确的数据包
        if buffer[2:5] == b'\xaa\x00\x00':
            # 先提取出data段再分割
            data_length = int.from_bytes(buffer[1:2], byteorder='big')
            data = buffer[7:(5+data_length-2)]
            read_count = int.from_bytes(data[0:1], byteorder='big')
            rssi = int.from_bytes(data[1:2], byteorder='big') - 256
            frequency = int.from_bytes(data[2:5], byteorder='big')
            phase = int.from_bytes(data[5:7], byteorder='big')
            epcID = data[10:].hex()
            self.time = time.time()
            # data = dict()
            # if epcID in self.data.keys():
            #     data['盘存次数'] = ((self.data[epcID])[-1])['盘存次数'] + 1
            # print('盘存次数:', read_count, ', RSSI:', rssi, ', 频率:',
            #       frequency, ', phase:', phase, ', epcID:', epcID, ', 时间:', self.time, sep='')
            self.data = dict([('盘存次数', read_count), ('RSSI', rssi), ('频率', frequency),
                              ('phase', phase), ('epcID', epcID), ('时间', self.time)])

    # 读取标签数据
    # class Read():
    #     def __init__(self):
    #         self.num = 0
    #         self.isRun = True
    #
    #     def run(self):
    #         # 读取至数据包开头
    #         buffer = ''
    #         data = ser.read()
    #         while True:
    #             if data == b'\xff':
    #                 break
    #             else:
    #                 data = ser.read()
    #         i = 0
    #         while self.isRun:
    #             # 逐行显示数据包
    #             if data == b'\xff':
    #                 self.print_data(buffer)
    #                 buffer = ''
    #                 i += 1
    #                 # time.sleep(0.5)
    #             # if i % 10 == 0:
    #             #     _ = ser.read(ser.inWaiting())
    #             #     data = ser.read()
    #             #     while True:
    #             #         if data == b'\xff':
    #             #             break
    #             #         else:
    #             #             data = ser.read()
    #             #     buffer += data.hex()
    #             #     continue
    #             buffer += data.hex()
    #             data = ser.read()
    #
    #     def stop(self):
    #         self.isRun = False

    @classmethod
    def kbhit(cls):
        # 检测是否有按键按下
        return keyboard.is_pressed('esc')

    # 异步盘存
    def __Asyncinventory(self):
        self.__startinventory()
        # read = self.Read()
        print('输入esc结束盘存...')
        time.sleep(1)
        self.time = time.time()
        # 读取至数据包开头
        buffer = ''
        data = self.ser.read()
        while True:
            if data == b'\xff':
                break
            else:
                data = self.ser.read()
        i = 0
        # t1 = time.time()
        while True:
            # 逐行显示数据包
            if data == b'\xff':
                self.__print_data(buffer)
                buffer = ''
                i += 1
                # if(int(time.time()-t1)==20):
                #     print(i)
                #     break
                # time.sleep(0.5)
            # if i % 10 == 0:
            #     _ = ser.read(ser.inWaiting())
            #     data = ser.read()
            #     while True:
            #         if data == b'\xff':
            #             break
            #         else:
            #             data = ser.read()
            #     buffer += data.hex()
            #     continue
            buffer += data.hex()
            data = self.ser.read()
            # 判断是否结束盘存
            if self.kbhit():
                break
            # keyboard.add_hotkey('d', read.stop)
            # read.run()
        self.__stopinventory()

    # 外部调用时直接调用该方法即可开启异步盘存
    def run(self):
        self.__port_open()
        self.__Firmware()
        self.__Setantennaport_2()
        self.__SetGEN2()
        self.__Asyncinventory()
        self.__port_close()


if __name__ == '__main__':
    '''
    # 新版串口驱动340需添加以下代码
    try:
        p = seriallp.comports()
        for pi in p:
            # print(pi.device)
            _ = pi.device
        self.ser = serial.Serial('COM3')
        # self.__port_open('COM3')
        # Bootloader()
        self.__port_close()
    except:
        pass
    '''

    hreader = Hreader('com3', '01')
    hreader.run()
