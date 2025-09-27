#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import time
import socket
import subprocess
import psutil
import platform
import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
import traceback
import glob
import stat

# Try to import the correct epd module
try:
    from waveshare_epd import epd2in13_V4
    EPD_CLASS = epd2in13_V4.EPD
    print("Using epd2in13_V4")
except ImportError:
    try:
        from waveshare_epd import epd2in13_V2
        EPD_CLASS = epd2in13_V2.EPD
        print("Using epd2in13_V2")
    except ImportError:
        try:
            from waveshare_epd import epd2in13
            EPD_CLASS = epd2in13.EPD
            print("Using epd2in13")
        except ImportError:
            print("Error: Could not import any 2.13\" e-ink display module!")
            sys.exit(1)

logging.basicConfig(level=logging.DEBUG)

class PiDisplay:
    def __init__(self):
        """Initialize the e-ink display."""
        self.epd = EPD_CLASS()
        self.width = self.epd.width
        self.height = self.epd.height
        
        # Cache for Rick images
        self.rick_images_cache = []
        self.last_scan_time = 0
        self.scan_interval = 30  # Scan for new images every 30 seconds
        
        # File monitoring for auto-restart
        self.script_path = os.path.abspath(__file__)
        self.script_mtime = os.path.getmtime(self.script_path)

        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear(0xFF)

        # Try to load cyberpunk fonts with fallbacks
        try:
            # Try Orbitron first (if downloaded)
            self.font12 = ImageFont.truetype("/home/pi/.fonts/Orbitron-Regular.ttf", 12)
            self.font15 = ImageFont.truetype("/home/pi/.fonts/Orbitron-Regular.ttf", 15)
            self.font18 = ImageFont.truetype("/home/pi/.fonts/Orbitron-Bold.ttf", 18)
            self.font24 = ImageFont.truetype("/home/pi/.fonts/Orbitron-Bold.ttf", 24)
            self.font32 = ImageFont.truetype("/home/pi/.fonts/Orbitron-Bold.ttf", 32)
            logging.info("Using Orbitron cyberpunk fonts")
        except:
            try:
                # Try Liberation Mono (monospace cyberpunk look)
                self.font12 = ImageFont.truetype("/home/pi/.fonts/LiberationMono-Regular.ttf", 12)
                self.font15 = ImageFont.truetype("/home/pi/.fonts/LiberationMono-Regular.ttf", 15)
                self.font18 = ImageFont.truetype("/home/pi/.fonts/LiberationMono-Bold.ttf", 18)
                self.font24 = ImageFont.truetype("/home/pi/.fonts/LiberationMono-Bold.ttf", 24)
                self.font32 = ImageFont.truetype("/home/pi/.fonts/LiberationMono-Bold.ttf", 32)
                logging.info("Using Liberation Mono cyberpunk fonts")
            except:
                try:
                    # Try Roboto Mono (modern monospace)
                    self.font12 = ImageFont.truetype("/home/pi/.fonts/RobotoMono-Regular.ttf", 12)
                    self.font15 = ImageFont.truetype("/home/pi/.fonts/RobotoMono-Regular.ttf", 15)
                    self.font18 = ImageFont.truetype("/home/pi/.fonts/RobotoMono-Bold.ttf", 18)
                    self.font24 = ImageFont.truetype("/home/pi/.fonts/RobotoMono-Bold.ttf", 24)
                    self.font32 = ImageFont.truetype("/home/pi/.fonts/RobotoMono-Bold.ttf", 32)
                    logging.info("Using Roboto Mono cyberpunk fonts")
                except:
                    try:
                        # Try system monospace fonts
                        self.font12 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 12)
                        self.font15 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 15)
                        self.font18 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 18)
                        self.font24 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 24)
                        self.font32 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 32)
                        logging.info("Using system Liberation Mono fonts")
                    except:
                        # Final fallback to DejaVu
                        self.font12 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
                        self.font15 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
                        self.font18 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
                        self.font24 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                        self.font32 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                        logging.info("Using DejaVu fonts (fallback)")

    def get_device_name(self):
        """Get the device name (hostname)"""
        return platform.node()

    def get_ip_address(self):
        """Get the primary IP address of the Raspberry Pi."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                return result.stdout.strip().split()[0]
            except:
                return "No IP"

    def get_cpu_percent(self):
        """Get CPU usage percentage"""
        try:
            return psutil.cpu_percent(interval=1)
        except:
            return 0

    def get_memory_percent(self):
        """Get memory usage percentage"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except:
            return 0

    def get_disk_percent(self):
        """Get disk usage percentage"""
        try:
            disk = psutil.disk_usage('/')
            return (disk.used / disk.total) * 100
        except:
            return 0

    def get_cpu_temperature(self):
        """Get CPU temperature in Fahrenheit"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_c = int(f.read()) / 1000.0
            temp_f = (temp_c * 9/5) + 32
            return temp_f
        except:
            return 0

    def get_weather(self):
        """Get real weather information for the local area."""
        try:
            # Try to get location from IP
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                location_data = response.json()
                city = location_data.get('city', 'Unknown')
                country = location_data.get('country', '')
                region = location_data.get('regionName', '')
                lat = location_data.get('lat')
                lon = location_data.get('lon')
                
                # Get real weather data using WeatherAPI (no API key required)
                if lat and lon:
                    weather_data = self.get_real_weather(lat, lon)
                    if weather_data:
                        return {
                            'city': city,
                            'country': country,
                            'region': region,
                            'temp': weather_data.get('current_temp', 'N/A'),
                            'description': weather_data.get('current_desc', 'Unknown'),
                            'forecast': weather_data.get('forecast', self.generate_mock_forecast()),
                            'error': None
                        }
                
                # Fallback to system temperature if weather API fails
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp_c = int(f.read()) / 1000.0
                    temp_f = (temp_c * 9/5) + 32
                    temp_str = f"{temp_f:.1f}°F"
                except:
                    temp_str = "N/A"
                
                return {
                    'city': city,
                    'country': country,
                    'region': region,
                    'temp': temp_str,
                    'description': 'System Temperature',
                    'forecast': self.generate_mock_forecast(),
                    'error': 'Weather API failed'
                }
        except:
            pass
        
        return {
            'city': 'Local Area',
            'country': '',
            'region': '',
            'temp': 'N/A',
            'description': 'No connection',
            'forecast': self.generate_mock_forecast(),
            'error': 'Connection failed'
        }

    def get_real_weather(self, lat, lon):
        """Get real weather data from WeatherAPI."""
        try:
            # WeatherAPI free tier (no API key required for basic usage)
            url = f"http://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q={lat},{lon}&days=3"
            
            # For now, let's use a free alternative - Open-Meteo (no API key required)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,weathercode&timezone=auto&temperature_unit=fahrenheit"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Get current temperature (use first day's max as current)
                current_temp = int(data['daily']['temperature_2m_max'][0])
                current_desc = self.get_weather_description(data['daily']['weathercode'][0])
                
                # Generate 3-day forecast
                forecast = []
                for i in range(3):
                    day = time.localtime(time.time() + i * 86400)
                    day_name = time.strftime('%a', day)
                    high_temp = int(data['daily']['temperature_2m_max'][i])
                    weather_desc = self.get_weather_description(data['daily']['weathercode'][i])
                    
                    forecast.append({
                        'day': day_name,
                        'desc': weather_desc,
                        'temp': f"{high_temp}°F"
                    })
                
                return {
                    'current_temp': f"{current_temp}°F",
                    'current_desc': current_desc,
                    'forecast': forecast
                }
        except Exception as e:
            logging.error(f"Weather API error: {e}")
        
        return None

    def get_weather_description(self, weather_code):
        """Convert weather code to description."""
        weather_codes = {
            0: 'Clear', 1: 'Clear', 2: 'Partly Cloudy', 3: 'Overcast',
            45: 'Foggy', 48: 'Foggy', 51: 'Drizzle', 53: 'Drizzle', 55: 'Drizzle',
            61: 'Rainy', 63: 'Rainy', 65: 'Rainy', 71: 'Snowy', 73: 'Snowy', 75: 'Snowy',
            77: 'Snowy', 80: 'Rainy', 81: 'Rainy', 82: 'Rainy', 85: 'Snowy', 86: 'Snowy',
            95: 'Stormy', 96: 'Stormy', 99: 'Stormy'
        }
        return weather_codes.get(weather_code, 'Unknown')

    def generate_mock_forecast(self):
        """Generate a mock 3-day weather forecast with daily high temperatures."""
        import random
        
        # Weather types with realistic daily high temperatures
        weather_types = [
            {'desc': 'Sunny', 'high_f': 75},
            {'desc': 'Cloudy', 'high_f': 68},
            {'desc': 'Rainy', 'high_f': 62},
            {'desc': 'Stormy', 'high_f': 58},
            {'desc': 'Partly Cloudy', 'high_f': 72},
            {'desc': 'Foggy', 'high_f': 65}
        ]
        
        forecast = []
        for i in range(3):
            day = time.localtime(time.time() + i * 86400)
            day_name = time.strftime('%a', day)
            weather = random.choice(weather_types)
            forecast.append({
                'day': day_name,
                'desc': weather['desc'],
                'temp': f"{weather['high_f']}°F"  # Daily high temperature
            })
        
        return forecast

    def scan_for_rick_images(self):
        """Scan for Rick Sanchez images and update cache."""
        current_time = time.time()
        
        # Only scan every scan_interval seconds
        if current_time - self.last_scan_time < self.scan_interval:
            return self.rick_images_cache
        
        self.last_scan_time = current_time
        logging.info("Scanning for Rick Sanchez images...")
        
        # Clear cache
        self.rick_images_cache = []
        
        # Check multiple locations
        search_paths = [
            "/custom-faces/",
            "./custom-faces/",
            "./",
            "/home/pi/custom-faces/"
        ]
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                logging.info(f"Scanning path: {search_path}")
                
                # Look for PNG files that might be Rick faces
                pattern = os.path.join(search_path, "*.png")
                png_files = glob.glob(pattern)
                
                # Filter for likely Pickle Rick face files (case insensitive)
                pickle_rick_keywords = ['pickle', 'rick', 'look', 'happy', 'sleep', 'awake', 'bored', 'intense', 
                                       'cool', 'excited', 'grateful', 'motivated', 'demotivated', 
                                       'smart', 'lonely', 'sad', 'angry', 'friend', 'broken', 'debug', 'upload']
                
                for png_file in png_files:
                    filename = os.path.basename(png_file).lower()
                    if any(keyword in filename for keyword in pickle_rick_keywords):
                        self.rick_images_cache.append(png_file)
                        logging.info(f"Found Pickle Rick image: {png_file}")
        
        logging.info(f"Total Pickle Rick images found: {len(self.rick_images_cache)}")
        return self.rick_images_cache

    def get_rick_expression(self):
        """Get a random Pickle Rick ASCII expression."""
        import random
        
        # Always use Pickle Rick ASCII art (no images for now)
        # Using basic ASCII characters that work on e-ink displays
        pickle_rick_ascii = [
            "( o_o)",  # pickle look_r
            "(o_o )",  # pickle look_l
            "( ^_^)",  # pickle look_r_happy
            "(^_^ )",  # pickle look_l_happy
            "( -_-)",  # pickle sleep
            "(=_=)",   # pickle sleep2
            "(^_^)",   # pickle awake
            "(-__-)",  # pickle bored
            "(>_<)",   # pickle intense
            "(^_^)",   # pickle cool
            "(^_^)",   # pickle happy
            "(^o^)",   # pickle excited
            "(^_^)",   # pickle grateful
            "(^_^)",   # pickle motivated
            "(-_-)",   # pickle demotivated
            "(^_^)",   # pickle smart
            "(T_T)",   # pickle lonely
            "(T_T)",   # pickle sad
            "(>_<)",   # pickle angry
            "(^_^)",   # pickle friend
            "(X_X)",   # pickle broken
            "(#_#)",   # pickle debug
            "(1_0)",   # pickle upload
            "(1_1)",   # pickle upload1
            "(0_1)"    # pickle upload2
        ]
        
        selected_ascii = random.choice(pickle_rick_ascii)
        logging.info(f"Selected Pickle Rick ASCII: {selected_ascii}")
        return selected_ascii


    def draw_system_info(self):
        """Draw system information with device name, IP, CPU%, and Mem%."""
        logging.info("Drawing system information...")

        # Create image with correct dimensions (height x width)
        image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Get system information
        device_name = self.get_device_name()
        ip_address = self.get_ip_address()
        cpu_percent = self.get_cpu_percent()
        mem_percent = self.get_memory_percent()

        # Draw title with border
        draw.rectangle([(0, 0), (self.epd.height-1, 30)], outline=0)
        draw.text((5, 8), f"Device: {device_name}", font=self.font15, fill=0)

        # Draw system info in boxes
        y_start = 40

        # IP Address box
        draw.rectangle([(0, y_start), (self.epd.height-1, y_start+25)], outline=0)
        draw.text((5, y_start+5), f"IP: {ip_address}", font=self.font15, fill=0)

        # CPU usage box
        y_start += 30
        draw.rectangle([(0, y_start), (self.epd.height-1, y_start+25)], outline=0)
        draw.text((5, y_start+5), f"CPU: {cpu_percent:.1f}%", font=self.font15, fill=0)

        # Memory usage box
        y_start += 30
        draw.rectangle([(0, y_start), (self.epd.height-1, y_start+25)], outline=0)
        draw.text((5, y_start+5), f"Mem: {mem_percent:.1f}%", font=self.font15, fill=0)

        return image

    def draw_clock(self):
        """Draw a large clock filling the screen."""
        logging.info("Drawing clock...")

        # Create image with correct dimensions
        image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Get current time
        now = time.localtime()
        time_str = time.strftime('%H:%M', now)
        date_str = time.strftime('%A, %B %d', now)

        # Center the time on screen
        time_bbox = draw.textbbox((0, 0), time_str, font=self.font32)
        time_width = time_bbox[2] - time_bbox[0]
        time_height = time_bbox[3] - time_bbox[1]
        
        time_x = (self.epd.height - time_width) // 2
        time_y = (self.epd.width - time_height) // 2 - 20

        # Draw time
        draw.text((time_x, time_y), time_str, font=self.font32, fill=0)

        # Draw date below time
        date_bbox = draw.textbbox((0, 0), date_str, font=self.font15)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = (self.epd.height - date_width) // 2
        date_y = time_y + time_height + 10

        draw.text((date_x, date_y), date_str, font=self.font15, fill=0)

        return image

    def draw_weather(self):
        """Draw weather information with 3-day forecast."""
        logging.info("Drawing weather...")

        # Create image with correct dimensions
        image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Get weather data
        weather = self.get_weather()

        # Draw title
        draw.rectangle([(0, 0), (self.epd.height-1, 25)], outline=0)
        draw.text((5, 5), "Weather Forecast", font=self.font15, fill=0)

        # Draw location
        if weather['region']:
            location = f"{weather['city']}, {weather['region']}"
        else:
            location = f"{weather['city']}, {weather['country']}"
        draw.text((5, 30), location, font=self.font12, fill=0)

        # Draw current temperature
        temp_text = f"Now: {weather['temp']}"
        draw.text((5, 45), temp_text, font=self.font12, fill=0)

        # Draw 3-day forecast
        y_start = 65
        for i, day in enumerate(weather['forecast']):
            # Draw day name
            draw.text((5, y_start), day['day'], font=self.font12, fill=0)
            
            # Draw weather icon (ASCII)
            draw.text((35, y_start), day['icon'], font=self.font12, fill=0)
            
            # Draw temperature
            temp_text = day['temp']
            draw.text((70, y_start), temp_text, font=self.font12, fill=0)
            
            # Draw description (abbreviated)
            desc = day['desc'][:6]  # Limit to 6 chars for space
            draw.text((100, y_start), desc, font=self.font12, fill=0)
            
            y_start += 15

        # Draw error message if any
        if weather.get('error'):
            draw.text((5, y_start + 5), f"Note: {weather['error']}", font=self.font12, fill=0)

        return image

    def draw_combined_screen(self):
        """Draw the combined screen with hostname, IP, clock, and 3-day weather."""
        logging.info("Drawing combined screen...")

        # Create image with correct dimensions
        image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Get system information
        device_name = self.get_device_name()
        ip_address = self.get_ip_address()
        weather = self.get_weather()
        rick_face = self.get_rick_expression()

        # Top row: Hostname (left), Face (center), IP (right)
        draw.text((5, 5), device_name, font=self.font12, fill=0)
        
        # Center the Pickle Rick face
        face_bbox = draw.textbbox((0, 0), rick_face, font=self.font12)
        face_width = face_bbox[2] - face_bbox[0]
        face_x = (self.epd.height - face_width) // 2
        face_y = 5
        draw.text((face_x, face_y), rick_face, font=self.font12, fill=0)
        
        # Right-align IP address
        ip_bbox = draw.textbbox((0, 0), ip_address, font=self.font12)
        ip_width = ip_bbox[2] - ip_bbox[0]
        ip_x = self.epd.height - ip_width - 5
        draw.text((ip_x, 5), ip_address, font=self.font12, fill=0)

        # Right side: Large clock and date
        now = time.localtime()
        time_str = time.strftime('%I:%M %p', now)
        date_str = time.strftime('%A, %B %d', now)

        # Position time on the right side (much larger)
        time_bbox = draw.textbbox((0, 0), time_str, font=self.font32)  # Already large font
        time_width = time_bbox[2] - time_bbox[0]
        time_x = self.epd.height - time_width - 5
        time_y = 30

        draw.text((time_x, time_y), time_str, font=self.font32, fill=0)

        # Position date below time with more spacing
        date_bbox = draw.textbbox((0, 0), date_str, font=self.font12)  # Reduced to font12 to prevent overlap
        date_width = date_bbox[2] - date_bbox[0]
        date_x = self.epd.height - date_width - 5
        date_y = time_y + 40  # Reduced spacing to prevent overlap

        draw.text((date_x, date_y), date_str, font=self.font12, fill=0)

        # Left side: Weather info in rows (moved up 3 lines)
        weather_y_start = 20  # Moved up 3 lines from 50 to 20
        
        # Draw weather for today, tomorrow, and day after in rows
        for i, day in enumerate(weather['forecast']):
            y_pos = weather_y_start + (i * 25)  # Reduced spacing to remove blank lines
            
            # Draw day name and temperature on same line
            day_temp_text = f"{day['day']} | {day['temp']}"
            draw.text((5, y_pos), day_temp_text, font=self.font12, fill=0)
            
            # Draw description on next line
            desc = day['desc']
            draw.text((5, y_pos + 15), desc, font=self.font12, fill=0)

        # Lower right: System stats (CPU%, Mem%, Disk%, Temp) - Horizontal
        cpu_percent = self.get_cpu_percent()
        mem_percent = self.get_memory_percent()
        disk_percent = self.get_disk_percent()
        cpu_temp = self.get_cpu_temperature()
        
        # System stats text - all on one line
        stats_text = f"CPU:{cpu_percent:.0f}% MEM:{mem_percent:.0f}% DSK:{disk_percent:.0f}% TMP:{cpu_temp:.0f}°F"
        
        # Position in lower right corner
        stats_y = self.epd.width - 20  # 20px from bottom
        
        # Right-align the stats
        stats_bbox = draw.textbbox((0, 0), stats_text, font=self.font12)
        stats_width = stats_bbox[2] - stats_bbox[0]
        stats_x = self.epd.height - stats_width - 5
        
        draw.text((stats_x, stats_y), stats_text, font=self.font12, fill=0)
        
        logging.info(f"Displayed Pickle Rick ASCII: {rick_face}")
        return image

    def check_script_update(self):
        """Check if the script file has been updated."""
        try:
            current_mtime = os.path.getmtime(self.script_path)
            if current_mtime > self.script_mtime:
                logging.info("Script file updated, restarting...")
                return True
        except Exception as e:
            logging.error(f"Error checking script update: {e}")
        return False

    def run_demo(self):
        """Run the continuous update loop with partial refresh."""
        try:
            logging.info("Starting continuous display loop with partial refresh...")
            
            # Set up partial update base image
            base_image = Image.new('1', (self.epd.height, self.epd.width), 255)
            self.epd.displayPartBaseImage(self.epd.getbuffer(base_image))
            
            while True:
                try:
                    # Check if script has been updated
                    if self.check_script_update():
                        logging.info("Restarting script due to file update...")
                        # Restart the script
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                        break
                    
                    # Draw the updated screen
                    image = self.draw_combined_screen()
                    
                    # Use partial refresh for faster updates
                    self.epd.displayPartial(self.epd.getbuffer(image))
                    
                    # Wait 60 seconds before next update
                    logging.info("Display updated with partial refresh, waiting 60 seconds...")
                    time.sleep(60)
                    
                except KeyboardInterrupt:
                    logging.info("Keyboard interrupt received, exiting...")
                    break
                except Exception as e:
                    logging.error(f"Error in display loop: {e}")
                    traceback.print_exc()
                    # Wait a bit before retrying
                    time.sleep(10)

        except Exception as e:
            logging.error(f"Error in demo: {e}")
            traceback.print_exc()

    def cleanup(self):
        """Clean up resources."""
        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        self.epd.sleep()

def main():
    """Main function."""
    try:
        display = PiDisplay()
        display.run_demo()
        display.cleanup()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        try:
            EPD_CLASS.epdconfig.module_exit(cleanup=True)
        except:
            pass
        exit()

if __name__ == "__main__":
    main()
