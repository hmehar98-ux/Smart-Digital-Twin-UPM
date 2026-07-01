import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import QTimer

class TwinScene:

    def __init__(self, main_window):
        self.main_window = main_window

        # =================================
        # QT INTERACTOR
        # =================================
        self.interactor = QtInteractor()

        # =================================
        # BACKGROUND
        # =================================
        self.interactor.set_background("white")

        # =================================
        # FLOOR
        # =================================
        # =================================
# MAIN FLOOR
# =================================

        main_floor = pv.Box(
            bounds=(-8, 8, -6, 6, -0.1, 0)
        )

        self.interactor.add_mesh(
            main_floor,
         color="#d8d4cc",
            show_edges=True,
         edge_color="#bdbdbd",
         pickable=False
        )
        # =================================
# ENTRANCE FLOOR
# =================================

        entrance_floor = pv.Box(
         bounds=(-3, 8, -10, -6, -0.1, 0)
        )

        self.interactor.add_mesh(
         entrance_floor,
         color="#d8d4cc",
         show_edges=True,
         edge_color="#bdbdbd",
         pickable=False
        )
        # =================================
        # BACK WALL
        # =================================
        back_wall = pv.Box(
            bounds=(-8, 8, 6, 6.2, 0, 8)
        )

        self.interactor.add_mesh(
            back_wall,
            color="#f2f2f2",
            opacity =0.08,
            pickable=False
        )
        # =================================
# FRONT WALL
# =================================

        front_wall = pv.Box(
          bounds=(-8, 8, -10, -9.8, 0, 8)
        )

        self.interactor.add_mesh(
         front_wall,
         color="#f2f2f2",
         opacity=0.05,
         pickable=False,
         smooth_shading=True
        )
        # =================================
        # CUSTOM WALL
# =================================

        custom_wall = pv.Box(
            bounds=(-8, -3, -6.2, -6, 0, 8)
        )

        self.interactor.add_mesh(

         custom_wall,
         color="#f2f2f2",
            opacity=0.06,
         smooth_shading=True,
         pickable=False
        )
        # =================================
        # LEFT WALL
        # =================================
        # =================================
# LEFT WALL BACK SECTION
# =================================
        left_wall = pv.Box(
          bounds=(-8, -7.8, -10, 6, 0, 8)
        )

        self.interactor.add_mesh(
            left_wall,
         color="#f2f2f2",
         opacity=0.08,
         pickable=False
        )

        # =================================
        # RIGHT WALL
        # =================================
        right_wall = pv.Box(
            bounds=(7.8, 8, -10, 6, 0, 8)
        )

        self.interactor.add_mesh(
            right_wall,
            color="#f2f2f2",
            opacity = 0.08,
            pickable=False
        )
        # =================================
# ROOF
# =================================

        roof = pv.Box(
            bounds=(-8, 8, -10, 6, 8, 8.2)
        )

        self.interactor.add_mesh(
            roof,
         color="#f2f2f2",
          opacity=0.08,
          pickable=False
        )
        # =================================
# DOOR MODEL
# =================================

        door = pv.read(
            "assets/models/door/door.stl"
        )

# SCALE
        door.scale(
         [0.1, 0.1, 0.1],
         inplace=True
        )

# ROTATION
        door.rotate_z(
             90,
            inplace=True
        )

# POSITION
        door.translate(
         (-3.2, -7.9, 0),
         inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
         door,
         color= "white",
         smooth_shading=True,
         opacity = 0.04,
         pickable=False
        )
        # =================================
# PRECITECH MACHINE
# =================================
# =================================
# PRECITECH MACHINE
# =================================

        machine = pv.read(
         "assets/models/machine/machine.stl"
        )

# =================================
# SCALE
# =================================

        machine.scale(
            [0.025, 0.025, 0.025],
            inplace=True
        )

# =================================
# ROTATION
# =================================

        machine.rotate_x(
            90,
            inplace=True
        )

