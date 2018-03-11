/* WiFi Example
 * Copyright (c) 2016 ARM Limited
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
 */

#include "mbed.h"
#include "TCPSocket.h"
#include "C12832.h"
#include "Sht31.h"
#include "CCS811.h"
#include "TSL2561.h"
#include <cstdlib>
#include <string>
using std::string;

#define WIFI_ESP8266    1
#define WIFI_IDW0XX1    2

#if 1
#include "OdinWiFiInterface.h"
OdinWiFiInterface wifi;

#elif TARGET_REALTEK_RTL8195AM
#include "RTWInterface.h"
RTWInterface wifi;

#else // External WiFi modules

#if MBED_CONF_APP_WIFI_SHIELD == WIFI_ESP8266
#include "ESP8266Interface.h"
ESP8266Interface wifi(MBED_CONF_APP_WIFI_TX, MBED_CONF_APP_WIFI_RX);
#elif MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1
#include "SpwfSAInterface.h"
SpwfSAInterface wifi(MBED_CONF_APP_WIFI_TX, MBED_CONF_APP_WIFI_RX);
#endif // MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1

#endif
Serial pc(USBTX, USBRX); // tx, rx

C12832  lcd(PE_14, PE_12, PD_12, PD_11, PE_9);
Sht31 sht31(PF_0, PF_1); //TEMP SENSOR: I2C_SDA, I2C_SCL
CCS811 ccs811(PF_0, PF_1); //IAQ SENSOR: I2C_SDA, I2C_SCL
TSL2561 tsl2561(PF_0, PF_1, TSL2561_ADDR_HIGH); //LIGHT SENSOR: I2C_SDA, I2C_SCL 



void lcd_print(const char* message)
{
    lcd.cls();
    lcd.locate(0, 3);
    pc.printf(message);
}

const char *sec2str(nsapi_security_t sec)
{
    switch (sec) {
        case NSAPI_SECURITY_NONE:
            return "None";
        case NSAPI_SECURITY_WEP:
            return "WEP";
        case NSAPI_SECURITY_WPA:
            return "WPA";
        case NSAPI_SECURITY_WPA2:
            return "WPA2";
        case NSAPI_SECURITY_WPA_WPA2:
            return "WPA/WPA2";
        case NSAPI_SECURITY_UNKNOWN:
        default:
            return "Unknown";
    }
}

int scan_demo(WiFiInterface *wifi)
{
    WiFiAccessPoint *ap;

    pc.printf("Scan:\n");

    int count = wifi->scan(NULL,0);

    /* Limit number of network arbitrary to 15 */
    count = count < 15 ? count : 15;

    ap = new WiFiAccessPoint[count];
    count = wifi->scan(ap, count);
    for (int i = 0; i < count; i++) {
        pc.printf("Network: %s secured: %s BSSID: %hhX:%hhX:%hhX:%hhx:%hhx:%hhx RSSI: %hhd Ch: %hhd\n", ap[i].get_ssid(),
                   sec2str(ap[i].get_security()), ap[i].get_bssid()[0], ap[i].get_bssid()[1], ap[i].get_bssid()[2],
                   ap[i].get_bssid()[3], ap[i].get_bssid()[4], ap[i].get_bssid()[5], ap[i].get_rssi(), ap[i].get_channel());
    }
    pc.printf("%d networks available.\n", count);

    delete[] ap;
    return count;
}

