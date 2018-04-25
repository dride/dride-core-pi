#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <signal.h>
#include <stdarg.h>
#include <getopt.h>

#include "clk.h"
#include "gpio.h"
#include "dma.h"
#include "pwm.h"
#include "version.h"

#include "ws2811.h"

#define TARGET_FREQ WS2811_TARGET_FREQ
#define GPIO_PIN 10
#define DMA 5
#define STRIP_TYPE SK6812_STRIP_GRBW // WS2812/SK6812RGB integrated chip+leds
//#define STRIP_TYPE                            WS2811_STRIP_GBR        // WS2812/SK6812RGB integrated chip+leds
//#define STRIP_TYPE SK6812_STRIP_RGBW // SK6812RGBW (NOT SK6812RGB)
#define LED_COUNT 16

ws2811_t ledstring =
	{
		.freq = TARGET_FREQ,
		.dmanum = DMA,
		.channel =
			{
				[0] =
					{
						.gpionum = GPIO_PIN,
						.count = LED_COUNT,
						.invert = 0,
						.brightness = 255,
						.strip_type = STRIP_TYPE,
					},
			},
};

uint8_t brightness = 32;
uint32_t color(uint8_t r, uint8_t g, uint8_t b, uint8_t w)
{
	return ((((uint32_t)w * brightness) >> 8) << 24) |
		   ((((uint32_t)r * brightness) >> 8) << 16) |
		   ((((uint32_t)g * brightness) >> 8) << 8) |
		   ((((uint32_t)b * brightness) >> 8));
}

void fade(int r1, int g1, int b1, int w1, int r2, int g2, int b2, int w2, int steps, int interval)
{
	int r = 0;
	int g = 0;
	int b = 0;

	for (int i = 0; i < steps; i++)
	{
		r = ((r1 * (steps - i)) + (r2 * i)) / steps;
		g = ((g1 * (steps - i)) + (g2 * i)) / steps;
		b = ((b1 * (steps - i)) + (b2 * i)) / steps;

		usleep(25000);
		ledstring.channel[0].leds[0] = color(r, g, b, 0);

		ws2811_render(&ledstring);
	}
}
//delay in ms
void blink(int r, int g, int b, int delay)
{
	ledstring.channel[0].leds[0] = color(r, g, b, 100);
	ws2811_render(&ledstring);

	if (delay > 0)
	{
		usleep(delay * 1000);

		ledstring.channel[0].leds[0] = color(0, 0, 0, 100);
		ws2811_render(&ledstring);
	}
}

int main(int argc, char *argv[])
{
	ws2811_init(&ledstring);

	if (!strcmp(argv[1], "welcome"))
	{
		fade(0, 0, 0, 0, 255, 255, 255, 0, 40, 0.025);
		fade(255, 255, 255, 0, 0, 0, 0, 0, 40, 0.025);
	}
	else if (!strcmp(argv[1], "isPaired"))
	{
		fade(0, 0, 0, 0, 0, 130, 252, 0, 20, 0.025);
		fade(0, 130, 252, 0, 0, 0, 0, 0, 20, 0.025);
	}
	else if (!strcmp(argv[1], "error"))
	{
		blink(255, 0, 0, -1);
	}
	else if (!strcmp(argv[1], "pending"))
	{
		blink(255, 255, 0, -1);
	}
	else
	{
		printf("Invalid action\n");
	}

	return 0;
}