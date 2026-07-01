from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QGridLayout,
    QSizePolicy
)

from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
from twin.scene import TwinScene
from datetime import datetime
import json
import paho.mqtt.client as mqtt
import ssl
import sqlite3
from supabase import create_client
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Ultra Precision Machining Lab Digital Twin"
        )

        self.resize(1600, 900)

        # =================================
        # CENTRAL WIDGET
        # =================================

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        # =================================
        # MAIN LAYOUT
        # =================================

        main_layout = QHBoxLayout()

        central_widget.setLayout(
            main_layout
        )

        # =================================
        # LEFT DASHBOARD PANEL
        # =================================

        self.dashboard = QFrame()

        self.dashboard.setFixedWidth(350)

        self.dashboard.setStyleSheet("""

         QFrame {

          background-color: rgba(8, 20, 40, 235);

            border-right: 1px solid rgba(255,255,255,0.08);

         border-radius: 18px;

         }

        """)
        dashboard_layout = QVBoxLayout()

        self.dashboard.setLayout(
            dashboard_layout
        )

        # TITLE
        self.dashboard_title = QLabel(
            "Precitech Nanoform Xug"
        )

        self.dashboard_title.setAlignment(
            Qt.AlignCenter
        )

        self.dashboard_title.setStyleSheet("""

            color: white;

            font-size: 15px;

            font-weight: bold;

          padding-top: 5px;

            padding-bottom: 5px;

        """)

        dashboard_layout.addWidget(
            self.dashboard_title
        )
        # =================================
# STATUS LABEL
# =================================

        self.status_label = QLabel(
        "● MACHINE RUNNING"
    )

        self.status_label.setAlignment(
         Qt.AlignCenter
        )

        self.status_label.setStyleSheet("""

         color: #00e676;

            font-size: 9px;

         font-weight: bold;

            padding-bottom: 5px;

        """)

        dashboard_layout.addWidget(
         self.status_label
        )

        # PARAMETERS
        self.rpm_label = QLabel(
            "🌀 RPM :--"
        )

        self.temp_label = QLabel(
            "🌡 TEMPERATURE: --°C"
        )

        self.humidity_label = QLabel(
            "💧 HUMIDITY:--%"
        )

        self.brightness_label = QLabel(
            "💡 BRIGHTNESS: -- lx"
        )

        labels = [
            self.rpm_label,
            self.temp_label,
            self.humidity_label,
            self.brightness_label
        ]

        # =================================
# TELEMETRY GRID
# =================================

        grid_layout = QGridLayout()

        grid_layout.setSpacing(10)

        dashboard_layout.addLayout(
        grid_layout
    )

        labels = [

            self.rpm_label,

         self.temp_label,

         self.humidity_label,

         self.brightness_label

        ]

        for label in labels:

         label.setFixedHeight(45)

         label.setStyleSheet("""

            background-color: rgba(255,255,255,0.05);

            border: 1px solid rgba(255,255,255,0.08);

            color: white;

            font-size: 9px;

            font-weight: bold;

            padding: 4px;

            border-radius: 6px;
          margin: 2px;

            min-height: 18px;
            max-height: 20px;
            min-width: 120px;

         """)

        grid_layout.addWidget(
            self.rpm_label,
         0, 0
        )

        grid_layout.addWidget(
            self.temp_label,
         0, 1
        )

        grid_layout.addWidget(
            self.humidity_label,
         1, 0
        )

        grid_layout.addWidget(
         self.brightness_label,
            1, 1
        )
        # =================================
# MACHINE CONDITION MONITORING
# =================================
        # =================================
# MACHINE CONDITION MONITORING
# =================================

        self.condition_title = QLabel("Machine Condition Monitoring")

        self.condition_title.setStyleSheet("""
            color:white;
            font-size:12px;
         font-weight:bold;
            padding-top:8px;
         padding-bottom:4px;
        """)

        dashboard_layout.addWidget(self.condition_title)