# =================================
# POSITION
# =================================

        machine.translate(
            (-1.5, 1, 1.3),
            inplace=True
        )

# =================================
# ADD MACHINE TO SCENE
# =================================

        self.machine_actor = self.interactor.add_mesh(
            machine,
            color="#e8e6df",
            smooth_shading=True,
            metallic=0.15,
            roughness=0.45,
            pickable=True,
            name = "machine"
        )

# =================================
# ENCLOSURE
# =================================

        enclosure = pv.read(
            "assets/models/machine/enclosure.stl"
        )

# =================================
# SCALE
# =================================

        enclosure.scale(
         [0.025, 0.025, 0.025],
            inplace=True
        )

# =================================
# ROTATION
# =================================

        enclosure.rotate_x(
            90,
            inplace=True
        )

# =================================
# POSITION
# =================================

        enclosure.translate(
         ( -1.5,1 , 1.3),
            inplace=True
        )

# =================================
# ADD ENCLOSURE TO SCENE
# =================================

        self.enclosure_actor = self.interactor.add_mesh(
            enclosure,
            color="#85cdee",
            opacity=0.15,
            smooth_shading=True,
            metallic=0.05,
            roughness=0.1,
            pickable=False
        )
        # =================================
# COMPRESSOR
# =================================

        compressor = pv.read(
         "assets/models/machine/compressor.stl"
        )

# =================================
# SCALE
# =================================

        compressor.scale(
            [0.025, 0.025, 0.025],
         inplace=True
        )

# =================================
# ROTATION
# =================================

        compressor.rotate_x(
            90,
         inplace=True
        )

# OPTIONAL
# compressor.rotate_z(90, inplace=True)

# =================================
# POSITION
# =================================

        compressor.translate(
         (-1.5, 1, 1.3),
         inplace=True
        )

# =================================
# ADD TO SCENE
# =================================

        self.compressor_actor = self.interactor.add_mesh(
          compressor,
         color="#2f343a",
            smooth_shading=True,
          metallic=0.25,
          roughness=0.5,
         pickable=True
        )   
        # =================================
        # # MACHINE BASE
        # # =================================
        # machine_base = pv.Box(
        #     bounds=(-2.5, 2.5, -1.5, 1.5, 0, 1)
        # )

        # self.interactor.add_mesh(
        #     machine_base,
        #     color="lightgray"
        # )
        # self.interactor.enable_lightkit()

        # # =================================
        # # MACHINE BODY
        # # =================================
        # machine_body = pv.Box(
        #     bounds=(-2, 2, -1, 1, 1, 2.8)
        # )

        # self.machine_actor = self.interactor.add_mesh(
        #     machine_body,
        #     color="white",
        #     pickable=True
        # )
        # self.interactor.enable_lightkit()
        # =================================
        # SPINDLE
        # =================================
       
        # =================================
        # CHILLER
        # =================================
       # =================================
# CHILLER MODEL
# =================================

        chiller = pv.read(
        "assets/models/chiller/chiller.stl"
        )

# SCALE
        chiller.scale(
         [1, 1, 1],
         inplace=True
        )

# ROTATION
        chiller.rotate_y(
         180,
         inplace=True
        )
        chiller.rotate_x(
         180,
         inplace=True
        )
        chiller.rotate_z(
         90,
         inplace=True
        )


# POSITION
        chiller.translate(
         (4.0, 4.7, 0),
         inplace=True
        )
        

# ADD TO SCENE
        self.chiller_actor = self.interactor.add_mesh(
            chiller,
         color="#20c2e3",
            smooth_shading=True,
         metallic=0.3,
            roughness=0.5,
            pickable=True
        )
        self.interactor.enable_lightkit()
        # =================================
# CHILLER GLB MODEL
# =================================

#         chiller = pv.read(
#          "assets/models/chiller/chiller.glb"
#         )

# # SCALE
#         chiller.scale(
#          [1, 1, 1],
#          inplace=True
#         )

