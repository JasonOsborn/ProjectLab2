cmake_minimum_required(VERSION 3.13.4)

project(ProjectLab2_1)

#include

include_directories(./includes ./src)

#target

add_executable(MLX_Test ./src/main.cpp ./src/MLX90640_API.cpp ./src/MLX90640_I2C_Driver.cpp ./src/i2c.c) 
