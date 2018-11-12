#!/usr/bin/env python3
# -*- coding: utf-8 -*-


################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# 根據Apache許可證2.0版（“許可證”）獲得許可;
# 除非符合許可，否則您不得使用此文件。.
# 您可以在以下位置獲取許可證副本
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 除非適用法律要求或書面同意，否則軟件
# 根據許可證分發的“按現狀”分發，
# 不附帶任何明示或暗示的保證或條件。
# 有關管理權限的特定語言，請參閱許可證
# 許可證下的限制。
################################################################################

# Author: 黃祥晏 (Rod)

#
# *********    讀寫示例      *********
#
#

#此示例中可用的DXL模型：所有模型使用Protocol 1.0
# 此示例使用DXL AX-12和USB2DYNAMIXEL進行測試
# 確保DXL AX屬性已設置為%% ID：1 / Baudnum：34（波特率：57600）
#

import os  #正如其名，主要与操作系统打交道的
from time import sleep
if os.name == 'nt':  #字符串指示你正在使用的平台。比如对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'。
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_DXL_CW_ANGLE_LIMIT    = 26
ADDR_DXL_CCW_ANGLE_LIMIT   = 27
ADDR_DXL_PRESENT_SPEED     = 38
ADDR_DXL_DRIVE_MODE        = 10
ADDR_DXL_GOAL_SPEED        = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
#馬達的ID修改處與波特率的修改處與Port設定的地方
DXL_ID                      = 1                 # Dynamixel ID : 1
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 1000000  
DEVICENAME                  = 'COM9'    # Check w hich port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100          # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 10                # Dynamixel moving status threshold 動態像素移動狀態閾值


index = 0
#dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position 的兩個位置

# Initialize PortHandler instance  初始化PortHandler實例
# Set the port path  設置端口路徑
# Get methods and members of PortHandlerLinux or PortHandlerWindows  獲取PortHandlerLinux或PortHandlerWindows的方法和成員
portHandler = PortHandler(DEVICENAME)  ##這個設定有在上面

# Initialize PacketHandler instance  初始化PacketHandler實例
# Set the protocol version   設置協議版本
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler  獲取Protocol1PacketHandler或Protocol2PacketHandler的方法和成員
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port  打開端口
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate  設置端口波特率
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque  啟用Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

# #cw設0
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_DXL_CW_ANGLE_LIMIT, 0)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))
# else:
#     print("Dynamixel CW angle set to 0 successfully")

# #ccw設0
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_DXL_CCW_ANGLE_LIMIT, 0)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))
# else:
#     print("Dynamixel CCW angle set to 0 successfully")

angle_goal=[]

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break
    angle_present_goal=angle_goal  #把之前的位置給他
    angle_goal = int(input("input:"))
    
    #寫下馬達的速度 當 angle_goal 大於 angle_present_goal
    if angle_goal > angle_present_goal :
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_DXL_GOAL_SPEED,1000)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
    #寫下馬達的速度 當 angle_goal 小於 angle_present_goal
    if angle_goal < angle_present_goal :
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_DXL_GOAL_SPEED,2000)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


    i=0
    circle=0
    angle_present=0
    angle_pass=0


    while 1:
        
        # Read present position  閱讀現在的位置
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))   
        #判斷圈數
        real_pulse = dxl_present_position% 4096        
        if real_pulse == 1023:
            i=1
        elif real_pulse == 0 and i == 1:
            circle+=1
            i=0
            angle_pass+=360

        #紀錄角度目前位置
        angle_present = real_pulse/3  #
         
        print("[ID:%d]  PresPos:%s  circle:%d angle:%d" % (DXL_ID, real_pulse, circle,angle_present+angle_pass ))


        #目標位置停止
        if angle_pass+angle_present-5 <= angle_goal <= angle_pass+angle_present+5  :
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_DXL_GOAL_SPEED,0)
            if dxl_comm_result != COMM_SUCCESS: 
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            

            break 
        
# Disable Dynamixel Torque  禁用Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
   


   