# ---------- Helper ----------

        def create_axis_row(name, color):

         row = QHBoxLayout()
         row.setSpacing(6)

         axis = QLabel(name)
         axis.setFixedWidth(20)
         axis.setAlignment(Qt.AlignCenter)
         axis.setStyleSheet(f"""
            color:{color};
            font-size:11px;
            font-weight:bold;
        """)

         plot = pg.PlotWidget()
         plot.setFixedHeight(85)
         plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

         plot.setBackground((15,23,42))
         plot.hideAxis("left")
         plot.hideAxis("bottom")
         plot.hideButtons()

         plot.setMouseEnabled(False, False)
         plot.setMenuEnabled(False)

# Auto-scale Y axis
         plot.enableAutoRange(axis='y', enable=True)
         plot.setClipToView(True)
         plot.setDownsampling(mode="peak")
         curve = plot.plot(
          pen=pg.mkPen(color, width=2)
         )

         rms = QLabel("RMS\n0.000")

         rms.setFixedWidth(42)

         rms.setAlignment(Qt.AlignCenter)

         rms.setStyleSheet("""
            color:white;
          font-size:9px;
          font-weight:bold;
         background-color: rgba(255,255,255,0.05);
         border:1px solid rgba(255,255,255,0.08);
            border-radius:8px;
         """)

         row.addWidget(axis)
         row.addWidget(plot, 1)
         row.addWidget(rms)

         dashboard_layout.addLayout(row)

         return plot, curve, rms


# ---------- X ----------

        self.ax_plot, self.ax_curve, self.ax_rms = create_axis_row(
            "X",
         "#00E5FF"
        )

# ---------- Y ----------

        self.ay_plot, self.ay_curve, self.ay_rms = create_axis_row(
            "Y",
         "#00FF7F"
        )

# ---------- Z ----------

        self.az_plot, self.az_curve, self.az_rms = create_axis_row(
         "Z",
         "#FFA726"
        )

        dashboard_layout.addStretch()
        # HIDE INITIALLY
        self.dashboard.hide()
        # =================================
# ENVIRONMENT DASHBOARD
# =================================

        self.env_dashboard = QFrame()

        self.env_dashboard.setFixedWidth(420)

        env_layout = QVBoxLayout()
        env_layout.setSpacing(20)
        self.env_dashboard.setLayout(
            env_layout
        )

        self.env_dashboard.setStyleSheet("""

            background-color: rgba(8,20,40,235);

         border-radius: 12px;

        """)

# TITLE

        self.env_title = QLabel(
             "LAB ENVIRONMENT"
        )

        self.env_title.setAlignment(
            Qt.AlignCenter
        )

        self.env_title.setStyleSheet("""

            color: white;

            font-size: 24px;

            font-weight: bold;

            padding: 15px;

        """)

        env_layout.addWidget(
            self.env_title
        )

# =================================
# TEMPERATURE GRAPH
# =================================

        axis = pg.DateAxisItem()

        self.temp_plot = pg.PlotWidget(
            axisItems={'bottom': axis}
        )

        self.temp_plot.setBackground(
            (15, 23, 42)
        )

        self.temp_plot.showGrid(
            x=True,
            y=True
        )

        self.temp_plot.setTitle(
            "Temperature",
            color="w"
        )
        self.temp_plot.getAxis("bottom").setTickSpacing(
            major=5,
             minor=1
        )

        self.temp_plot.getAxis("bottom").setHeight(
            50
        )
        env_layout.addWidget(
            self.temp_plot
        )

# =================================
# HUMIDITY GRAPH
# =================================

        axis = pg.DateAxisItem()

        self.humidity_plot = pg.PlotWidget(
            axisItems={'bottom': axis}
        )

        self.humidity_plot.setBackground(
            (15, 23, 42)
        )

        self.humidity_plot.showGrid(
         x=True,
            y=True
        )

        self.humidity_plot.setTitle(
            "Humidity ",
            color="w"
        )
        self.humidity_plot.getAxis("bottom").setTickSpacing(
            major=5,
             minor=1
        )
        self.humidity_plot.getAxis("bottom").setHeight(
            50
        )
        env_layout.addWidget(
            self.humidity_plot
        )