# # ROTATION
#         chiller.rotate_x(
#          90,
#          inplace=True
#         )
#         chiller.rotate_z(
#          90,
#          inplace=True
#         )

# # POSITION
#         chiller.translate(
#          (4.5, 1.5, 0),
#             inplace=True
#         )

# # ADD TO SCENE
#         self.chiller_actor = self.interactor.add_mesh(
#             chiller,
#             smooth_shading=True,
#             pickable=True
#         )
        # =================================
        # UPS
        # =================================
       # =================================
# UPS MODEL
# =================================

        ups = pv.read(
            "assets/models/ups/ups.stl"
        )

# SCALE
        ups.scale(
         [2, 2, 1],
         inplace=True
        )

# # ROTATION
#         ups.rotate_x(
#             90,
#          inplace=True
#         )

# POSITION
        ups.translate(
         (-6, 4.5, 1.3),
         inplace=True
        )

# ADD TO SCENE
        self.ups_actor = self.interactor.add_mesh(

         ups,

                name="ups",

         color="#444444",

                smooth_shading=True,

                metallic=0.6,

         roughness=0.4,
         pickable = True
        )
        self.interactor.enable_lightkit()
        # =================================
        # DEHUMIDIFIER
       
        # =================================
# DEHUMIDIFIER MODEL
# =================================

        dehumidifier = pv.read(
         "assets/models/dehumidifier/dehumidifier.stl"
        )

# SCALE
        dehumidifier.scale(
         [1, 1, 1],
          inplace=True
        )

# ROTATION
        dehumidifier.rotate_x(
         180,
            inplace=True
        )
        dehumidifier.rotate_y(
         180,
            inplace=True
        )
        dehumidifier.rotate_z(
         90,
            inplace=True
        )


# POSITION
        dehumidifier.translate(
         (6.5, 4.5, 0),
         inplace=True
        )

# ADD TO SCENE
        self.dehumidifier_actor = self.interactor.add_mesh(
         dehumidifier,
         color="#90a4ae",
         smooth_shading=True,
         metallic=0.2,
         roughness=0.5,
         pickable=True,
         name = "dehumidifier"
        )
        self.interactor.enable_lightkit()

        # =================================
        # COMPRESSOR
        # =================================
        # compressor = pv.Cylinder(
        #     center=(0, -2.2, 0.7),
        #     direction=(1, 0, 0),
        #     radius=0.5,
        #     height=2
        # )

        # self.interactor.add_mesh(
        #     compressor,
        #     smooth_shading=True,
        #     color="orange"
        # )
        # self.interactor.enable_lightkit()
        # =================================
        # LABELS
        # =================================
        self.machine_label_pos = [1.1, 1, 3.1]

        self.machine_label_actor = self.interactor.add_point_labels(

                [self.machine_label_pos],

                ["Ultra-Precision machine"],

         font_size=10,

         text_color="#f5f5f5",

         fill_shape=True,

         shape_color="#37474f",

         margin=8,

         point_size=0,

         always_visible=True

        
        )
        
        self.interactor.add_point_labels(
            [[2.8, 4.0, 2.0]],
            ["CHILLER"],
            font_size=10,

         text_color="#f5f5f5",

         fill_shape=True,

         shape_color="#37474f",

         margin=8,

         point_size=0,

         always_visible=True

        )
        
        self.interactor.add_point_labels(
            [[-5.2, 3.0, 3.5]],
            ["UPS"],
            font_size=10,

         text_color="#f5f5f5",

         fill_shape=True,

         shape_color="#37474f",

         margin=8,

         point_size=0,

         always_visible=True

        )
        # =================================
# LAB ENVIRONMENT LABEL
# =================================

       

        self.interactor.add_point_labels(
            [[5.5, 5.0, 3.5]],
            ["DEHUMIDIFIER"],
          font_size=10,

         text_color="#f5f5f5",

         fill_shape=True,

         shape_color="#37474f",

         margin=8,

         point_size=0,

         always_visible=True

        )

        self.interactor.add_point_labels(
            [[0.0, 0.25, 0]],
            ["COMPRESSOR"],
           font_size=10,

         text_color="#f5f5f5",

         fill_shape=True,

         shape_color="#37474f",

         margin=8,

         point_size=0,

         always_visible=True

        
        )
        monitor = pv.read(
            "assets/models/monitor/monitor.stl"
        )

