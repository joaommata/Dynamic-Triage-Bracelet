Here's your formatted README with proper Markdown structure and emojis for better readability:  

---

# 🚑 Dynamic Triage Bracelet  

## 📝 Description  
The **Dynamic Triage Bracelet** is an innovative healthcare solution that combines wearable technology with real-time patient monitoring. This system helps medical professionals efficiently manage patient care in emergency and hospital settings by providing continuous vital sign monitoring and dynamic triage status updates through a smart bracelet and a comprehensive dashboard interface.  

## 🛠 Tech Stack  
- 🔧 **Backend:** Python  
- 🎨 **Frontend:** Streamlit  
- 📊 **Data Visualization:** Plotly, Pandas  
- 🔌 **Hardware Communication:** PySerial  
- 🖥️ **Microcontroller:** Arduino (for bracelet control)  
- 📉 **Data Processing:** NumPy  

## ✨ Features  
✅ **Real-time Patient Monitoring** – Tracks vital signs like heart rate, temperature, and PPG data  
🎨 **Dynamic Triage Classification** – Color-coded patient status (🟢 Green, 🟡 Yellow, 🟠 Orange, ⚫ Gray) for quick assessment  
📊 **Interactive Dashboard** – Provides an overview of all patients with detailed individual monitoring  
📈 **Time Series Visualization** – Displays trends of vital signs over time  
🔒 **Secure Authentication** – Doctor login system with role-based access  
💡 **LED Bracelet Control** – Remote control of patient bracelet color indicators  
🚑 **Patient Prioritization** – Visual indicators to help medical staff prioritize care  

## ⚙️ Installation Steps  

### 🔹 Prerequisites  
Ensure you have the following installed:  
- 🐍 Python 3.7+  
- 🛠️ Arduino IDE  
- 🔌 USB serial connection to Arduino  

### 📥 Setup Instructions  
Clone the repository:  
```bash
git clone https://github.com/joaommata/Dynamic-Triage-Bracelet.git
cd Dynamic-Triage-Bracelet
```

Create and activate a virtual environment:  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install required dependencies:  
```bash
pip install -r requirements.txt
```

Upload the Arduino sketch to your microcontroller:  
1. Open the **Arduino IDE**  
2. Load the sketch from the `arduino/` directory  
3. Select your board and port  
4. Upload the sketch  

Prepare sample data:  
- Ensure `sensor_data.csv` is in the project root directory  

## 🚀 Usage Instructions  

### 1️⃣ Connect the Arduino to your computer via USB  
### 2️⃣ Update the serial port in `app.py`:  
```python
PORT = '/dev/tty.usbserial-A10LUUR2'  # Change to match your system
```
### 3️⃣ Run the Streamlit application:  
```bash
streamlit run app.py
```
### 4️⃣ Access the dashboard:  
- Open your web browser and go to: **[http://localhost:8501](http://localhost:8501)**  
- Login with one of the following credentials:  
  - 👤 **Username:** `admin` | **Password:** `password123`  
  - 👤 **Username:** `johndoe` | **Password:** `doctor456`  
  - 👤 **Username:** `janesmit` | **Password:** `nurse789`  

### 🏥 Using the Dashboard:  
- 📌 View all patients in the overview screen  
- 🩺 Select a patient to view detailed information  
- 🎨 Set the triage color for a patient using the dropdown menu  
- 📊 Monitor real-time vital signs  

## ⚙️ Configuration  

### 🔧 Environment Variables  
No environment variables are required, but you may need to adjust:  
- **Serial port configuration** in `app.py`  
- **Baud rate** (default: `9600`)  

### 🔌 Hardware Configuration  
- The bracelet requires an **Arduino-compatible microcontroller**  
- An **LED strip** compatible with the Arduino code  
- **Sensors** for temperature and PPG measurements  

## 🤝 Contributing  
Contributions are welcome! Follow these steps:  
1. **Fork the repository**  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```  
3. Commit your changes:  
   ```bash
   git commit -m 'Add some feature'
   ```  
4. Push to the branch:  
   ```bash
   git push origin feature/your-feature-name
   ```  
5. Open a **Pull Request**  

## 📜 License  
This project is licensed under the **MIT License** – see the `LICENSE` file for details.  

## 👤 Author  
**Ana Silva, Catarina Finuras, João Mata e Tomás Serra - Técnico Lisboa **  

## 🙌 Acknowledgments  
- This project was developed as part of a **healthcare innovation initiative**  
- Special thanks to all **healthcare professionals** who provided insights and feedback  

---

This README is now structured, engaging, and professional while maintaining readability. Let me know if you'd like further refinements! 🚀
