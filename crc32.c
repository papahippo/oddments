#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>

#define CRC32_TOPBIT                        0x80000000L  // (1 << (CRC32_WIDTH - 1))
#define CRC32_SHIFT                         24           // (derived from CRC32_SHIFT_FAC: shift right 24 bits)
#define CRC32_POLYNOMIAL                    0x04C11DB7L

#define IRIS_ENDIAN_LONG(I32) __builtin_bswap32(I32)

static void CRC32_accrue(uint32_t *pRemainder, uint8_t *pBytes, unsigned int byte_count)
{
	unsigned long remainder = IRIS_ENDIAN_LONG(*pRemainder);
	while (byte_count--)
	{
		int bit_count = 8;
		remainder ^= ((uint32_t)(*pBytes++) << 24);
		while(bit_count--)
		{
			if (remainder & CRC32_TOPBIT)
			{
				remainder = ((remainder << 1) ^ CRC32_POLYNOMIAL);
			}
			else
			{
				remainder = (remainder << 1);
			}
		}
	}
	*pRemainder = IRIS_ENDIAN_LONG(remainder);
}

static uint32_t workingCRC = 0xffffffff, interpretedCRC;

int main(int argc, char **argv)
{
    static unsigned char tinyString[9];

    char *prog_name = *argv++;

    if (--argc) strcpy(tinyString, *argv++); else strcpy(tinyString, "12345678"); // "43218765");

    CRC32_accrue(&workingCRC, tinyString, 8);

    workingCRC ^= 0xffffffff;
    interpretedCRC = IRIS_ENDIAN_LONG(workingCRC);
    printf("running \'%s\' on \'%s\'gives CRC32 = 0x%08x", prog_name, tinyString, interpretedCRC);

}