# SCALE
        monitor.scale(
         [2, 2  , 2],
         inplace=True
        )

# ROTATE
        # monitor.rotate_x(90, inplace=True)

# POSITION IN ROOM CORNER
        monitor.translate(
        (-7, -4.7, 0),
        inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
            monitor,
         smooth_shading=True,
         color= "white",
         
         specular=1.0
        )
        self.interactor.enable_lightkit()   
        # =================================
        #2nd monitor
        monitor = pv.read(
            "assets/models/monitor/monitor.stl"
        )

# SCALE
        monitor.scale(
         [2, 2  , 2],
         inplace=True
        )

# ROTATE
        # monitor.rotate_x(90, inplace=True)
        monitor.rotate_z(
         180,
            inplace=True
        )

# POSITION IN ROOM CORNER
        monitor.translate(
        (7.2,-1,0),
        inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
            monitor,
         smooth_shading=True,
         color= "white",
         
         specular=1.0
        )
        self.interactor.enable_lightkit()
        #3rd monitor
        monitor = pv.read(
            "assets/models/monitor/monitor.stl"
        )

# SCALE
        monitor.scale(
         [2, 2  , 2],
         inplace=True
        )

# ROTATE
        # monitor.rotate_x(90, inplace=True)
        monitor.rotate_z(
         180,
            inplace=True
        )

# POSITION IN ROOM CORNER
        monitor.translate(
        (7.2, -4,0),
        inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
            monitor,
         smooth_shading=True,
         color= "white",
         
         specular=1.0
        )
        self.interactor.enable_lightkit()
# FRIDGE / CHILLER MODEL
# =================================

        fridge = pv.read(
         "assets/models/ref/ref.obj"
        )

# SCALE
        fridge.scale(
          [4, 4, 4],
          inplace=True
        )

# ROTATION
        fridge.rotate_x(
          90,
            inplace=True
        )
        fridge.rotate_z(
          90,
            inplace=True
        )

# POSITION
        fridge.translate(
         (-7, -2.5, 0),
         inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
            fridge,
            smooth_shading=True,
            color= "black",
            opacity = 0.5,
            specular=1.0,
            
        )
        self.interactor.enable_lightkit()
        # =================================
# AIR CONDITIONER MODEL
# =================================

        ac = pv.read(
            "assets/models/ac/ac.stl"
        )

        # SCALE
        ac.scale(
         [5, 5, 5],
         inplace=True
        )

# ROTATION
        
# POSITION
        ac.translate(
         (-5, 2.3, 7),
         inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
         ac,
         color="white",
         smooth_shading=True
        )
        # AIR CONDITIONER MODEL
# =================================

        ac = pv.read(
            "assets/models/ac/ac.stl"
        )

        # SCALE
        ac.scale(
         [5, 5, 5],
         inplace=True
        )

# ROTATION
        
# POSITION
        ac.translate(
         (5, 2.3, 7),
         inplace=True
        )

# ADD TO SCENE
        self.interactor.add_mesh(
         ac,
         color="white",
         smooth_shading=True
        )

        # =================================
        # CAMERA
        # =================================
        self.default_camera_position = [

                 (14, -14, 9),

                (0, 0, 2),

                (0, 0, 1)
        ]

        self.interactor.camera_position = (
                self.default_camera_position
        )

        # =================================
        # AXES
        # =================================
        # =================================