# =================================
# LIGHT GRAPH
# =================================

        axis = pg.DateAxisItem()

        self.light_plot = pg.PlotWidget(
            axisItems={'bottom': axis}
        )

        self.light_plot.setBackground(
         (15, 23, 42)
        )

        self.light_plot.showGrid(
            x=True,
             y=True
        )

        self.light_plot.setTitle(
            "Luminescence",
            color="w"
        )
        self.light_plot.getAxis("bottom").setTickSpacing(
            major=5,
             minor=1
        )

        self.light_plot.getAxis("bottom").setHeight(
            50
        )
        env_layout.addWidget(
            self.light_plot
        )

# =================================
# CURVES
# =================================

        self.temp_curve = self.temp_plot.plot(
            pen=pg.mkPen('#4dd0e1', width=1.2)
        )

        self.humidity_curve = self.humidity_plot.plot(
            pen=pg.mkPen('#81c784', width=1.2)
        )

        self.light_curve = self.light_plot.plot(
            pen=pg.mkPen('#ffd54f', width=1.2)
        )

# =================================
# DATA STORAGE
# =================================

        self.time_data = []
        

        self.temp_data = []

        self.humidity_data = []

        self.light_data = []
        self.ax_data = []
        self.ay_data = []
        self.az_data = []
        
        self.dehum_temp = 0
        self.dehum_humidity = 0
        self.lab_temp = 0
        self.lab_humidity = 0
        self.lab_lux = 0
        # =================================
# LIVE UPDATE TIMER
# =================================

        self.env_timer = QTimer()

        self.env_timer.timeout.connect(
        self.update_environment_graphs
        )

        self.env_timer.start(300000)

        self.env_dashboard.hide()
        # =================================
# UPS DASHBOARD
# =================================

        self.ups_dashboard = QFrame()

        self.ups_dashboard.setFixedWidth(350)

        self.ups_dashboard.setStyleSheet("""

            background-color: rgba(8,20,40,235);

            border-radius: 12px;

        """)

        ups_layout = QVBoxLayout()

        self.ups_dashboard.setLayout(
         ups_layout
        )

# TITLE

        self.ups_title = QLabel(
            "UPS MONITORING"
        )

        self.ups_title.setAlignment(
         Qt.AlignCenter
        )

        self.ups_title.setStyleSheet("""

            color: white;

            font-size: 24px;

            font-weight: bold;

            padding: 15px;

        """)

        ups_layout.addWidget(
             self.ups_title
        )

# STATUS

        self.ups_status = QLabel(
         "🟢 NORMAL OPERATION"
        )

        self.ups_status.setAlignment(
            Qt.AlignCenter
        )

        self.ups_status.setStyleSheet("""

            color: #00e676;

         font-size: 14px;

            font-weight: bold;

            padding-bottom: 10px;

        """)

        ups_layout.addWidget(
            self.ups_status
        )

# =================================
# UPS CARDS
# =================================

        self.voltage_label = QLabel(
         "⚡ VOLTAGE\n230 V"
        )

        self.current_label = QLabel(
            "🔌 CURRENT\n3.2 A"
        )

        self.power_label = QLabel(
            "⚙ POWER\n720 W"
        )

        self.frequency_label = QLabel(
            "📡 FREQUENCY\n50 Hz"
        )

        ups_labels = [

            self.voltage_label,

            self.current_label,

            self.power_label,

            self.frequency_label
        ]

        ups_grid = QGridLayout()

        ups_grid.setSpacing(10)

        ups_layout.addLayout(
             ups_grid
        )

        for label in ups_labels:

            label.setFixedHeight(60)

            label.setStyleSheet("""

                background-color: rgba(255,255,255,0.05);

                border: 1px solid rgba(255,255,255,0.08);

                color: white;

                font-size: 11px;

                font-weight: bold;

                padding: 8px;

                border-radius: 8px;

            """)

        ups_grid.addWidget(
            self.voltage_label,
            0, 0
        )

        ups_grid.addWidget(
            self.current_label,
            0, 1
        )

        ups_grid.addWidget(
            self.power_label,
             1, 0
        )

        ups_grid.addWidget(
            self.frequency_label,
            1, 1
        )

