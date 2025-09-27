# Pi Display - E-ink Screen Companion

A Raspberry Pi Zero 2 e-ink display project featuring real-time system monitoring, weather data, and cyberpunk aesthetics.

## 🌟 Features

- **Real-time System Stats**: CPU%, Memory%, Disk%, Temperature
- **Live Weather Data**: 3-day forecast using Open-Meteo API
- **Cyberpunk Fonts**: Monospace fonts for a futuristic look
- **Auto-start Service**: Runs automatically on boot
- **Pickle Rick Expressions**: Random ASCII art faces
- **Partial Refresh**: Fast, smooth display updates
- **Auto-restart**: Detects file changes and restarts automatically

## 📋 Hardware Requirements

- Raspberry Pi Zero 2 (or compatible)
- Waveshare 2.13" e-ink display (non-touch)
- MicroSD card (8GB+)
- Power supply for Pi

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/JohnFiedler/pidisplay.git
cd pidisplay
```

### 2. Install Dependencies
```bash
# Install Python packages
pip3 install -r requirements.txt

# Install system dependencies
sudo apt update
sudo apt install -y python3-pil python3-requests python3-psutil
```

### 3. Install Waveshare Library
```bash
# Run the installation script
chmod +x install_local.sh
./install_local.sh
```

### 4. Set Up Cyberpunk Fonts
```bash
# Install cyberpunk fonts
chmod +x use_system_cyberpunk.sh
./use_system_cyberpunk.sh
```

### 5. Enable Auto-start
```bash
# Set up systemd service
chmod +x setup_autostart.sh
./setup_autostart.sh
```

### 6. Start the Display
```bash
# Start the service
sudo systemctl start pidisplay.service

# Check status
sudo systemctl status pidisplay.service
```

## 📱 Display Layout

```
┌─────────────────────────────────┐
│ Hostname    (^_^)    IP Address │
│                                 │
│ Fri | 68°F          12:34 PM    │
│ Cloudy                         │
│                                 │
│ Sat | 72°F           Friday,    │
│ Sunny              September 27 │
│                                 │
│ Sun | 65°F                      │
│ Rainy                           │
│                                 │
│ CPU:15% MEM:45% DSK:23% TMP:98°F│
└─────────────────────────────────┘
```

## 🔧 Configuration

### Weather API
The display uses Open-Meteo API (free, no API key required) for real weather data.

### Fonts
- **Primary**: Liberation Mono (monospace, cyberpunk look)
- **Fallback**: System fonts if custom fonts fail

### Update Frequency
- **Display refresh**: Every 60 seconds
- **Weather data**: Real-time from API
- **System stats**: Live monitoring

## 📁 File Structure

```
pidisplay/
├── ink.py                      # Main display script
├── requirements.txt            # Python dependencies
├── pidisplay.service          # Systemd service file
├── install_local.sh           # Waveshare library installer
├── use_system_cyberpunk.sh    # Font installer
├── setup_autostart.sh         # Auto-start setup
└── *.bat                      # Windows helper scripts
```

## 🛠️ Troubleshooting

### Display Not Working
```bash
# Check service status
sudo systemctl status pidisplay.service

# View logs
sudo journalctl -u pidisplay.service -f

# Restart service
sudo systemctl restart pidisplay.service
```

### Font Issues
```bash
# Check available fonts
fc-list | grep -i mono

# Reinstall fonts
./use_system_cyberpunk.sh
```

### Weather Not Loading
- Check internet connection
- Verify Open-Meteo API is accessible
- Check logs for API errors

## 🔄 Updating

```bash
# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart pidisplay.service
```

## 📊 System Requirements

- **OS**: Raspberry Pi OS (latest)
- **Python**: 3.7+
- **Memory**: 512MB+ RAM
- **Storage**: 100MB+ free space

## 🎨 Customization

### Change Fonts
Edit `ink.py` and modify the font loading section to use different fonts.

### Modify Display Layout
Edit the `draw_combined_screen()` function in `ink.py` to change the layout.

### Add New Features
The code is modular - add new functions and integrate them into the main display loop.

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check this README and code comments
- **Hardware**: Refer to Waveshare documentation

## 🎯 Features in Detail

### Real-time Monitoring
- **CPU Usage**: Live percentage monitoring
- **Memory Usage**: RAM utilization tracking
- **Disk Usage**: Storage space monitoring
- **Temperature**: CPU temperature in Fahrenheit

### Weather Integration
- **Location Detection**: Automatic via IP geolocation
- **3-Day Forecast**: High temperatures and conditions
- **Real Data**: No mock data, actual weather from Open-Meteo
- **Fallback**: System temperature if API fails

### Display Features
- **Partial Refresh**: Fast updates without full screen clear
- **Auto-restart**: Detects code changes and restarts
- **Error Handling**: Graceful fallbacks for all features
- **Logging**: Comprehensive logging for debugging

---

**Enjoy your cyberpunk Pi Display!** 🤖✨