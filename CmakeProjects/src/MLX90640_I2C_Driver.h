/**
 * @copyright (C) 2017 Melexis N.V.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
 

#include "/home/pi/Desktop/ProjectLab2/includes/MLX90640_I2C_Driver.h"
#include <wiringPiI2C.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <iostream>
#include <fstream>
#include "/home/pi/Desktop/ProjectLab2/includes/i2c.h"
#include <cstring>


int MLX90640_I2CRead(uint8_t slaveAddr, uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data)
{
    uint8_t sa;
    int i = 0;
    char cmd[2] = {0,0};
    char i2cData[1664] = {0};
    uint16_t *p;
    int fd;
    if((fd = i2c_open("/dev/i2c-1")) == -1) {
        return -1;
    }
    I2CDevice MLX;
    memset(&MLX, 0, sizeof(MLX));
    
    MLX.bus = fd;
    MLX.addr = 0x33;
    MLX.iaddr_bytes = 0;
    MLX.page_bytes = 32;
    
    unsigned char buffer[256]
    ssize_t size = sizeof(buffer);
    memset(buffer,0,sizeof(buffer));
    
    if (i2c_ioctl_write(&MLX,0x33,buffer,size)) != size {
        return -1;
    }
    
    p = data;
    sa = (slaveAddr << 1);
    cmd[0] = startAddress >> 8;
    cmd[1] = startAddress & 0x00FF;
    
    write(fd,cmd,2);
    
    sa = sa | 0x01;
    
    read(fd,i2cData,nMemAddressRead);
    
    close(fd);  
    
    for(int cnt=0; cnt < nMemAddressRead; cnt++)
    {
        i = cnt << 1;
        *p++ = (uint16_t)i2cData[i]*256 + (uint16_t)i2cData[i+1];
        printf("@pointer number %x value = %d\n",p-data-1,*(p-1));
    }
    
    return 0;   
} 


int MLX90640_I2CWrite(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
    uint8_t sa;
    char cmd[4] = {0,0,0,0};
    static uint16_t dataCheck;
    char *filename = (char*)"/dev/i2c-1";
    int fd;
    fd = open(filename,O_RDWR);
    ioctl(fd,I2C_SLAVE,0x33);
    

    sa = (slaveAddr << 1);
    cmd[0] = writeAddress >> 8;
    cmd[1] = writeAddress & 0x00FF;
    cmd[2] = data >> 8;
    cmd[3] = data & 0x00FF;
    
    if(write(fd,cmd,4) != 4){
        return -1;
    }
             
    sa = sa | 0x01;
    
    close(fd); 
    
    MLX90640_I2CRead(slaveAddr,writeAddress,1, &dataCheck);
    
    if ( dataCheck != data)
    {
        return -2;
    }    
    
    return 0;
}


int MLX90640_SetDeviceMode(uint8_t slaveAddr, uint8_t deviceMode)
{
    uint16_t controlRegister1;
    int value;
    int error;

    value = (deviceMode & 0x01)<<4;

    error = MLX90640_I2CRead(slaveAddr, 0x800D, 1, &controlRegister1);
    if(error == 0)
    {
        value = (controlRegister1 & 0b1111111111111101) | value;
        error = MLX90640_I2CWrite(slaveAddr, 0x800D, value);
    }

    return error;
}

int MLX90640_SetSubPageRepeat(uint8_t slaveAddr,uint8_t subPageRepeat)
{
    uint16_t controlRegister1;
    int value;
    int error;

    value = (subPageRepeat & 0x01)<<3;

    error = MLX90640_I2CRead(slaveAddr, 0x800D, 1, &controlRegister1);
    if(error == 0)
    {
        value = (controlRegister1 & 0b1111111111110111) | value;
        error = MLX90640_I2CWrite(slaveAddr, 0x800D, value);
    }

    return error;
}
