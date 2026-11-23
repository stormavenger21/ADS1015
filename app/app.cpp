#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <cstdint>

int main() {
    const char* device = "/dev/i2c-1";
    const int ads1015_addr = 0x48; // Default address when ADDR pin is tied to GND

    // ADS1015 Register Pointers
    const uint8_t REG_CONVERSION = 0x00;
    const uint8_t REG_CONFIG     = 0x01;

    // 1. Open I2C bus
    int file = open(device, O_RDWR);
    if (file < 0) {
        std::cerr << "Failed to open /dev/i2c-1\n";
        return 1;
    }

    // 2. Connect to ADS1015
    if (ioctl(file, I2C_SLAVE, ads1015_addr) < 0) {
        std::cerr << "Failed to connect to ADS1015 at 0x48\n";
        close(file);
        return 1;
    }

    // 3. Configure single-shot conversion on AIN0, +/-4.096V range, 1600 SPS
    // Config bits: OS=1 (start), MUX=100 (AIN0 vs GND), PGA=001 (+/-4.096V), MODE=1 (single-shot) -> 0xC3
    // Lower byte:  DR=100 (1600 SPS), COMP_QUE=11 (disable comparator) -> 0x83
    uint8_t config = {REG_CONFIG, 0xC3, 0x83};
    if (write(file, config, 3) != 3) {
        std::cerr << "Failed to write configuration register\n";
        close(file);
        return 1;
    }

    // 4. Wait for conversion to finish (~1ms at 1600 SPS; 2ms gives plenty of margin)
    usleep(2000);

    // 5. Point to the Conversion Register (0x00)
    if (write(file, &REG_CONVERSION, 1) != 1) {
        std::cerr << "Failed to select conversion register\n";
        close(file);
        return 1;
    }

    // 6. Read 2 bytes of conversion data
    uint8_t data = {0};
    if (read(file, data, 2) != 2) {
        std::cerr << "Failed to read conversion data\n";
        close(file);
        return 1;
    }

    // 7. Combine bytes and right-shift 4 bits (ADS1015 is 12-bit left-justified in 16 bits)
    int16_t raw_adc = ((data << 8) | data) >> 4;

    // Handle negative values for 12-bit two's complement
    if (raw_adc > 2047) {
        raw_adc -= 4096;
    }

    // Convert to volts: at +/-4.096V range, 1 LSB = 2mV (0.002V)
    double voltage = raw_adc * 0.002;

    std::cout << "Raw 12-bit value: " << raw_adc << "\n";
    std::cout << "Voltage (AIN0): " << voltage << " V\n";

    close(file);
    return 0;
}