# =================================
# VOLTAGE GRAPH
# =================================

        self.ups_plot = pg.PlotWidget()

        self.ups_plot.setBackground(
            (15, 23, 42)
        )

        self.ups_plot.showGrid(
         x=True,
         y=True
        )

        self.ups_plot.setTitle(
            "UPS Voltage",
            color="w"
        )   
        self.ups_plot.getAxis("bottom").setTickSpacing(
            major=5,
            minor=1
        )

        self.ups_plot.getAxis("bottom").setHeight(
            50
        )
        ups_layout.addWidget(
            self.ups_plot
        )

        self.ups_curve = self.ups_plot.plot(
            pen=pg.mkPen('#4dd0e1', width=1.5)
        )
# =================================
# CURRENT GRAPH
# =================================

        self.current_plot = pg.PlotWidget()

        self.current_plot.setBackground(
         (15, 23, 42)
        )

        self.current_plot.showGrid(
         x=True,
         y=True
        )

        self.current_plot.setTitle(
            "UPS Current",
            color="w"
        )
        self.current_plot.getAxis("bottom").setTickSpacing(
            major=5,
         minor=1
        )

        self.current_plot.getAxis("bottom").setHeight(
            50
        )
        ups_layout.addWidget(
            self.current_plot
        )

        self.current_curve = self.current_plot.plot(
            pen=pg.mkPen('#ffb74d', width=1.5)
        )
# =================================
# UPS DATA
# =================================

        self.ups_voltage_data = []
        self.ups_current_data = []

        self.ups_time_data = []
        self.ups_timestamp_data = []
        self.ups_counter = 0
        #dehumidifier data
        self.dehum_time_data = []
        self.dehum_humidity_data = []

        
# =================================
# UPS TIMER
# =================================

        self.ups_timer = QTimer()

        self.ups_timer.timeout.connect(
             self.update_ups_dashboard
        )

        self.ups_timer.start(3000)

        self.ups_dashboard.hide()
        # =================================
#dehumidifier timer
        self.dehum_timer = QTimer()

        self.dehum_timer.timeout.connect(
         self.update_dehum_dashboard
        )

        self.dehum_timer.start(
            60000
        )
# DEHUMIDIFIER DASHBOARD
# =================================

        self.dehum_dashboard = QFrame()

        self.dehum_dashboard.setFixedWidth(300)
        self.dehum_dashboard.setFixedHeight(
            450
        )
        dehum_layout = QVBoxLayout()

        self.dehum_dashboard.setLayout(
            dehum_layout
        )

        self.dehum_dashboard.setStyleSheet("""

            background-color: rgba(8,20,40,235);

            border-radius: 12px;

        """)
        self.dehum_title = QLabel(
            "DEHUMIDIFIER"
        )

        self.dehum_title.setAlignment(
            Qt.AlignCenter
        )

        self.dehum_title.setStyleSheet("""

            color:white;
            font-size:24px;
            font-weight:bold;
            padding:15px;

        """)

        dehum_layout.addWidget(
            self.dehum_title
        )
        self.dehum_humidity_label = QLabel(
            "💧 HUMIDITY\n45%"
        )

        self.dehum_humidity_label.setAlignment(
            Qt.AlignCenter
        )

        self.dehum_humidity_label.setFixedHeight(
            50
        )

        self.dehum_humidity_label.setStyleSheet("""

            background-color: rgba(255,255,255,0.05);

            border:1px solid rgba(255,255,255,0.08);

            color:#22c55e;

            font-size:12px;

            font-weight:bold;

            border-radius:6px;

        """)

        dehum_layout.addWidget(
            self.dehum_humidity_label
        )   
        axis = pg.DateAxisItem()

        self.dehum_plot = pg.PlotWidget(
            axisItems={'bottom': axis}
        )
        self.dehum_plot.setFixedHeight(300)
        self.dehum_plot.setBackground(
            (15,23,42)
        )

        self.dehum_plot.showGrid(
         x=True,
            y=True
        )

        self.dehum_plot.setTitle(
         "Humidity vs Time",
         color="w"
        )
        self.dehum_plot.getAxis("bottom").setTickSpacing(
            major=300,
            minor=60
        )

        dehum_layout.addWidget(
            self.dehum_plot
        )

        self.dehum_curve = self.dehum_plot.plot(
            pen=pg.mkPen(
             '#81c784',
                width=1.5
            )
        )
       

        
        

        # =================================
        # 3D SCENE
        # =================================

        self.scene = TwinScene(self)

        # =================================
        # ADD TO LAYOUT
        # =================================

        main_layout.addWidget(
            self.dashboard
        )
        main_layout.addWidget(
        self.env_dashboard
        )
        main_layout.addWidget(
            self.ups_dashboard
        )
        
        main_layout.addWidget(
            self.scene.interactor
        )
        
        # =================================
        self.dehum_dashboard.setParent(
            self.scene.interactor
        )

        self.dehum_dashboard.setGeometry(
            20,     # x
            150,    # y
            300,    # width
            450     # height
        )

        self.dehum_dashboard.hide()
        # =================================
    # SYSTEM STATUS
