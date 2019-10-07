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

int MLX90640_SetSubPageRepeat(uint8_t slaveAddr, uint8_t subPageRepeat)
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