void http_demo(NetworkInterface *net, string ip, string port, string body)
{
    TCPSocket socket;
    nsapi_error_t response;

    printf("Sending HTTP request to %s:%s...\n", ip.data(), port.data());

    // Open a socket on the network interface, and create a TCP connection to www.arm.com
    socket.open(net);
    response = socket.connect(ip.data(), std::atoi(port.data()));
    if(0 != response) {
        printf("Error connecting: %d\n", response);
        socket.close();
        return;
    }
    
    int body_size = strlen(body.data());
    char body_size_s [8];
    sprintf (body_size_s, "%d", body_size);
    string body_size_string = body_size_s;
    
    // Send a simple http request
    string stringbuffer = "";
    stringbuffer += "POST /data HTTP/1.1\r\n";
    stringbuffer += "Host: " + ip + "\r\n";
    stringbuffer += "Content-Type: application/json\r\n";
    //stringbuffer += "Cache-Control: no-cache\r\n";
    stringbuffer += "Content-Length: " + body_size_string + "\r\n";
    stringbuffer += "\r\n";
    stringbuffer += body;
    //POST /data HTTP/1.1
    //Host: www.arm.com
    //Content-Type: application/json
    //Content-Length: + body_size
    //
    //+ body
    
    const char* sbuffer = stringbuffer.data();
    
    nsapi_size_t size = strlen(sbuffer);
    response = 0;
    while(size) {
        response = socket.send(sbuffer+response, size);
        if (response < 0) {
            printf("Error sending data: %d\n", response);
            socket.close();
            return;
        } else {
            size -= response;
            // Check if entire message was sent or not
            printf("sent %d [%.*s]\n", response, strstr(sbuffer, "\r\n")-sbuffer, sbuffer);
        }
    }

    // Recieve a simple http response and print out the response line
    char rbuffer[64];
    response = socket.recv(rbuffer, sizeof rbuffer);
    if (response < 0) {
        printf("Error receiving data: %d\n", response);
    } else {
        printf("recv %d [%.*s]\n", response, strstr(rbuffer, "\r\n")-rbuffer, rbuffer);
    }

    // Close the socket to return its memory and bring down the network interface
    socket.close();
}
void display(const char* out){
    printf("%s\n", out);
    }

int main()
{
    int count = 0;

    pc.printf("WiFi example\n\n");

    count = scan_demo(&wifi);
    if (count == 0) {
        pc.printf("No WIFI APNs found - can't continue further.\n");
        return -1;
    }

    printf("\nConnecting to %s...\n", MBED_CONF_APP_WIFI_SSID);
    int ret = wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
    if (ret != 0) {
        pc.printf("\nConnection error\n");
        return -1;
    }

    pc.printf("Success\n\n");
    printf("MAC: %s\n", wifi.get_mac_address());
    printf("IP: %s\n", wifi.get_ip_address());
    printf("Netmask: %s\n", wifi.get_netmask());
    printf("Gateway: %s\n", wifi.get_gateway());
    printf("RSSI: %d\n\n", wifi.get_rssi());
    
    ccs811.init();
    tsl2561.begin();
    tsl2561.setGain(TSL2561_GAIN_0X);
    tsl2561.setTiming(TSL2561_INTEGRATIONTIME_402MS);
    
    
    
    string ip = "34.245.151.229";
    string port = "5000";
    
    while(1) {
        
        string json = "{\n";
        
        //Light
        
        int x = tsl2561.getLuminosity(TSL2561_VISIBLE);
        
        //printf("VIS: %d\n", x);
        
        char buffer [8];
        sprintf (buffer, "%d", x);
        
        json += "\t \"Light\" : ";
        json += buffer;
        json += ".0,\n";
        
        //Air
        
        uint16_t eco2, tvoc;
        ccs811.readData(&eco2, &tvoc);
        
        //printf("eCO2:%dppm\n", eco2);
        
        sprintf (buffer, "%d", eco2);
        
        json += "\t \"eCO2\"  : ";
        json += buffer;
        json += ".0,\n";
        
        //Hum and Temp
        
        float t = sht31.readTemperature();
        float h = sht31.readHumidity();
        
        //printf("TEMP:%3.2fC\n", t);
        //printf("HUM:%3.2f%%\n", h);
        
        sprintf (buffer, "%3.2f", t);
        
        json += "\t \"Tempr\" : ";
        json += buffer;
        json += ",\n";
        
        sprintf (buffer, "%3.2f", h);
        
        json += "\t \"Humid\" : ";
        json += buffer;
        json += "\n";
        
        json += "}\n\n";
        printf("%s", json.data());
        
        http_demo(&wifi, ip, port, json);
        
        wait(600);
    }
    
    wifi.disconnect();

    printf("\nDone\n");
}