# =================================
        # =================================
# HUD STATUS
# ==================

        # =================================
# SYSTEM STATUS CARD
# =================================

        self.system_panel = QFrame(self.scene.interactor)

        self.system_panel.setGeometry(1330, 10, 180, 105)

        self.system_panel.setStyleSheet("""
            QFrame{
            background-color: rgba(15,20,30,150);
            border:1px solid rgba(255,255,255,40);
            border-radius:10px;
        }
        """)

        layout = QVBoxLayout(self.system_panel)
        layout.setContentsMargins(10,8,10,8)
        layout.setSpacing(4)
        title = QLabel("SYSTEM STATUS")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            color:white;
         font-size:10px;
         font-weight:bold;
            background:transparent;
        """)

        layout.addWidget(title)
        self.mqtt_status = QLabel("● MQTT")

        self.mqtt_status.setStyleSheet("""
            color:#ef4444;
            font-size:9px;
         font-weight:bold;
         background:transparent;
        """)

        layout.addWidget(self.mqtt_status)
        self.supabase_status = QLabel("● Supabase")

        self.supabase_status.setStyleSheet("""
            color:#ef4444;
            font-size:9px;
         font-weight:bold;
            background:transparent;
        """)


        layout.addWidget(self.supabase_status)
        self.last_packet = QLabel("Last : --")

        self.last_packet.setStyleSheet("""
        color:white;
        font-size:9px;
        background:transparent;
        """)

        layout.addWidget(self.last_packet)
        self.system_panel.raise_()
        self.system_panel.show()

        self.last_packet_time = None
        
        self.mqtt_client = mqtt.Client(
         mqtt.CallbackAPIVersion.VERSION2
        )

        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.username_pw_set(
            os.getenv("MQTT_USERNAME"),
            os.getenv("MQTT_PASSWORD")
        )


        self.mqtt_client.tls_set(
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )

        self.mqtt_client.connect(
            os.getenv("MQTT_BROKER"),
            int(os.getenv("MQTT_PORT")),
            60
        )

        self.mqtt_client.loop_start()
        
        # =================================
        # =================================
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.supabase_status.setStyleSheet("""
            color:#22c55e;
            font-size:9px;
            font-weight:bold;
            background:transparent;
            border:none;
            """)
# SQLITE DATABASE
# =================================

        # self.conn = sqlite3.connect(
        #     "upmc_lab.db",
        #     check_same_thread=False
        # )

        # self.cursor = self.conn.cursor()

        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS sensor_data (

        #     id INTEGER PRIMARY KEY AUTOINCREMENT,

        #     timestamp TEXT,

        #     topic TEXT,

        #     temperature REAL,

        #     humidity REAL,

        #     lux REAL

        # )
        # """)

        # self.conn.commit()
