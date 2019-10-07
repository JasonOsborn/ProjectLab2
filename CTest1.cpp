#include "MLX90640_API.h"
#include "MLX90640_I2C_Driver.h"
#include <iostream>
#include <wiringPiI2C.h>
#include <limits>
#include <fstream>
#include <string>
#include <chrono>


#define MLX_I2C_ADDR 0x33
#define FRAME_TIME_MICROS (100000/32)
#define OFFSET_MICROS 850

using namespace std;

int main()
{
	wiringPiI2CSetup(51); // wiringPiI2CSetup(int ID) where ID is the address in i2cdetect command // MLX = 0x33
	
	
	MLX90640_I2CInit();
	MLX90640_I2CFreqSet(100);
	
	static uint16_t eeMLX90640[832];
	float emissivity = 1;
	uint16_t frame[768];
	static float image[768];
	static float mlx90640To[768];
	float eTa;
	static uint16_t data[768*sizeof(float)];
	string line;
	string OutputLine;
	int c = 0;
	int lineNum = 0;
	FILE * Temperatures2;
	
	auto frame_time = chrono::microseconds(FRAME_TIME_MICROS + OFFSET_MICROS); // !Values to set!
	
	MLX90640_SetDeviceMode(MLX_I2C_ADDR,0);
	MLX90640_SetSubPageRepeat(MLX_I2C_ADDR,0);
	MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b110);
	
	MLX90640_SetChessMode(MLX_I2C_ADDR);
	paramsMLX90640 mlx90640;
	MLX90640_DumpEE(MLX_I2C_ADDR,eeMLX90640);
	MLX90640_ExtractParameteres(eeMLX90640,&mlx90640);
	
	while (1){
		MLX90640_GetFrameData(MLX_I2C_ADDR,frame);
		
		eTa = MLX90640_GetTa(frame, &mlx90640);
		MLX90640_CalculateTo(frame, &mlx90640, emissivity, eTa, mlx90640To);
		
		MLX90640_BadPixelsCorrection((&mlx90640)->brokenPixels, mlx90640To, 1, &mlx90640);
		MLX90640_BadPixelsCorrection((&mlx90640)->outlierPixels, mlx90640To, 1, &mlx90640);
		for (int y = 0; y < 24; y++) {
			for (int x = 0; x < 32; x++) {
				float val = mlx90640To[32* (23-y) + x];
				ifstream Temperatures1("Temperatures.txt");
				while (getline(Temperatures1,line) ){
					c += line.length() + 1;
					if(lineNum >= (32* (23-y) + x))
						break;
					lineNum++;
				}
				Temperatures1.close();
				Temperatures2 = fopen("Temperatures.txt","wb");
				fseek(Temperatures2 , c, SEEK_SET);
				OutputLine = to_string(val);
				OutputLine.append("\n");
				fputs(OutputLine.c_str(),Temperatures2);
				fclose(Temperatures2);
				c = 0;
				lineNum = 0;
			}
		}
	}
	
	return 0;
}