# INTERACTION STYLE
# =================================

        self.interactor.enable_trackball_style()
        self.interactor.show_axes()
       

        self.interactor.reset_camera()
        self.camera_timer = QTimer()

        self.camera_timer.timeout.connect(
                 self.animate_camera
        )

        self.animation_step = 0

        self.start_camera_position = None

        self.target_camera_position = None
        
        self.last_click_time = 0

        self.interactor.enable_mesh_picking(
                callback=self.on_mesh_click,
         use_actor=True,
          left_clicking=True,
         show=False,
          show_message=False
        )
    
    def update_machine_label(

                self,

                rpm,

           temperature,

         humidity

     ):

        self.interactor.remove_actor(
                self.machine_label_actor
        )

        self.machine_label_actor = self.interactor.add_point_labels(

                [self.machine_label_pos],

                [[
                f"PRECITECH\n"
                f"RPM : {rpm}\n"
                f"T : {temperature}°C\n"
                f"H : {humidity}%"
                ]],

                font_size=10,

                text_color="#f5f5f5",

                fill_shape=True,

                shape_color="#37474f",

                margin=8,

                point_size=0,

                always_visible=True

    )
    def on_mesh_click(self, actor):

        import time

        current_time = time.time()

        if not hasattr(self, "last_click_time"):

                self.last_click_time = 0

    # ==========================
    # MACHINE
    # ==========================

        if actor == self.machine_actor:

                if current_time - self.last_click_time < 0.4:

                        if self.main_window.dashboard.isVisible():

                                self.main_window.toggle_dashboard()

                        else:

                                self.move_camera_smooth([

                                (5, -5, 5),

                                (-1.5, 1, 1.5),

                                (0, 0, 1)

                                ])

                                self.main_window.ups_dashboard.hide()

                                self.main_window.env_dashboard.hide()

                                self.main_window.show_machine_dashboard()

    # ==========================
    # UPS
    # ==========================

        if actor == self.ups_actor:

                if current_time - self.last_click_time < 0.4:

                         if self.main_window.ups_dashboard.isVisible():

                                self.main_window.toggle_ups_dashboard()

                         else:

                                self.move_camera_smooth([

                                (-4, 1, 6),

                                (-6, 4.5, 1.3),

                                (0, 1, 1)

                                ])

                                self.main_window.dashboard.hide()

                                self.main_window.env_dashboard.hide()

                                self.main_window.toggle_ups_dashboard()
        if actor == self.dehumidifier_actor:
              if current_time - self.last_click_time < 0.4:
                        if self.main_window.dehum_dashboard.isVisible():
                              self.main_window.toggle_dehum_dashboard()
                        else:
                                self.move_camera_smooth([
                                      (4,1,6),
                                      (5,4.5,1.3),
                                      (0,1,1)
                                ])
                                self.main_window.dashboard.hide()
                                self.main_window.env_dashboard.hide()
                                self.main_window.ups_dashboard.hide()
                                self.main_window.toggle_dehum_dashboard()
    # ======    ====================
    # UPDATE CLICK TIME
    # ==========================

        self.last_click_time = current_time
        
    def move_camera_smooth(self, target_position):

        current = self.interactor.camera_position

        self.start_camera_position = [

                tuple(current[0]),

                tuple(current[1]),

                tuple(current[2])
        ]

        self.target_camera_position = target_position

        self.animation_step = 0

        self.camera_timer.start(16)
    def animate_camera(self):

        t = self.animation_step / 60

        if t >= 1:

         self.interactor.camera_position = (
                self.target_camera_position
         )

         self.camera_timer.stop()

         return

        start = self.start_camera_position
        end = self.target_camera_position

        interpolated = []

        for start_point, end_point in zip(start, end):

                interpolated_point = (

                        float(
                         start_point[0]
                                 +
                                (end_point[0] - start_point[0]) * t
                        ),

                        float(
                                start_point[1]
                                +
                                (end_point[1] - start_point[1]) * t
                         ),

                        float(
                         start_point[2]
                                +
                                (end_point[2] - start_point[2]) * t
                        )
                 )

                interpolated.append(interpolated_point)

        self.interactor.camera_position = tuple(
                interpolated
        )

        self.animation_step += 1