# LAB ENVIRONMENT BUTTON
# =================================
# =================================
# LAB ENVIRONMENT BUTTON
# =================================

        self.lab_button = QPushButton(
            "UPMC\n────────\n🌡22°C   💧45%"
        )

        self.lab_button.setParent(
            self.scene.interactor
        )

        self.lab_button.raise_()

        self.lab_button.show()

# POSITION
        self.lab_button.setGeometry(
         690, 70, 120, 45
        )

        self.lab_button.setStyleSheet("""

        QPushButton {

         background-color: rgba(18,22,30,200);

         color: white;

            font-size: 10px;

            font-weight: bold;

            border-radius: 20px;

            border: 0px;

            padding: 2px;

        }

         QPushButton:hover {

            background-color: rgba(30,35,45,230);

        }

    """)
        self.lab_button.clicked.connect(
            self.toggle_environment_dashboard
        )
        self.load_dehumidifier_history()
        self.load_lab_history()
        self.update_dehum_dashboard(False)
    def on_mqtt_connect(
       
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties=None,
        
    ):
        
        self.mqtt_status.setStyleSheet("""
            color:#22c55e;
         font-size:9px;
            font-weight:bold;
            background:transparent;
            border:none;
        """)
        
        client.subscribe("upmc/lab/environment")
        client.subscribe(
        "upmc/dehumidifier/environment"
        )


    def on_mqtt_message(
     self,
     client,
     userdata,
        msg
    ):
        self.last_packet_time = datetime.now()

        self.last_packet.setText(
            "Last Packet : " +
         self.last_packet_time.strftime("%H:%M:%S")
        )
        print(msg.topic)
        print(msg.payload.decode())
        payload = json.loads(
            msg.payload.decode()
        )

        if msg.topic == "upmc/lab/environment":

         self.lab_temp = payload["temperature"]

         self.lab_humidity = payload["humidity"]

         self.lab_lux = payload["lux"]
         self.update_upmc_button(
          self.lab_temp,
          self.lab_humidity
        )

         timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        #  self.cursor.execute("""
        #  INSERT INTO sensor_data
        #  (
        #  timestamp,
        #     topic,
        #     temperature,
        #     humidity,
        #     lux
        #     )
        #  VALUES (?, ?, ?, ?, ?)
        #  """, (
        #     timestamp,
        #  msg.topic,
        #  self.lab_temp,
        #     self.lab_humidity,
        #     self.lab_lux
        #  ))

        #  self.conn.commit()

        elif msg.topic == "upmc/dehumidifier/environment":

         self.dehum_temp = payload["temperature"]

         self.dehum_humidity = payload["humidity"]

         timestamp = datetime.now().strftime(
         "%Y-%m-%d %H:%M:%S"
         )

        #  self.cursor.execute("""
        #  INSERT INTO sensor_data
        #     (
        #     timestamp,
        #     topic,
        #     temperature,
        #     humidity,
        #     lux
        #     )
        #  VALUES (?, ?, ?, ?, ?)
        #  """, (
        #  timestamp,
        #  msg.topic,
        #  self.dehum_temp,
        #  self.dehum_humidity,
        #  None
        #  ))

        # self.conn.commit()
        # print("Saved to SQLite")
        # print(
        #     f"Lab Temp={self.lab_temp}, "
        #     f"Lab Humidity={self.lab_humidity}, "
        #     f"Lux={self.lab_lux}"
        # )
       
    def toggle_dashboard(self):

        if self.dashboard.isVisible():

            self.dashboard.hide()
            self.scene.move_camera_smooth(
                self.scene.default_camera_position
            )
        else:

            self.show_machine_dashboard()
    def toggle_ups_dashboard(self):

        if self.ups_dashboard.isVisible():

            self.ups_dashboard.hide()

            self.scene.move_camera_smooth(
                self.scene.default_camera_position
            )

        else:

         self.ups_dashboard.show()
    # =================================
    # SHOW MACHINE DASHBOARD
    # =================================
    def toggle_environment_dashboard(self):

        if self.env_dashboard.isVisible():

            self.env_dashboard.hide()
            
        else:

         self.env_dashboard.show()
    def toggle_dehum_dashboard(self):

        if self.dehum_dashboard.isVisible():

            self.dehum_dashboard.hide()
            self.scene.move_camera_smooth(
                self.scene.default_camera_position
            )

        else:

         self.dehum_dashboard.show()
    def show_machine_dashboard(self):

        self.dashboard.show()
    def update_machine_data(

          self,

         rpm,

         temperature,

         humidity,

         brightness

         ):

        self.rpm_label.setText(
         f"🌀 RPM\n{rpm}"
        )

        self.temp_label.setText(
            f"🌡 TEMPERATURE\n{temperature}°C"
        )

        self.humidity_label.setText(
            f"💧 HUMIDITY\n{humidity}%"
        )

        self.brightness_label.setText(
         f"💡 BRIGHTNESS\n{brightness} lx"
        )
    def update_environment_graphs(self):

        

    # =================================
    # SIMULATED SENSOR VALUES
    # =================================

        temp = self.lab_temp

        humidity = self.lab_humidity

        light = self.lab_lux
        self.update_upmc_button(
            temp,
            humidity
        )
    # =================================
    # STORE DATA
    # =================================
        current_time = datetime.now()

        self.time_data.append(
            current_time.timestamp()
        )

        self.temp_data.append(temp)
        self.humidity_data.append(humidity)
        self.light_data.append(light)

       

    # =================================
    # LIMIT GRAPH SIZE
    # =================================

        if len(self.time_data) > 24:

            self.time_data.pop(0)
          

            self.temp_data.pop(0)

            self.humidity_data.pop(0)

            self.light_data.pop(0)

    # =================================
    # UPDATE CURVES
    # =================================

        self.temp_curve.setData(
         self.time_data,
            self.temp_data
        )

        self.humidity_curve.setData(
            self.time_data,
            self.humidity_data
        )

        self.light_curve.setData(
         self.time_data,
            self.light_data
        )
        
    def get_temperature(self):

            import random

            return 22 + random.uniform(-0.2, 0.2)


    def get_humidity(self):

            import random

            return 45 + random.uniform(-1, 1)


    def get_light(self):

            import random

            return 700 + random.uniform(-20, 20)
    def update_upmc_button(

        self,

        temperature,

        humidity

    ):

        self.lab_button.setText(

         f"UPMC\n────────\n"
            f"🌡{temperature:.1f}°C   "
         f"💧{humidity:.1f}%"

    )
    def update_ups_dashboard(self):

        import random

        voltage = 230 + random.uniform(-1, 1)

        current = 3 + random.uniform(-0.2, 0.2)

        power = voltage * current

        frequency = 50 + random.uniform(-0.05, 0.05)
        current_time = datetime.now()

        time_string = current_time.strftime("%H:%M:%S")
        self.voltage_label.setText(
            f"⚡ VOLTAGE\n{voltage:.1f} V"
        )

        self.current_label.setText(
            f"🔌 CURRENT\n{current:.1f} A"
        )

        self.power_label.setText(
            f"⚙ POWER\n{power:.0f} W"
        )

        self.frequency_label.setText(
            f"📡 FREQUENCY\n{frequency:.2f} Hz"
        )

        self.ups_voltage_data.append(
         voltage
        )
        self.ups_current_data.append(
            current
        )
        self.ups_counter += 1

        self.ups_time_data.append(
            self.ups_counter
        )
        self.ups_timestamp_data.append(
            time_string
        )
        if len(self.ups_voltage_data) > 30:

         self.ups_voltage_data.pop(0)
         self.ups_current_data.pop(0)
         self.ups_time_data.pop(0)
         self.ups_timestamp_data.pop(0)
        self.ups_curve.setData(
         self.ups_time_data,
            self.ups_voltage_data
        )
        self.current_curve.setData(
            self.ups_time_data,
            self.ups_current_data
        )
        ticks = []

        for i, timestamp in enumerate(
            self.ups_timestamp_data
        ):

         if i % 5 == 0:

             ticks.append(
                (
                self.ups_time_data[i],
                timestamp
                )
            )
       
        self.ups_plot.getAxis(
            "bottom"
        ).setTicks(
        [ticks]
        )

        self.current_plot.getAxis(
            "bottom"
        ).setTicks(
        [ticks]
        )
    def update_dehum_dashboard(self, append_new = True):
        humidity = self.dehum_humidity

        if append_new:

            self.dehum_humidity_data.append(humidity)

            current_time = datetime.now()

            self.dehum_time_data.append(
            current_time.timestamp()
         )

        if len(self.dehum_humidity_data) > 30:

            self.dehum_humidity_data.pop(0)

            self.dehum_time_data.pop(0)

        self.dehum_curve.setData(

            self.dehum_time_data,

            self.dehum_humidity_data

        )

        if humidity < 55:

            color = "#22c55e"

        elif humidity < 65:

            color = "#f59e0b"

        else:

         color = "#ef4444"

        self.dehum_humidity_label.setStyleSheet(f"""

         background-color: rgba(255,255,255,0.05);

         border:1px solid rgba(255,255,255,0.08);

            color:{color};

         font-size:12px;

            font-weight:bold;

            border-radius:6px;

         """)

        self.dehum_humidity_label.setText(

            f"💧 HUMIDITY\n\n{humidity:.1f}%"

         )  
    def load_dehumidifier_history(self):

        start_time = (
         datetime.now(timezone.utc)
         - timedelta(minutes=30)
        ).isoformat()

        response = (
            self.supabase.table("sensor_data")
            .select("*")
            .eq("topic", "upmc/dehumidifier/environment")
            .gte("created_at", start_time)
            .order("created_at")
            .execute()
        )

        rows = response.data

        self.dehum_time_data.clear()
        self.dehum_humidity_data.clear()

        for row in rows:

         timestamp = datetime.fromisoformat(
            row["created_at"].replace("Z", "+00:00")
            )

         self.dehum_time_data.append(
            timestamp.timestamp()
         )

         self.dehum_humidity_data.append(
            row["humidity"]
         )

        self.dehum_curve.setData(
         self.dehum_time_data,
         self.dehum_humidity_data
        )

        if rows:

         self.dehum_temp = rows[-1]["temperature"]
         self.dehum_humidity = rows[-1]["humidity"]

         self.update_dehum_dashboard(False)
    def load_lab_history(self):

        start_time = (
         datetime.now(timezone.utc)
            - timedelta(hours=2)
        ).isoformat()

        response = (
            self.supabase.table("sensor_data")
            .select("*")
            .eq("topic", "upmc/lab/environment")
            .gte("created_at", start_time)
            .order("created_at")
            .execute()
        )

        rows = response.data
        
        self.time_data.clear()
        self.temp_data.clear()
        self.humidity_data.clear()
        self.light_data.clear()

        for row in rows:
            print(row)
            timestamp = datetime.fromisoformat(
                row["created_at"].replace("Z", "+00:00")
            )

            self.time_data.append(
             timestamp.timestamp()
            )

            self.temp_data.append(
            row["temperature"]
            )

            self.humidity_data.append(
            row["humidity"]
            )

            self.light_data.append(
                row["lux"]
            )

        self.temp_curve.setData(
            self.time_data,
         self.temp_data
        )

        self.humidity_curve.setData(
            self.time_data,
         self.humidity_data
        )

        self.light_curve.setData(
            self.time_data,
            self.light_data
        )

        if rows:

            self.lab_temp = rows[-1]["temperature"]
            self.lab_humidity = rows[-1]["humidity"]
            self.lab_lux = rows[-1]["lux"]

            self.update_upmc_button(
            self.lab_temp,
            self.lab_humidity
            )
    