from motor import *
from mdv2 import *
from drivebase import *
from servo import *
from ble import *
from gamepad import *
from mpu6050 import MPU6050
from angle_sensor import AngleSensor
from abutton import *
from pins import *

async def on_cmd_BTN_L1():
  await servo3.run_angle(angle=0, speed=150)

async def on_cmd_BTN_THUMBR():
  motor5.brake()

async def on_cmd_BTN_L2():
  await servo3.run_angle(angle=90, speed=150)

async def on_abutton_BOOT_pressed():
  robot.mode_auto = True
  robot.speed(60, min_speed=40)
  motor5.run((-100))
  await asleep_ms(1000)
  await robot.forward_for(20, unit=CM, then=STOP)
  await asleep_ms(1000)
  await robot.turn_left_for(90, unit=DEGREE, then=STOP)
  await asleep_ms(1000)
  await robot.forward_for(100, unit=CM, then=STOP)
  await asleep_ms(1000)
  motor5.stop()
  robot.speed(95, min_speed=60)
  robot.mode_auto = False

async def on_abutton_D3_double_pressed():
  motor5.brake()
  robot.mode_auto = False

async def on_abutton_D3_pressed():
  robot.mode_auto = True
  robot.speed(60, min_speed=40)
  await asleep_ms(400)
  await robot.forward_for(15, unit=CM, then=STOP)
  await asleep_ms(500)
  await robot.turn_right_for(2.7, unit=DEGREE, then=STOP)
  await asleep_ms(500)
  await robot.forward_for(11, unit=CM, then=STOP)
  motor5.run((-100))
  await asleep_ms(500)
  await robot.forward_for(24, unit=CM, then=STOP)
  await asleep_ms(500)
  motor5.stop()
  robot.speed(95, min_speed=60)
  robot.mode_auto = False

async def on_abutton_D4_pressed():
  robot.mode_auto = True
  robot.speed(60, min_speed=40)
  await asleep_ms(200)
  await robot.forward_for(15, unit=CM, then=STOP)
  await asleep_ms(500)
  await robot.turn_left_for(2.7, unit=DEGREE, then=STOP)
  await asleep_ms(500)
  await robot.forward_for(11, unit=CM, then=STOP)
  motor5.run((-100))
  await asleep_ms(500)
  await robot.forward_for(24, unit=CM, then=STOP)
  await asleep_ms(500)
  motor5.stop()
  robot.speed(95, min_speed=60)
  robot.mode_auto = False

md_v2 = MotorDriverV2()
motor_fl = DCMotor(md_v2, M2, reversed=True)  # Trái Trước (M2)
motor_fr = DCMotor(md_v2, M1, reversed=True)  # Phải Trước (M1)
motor_rl = DCMotor(md_v2, E1, reversed=True)  # Trái Sau (E1)
motor_rr = DCMotor(md_v2, E2, reversed=True)  # Phải Sau (E2)
# Biến tương thích ngược
motor1 = motor_fl
motor2 = motor_fr
motor3 = motor_rl
motor4 = motor_rr
robot = DriveBase(MODE_MECANUM, m1=motor_fl, m2=motor_fr, m3=motor_rl, m4=motor_rr)
servo1 = Servo(md_v2, S1, 180)
servo2 = Servo(md_v2, S2, 180)
motor5 = DCMotor(md_v2, M3, reversed=True)
gamepad = Gamepad()
try:
  imu = MPU6050(transposition=(2, 1, 0), scaling=(-1, -1, -1))
  angle_sensor = AngleSensor(imu)
except Exception as e:
  print('[WARN] Khong cam bien goc MPU6050:', e)
  imu = None
  angle_sensor = None
servo3 = Servo(md_v2, S3, 180)
servo4 = Servo(md_v2, S4, 180)
btn_BOOT= aButton(BOOT_PIN)
btn_D3= aButton(D3_PIN)
btn_D4= aButton(D4_PIN)
led_D13 = Pins(D13_PIN)

def deinit():
  robot.stop()
  btn_BOOT.deinit()
  btn_D3.deinit()
  btn_D4.deinit()

import yolo_uno
yolo_uno.deinit = deinit

async def task_q_f_n_P():
  while True:
    await asleep_ms(75)
    if gamepad.data[BTN_TRIANGLE] == 1:
      motor5.run(100)
    elif gamepad.data[BTN_SQUARE] == 1:
      motor5.run((-100))
    if gamepad.data[BTN_R1] == 1:
      await servo1.run_angle(angle=85, speed=100)
      await servo2.run_angle(angle=60, speed=100)
    elif gamepad.data[BTN_R2] == 1:
      await servo1.run_angle(angle=125, speed=100)
      await servo2.run_angle(angle=0, speed=90)

async def task_z_e_u_v():
  while True:
    await asleep_ms(75)
    if gamepad.data[BTN_CIRCLE] == 1:
      await servo4.run_angle(angle=70, speed=40)
    elif gamepad.data[BTN_CROSS] == 1:
      await servo4.run_angle(angle=58, speed=40)

async def task_v_p_r_e():
  while True:
    await asleep_ms(500)
    led_D13.toggle()

async def setup():

  print('App started')
  robot.on_teleop_command(BTN_L1, on_cmd_BTN_L1)
  robot.on_teleop_command(BTN_THUMBR, on_cmd_BTN_THUMBR)
  robot.on_teleop_command(BTN_L2, on_cmd_BTN_L2)
  neopix.show(0, hex_to_rgb('#ff0000'))
  motor_rl.set_encoder(rpm=350, ppr=11, gears=35)
  motor_rr.set_encoder(rpm=350, ppr=11, gears=35)
  robot.size(wheel=60, width=320)
  servo1.limit(min=0, max=180)
  servo2.limit(min=0, max=180)
  robot.speed(95, min_speed=60)
  create_task(ble.wait_for_msg())
  create_task(gamepad.run())
  create_task(robot.run_teleop(gamepad, accel_steps=8))
  if angle_sensor is not None:
    try:
      angle_sensor.calibrate(500)
      create_task(angle_sensor.run())
      robot.angle_sensor(angle_sensor)
      robot.use_gyro(True)
    except Exception as e:
      print('[WARN] Loi calibrate cam bien goc:', e)
      robot.use_gyro(False)
  else:
    robot.use_gyro(False)
  await servo1.run_angle(angle=125, speed=90)
  await servo2.run_angle(angle=0, speed=90)
  neopix.show(0, hex_to_rgb('#00ff00'))
  print((md_v2.battery()))
  servo3.limit(min=0, max=180)
  await servo3.run_angle(angle=0, speed=150)
  servo4.limit(min=0, max=180)
  await servo4.run_angle(angle=58, speed=90)

  btn_BOOT.pressed(on_abutton_BOOT_pressed)
  btn_D3.double_pressed(on_abutton_D3_double_pressed)
  btn_D3.pressed(on_abutton_D3_pressed)
  btn_D4.pressed(on_abutton_D4_pressed)
  create_task(task_q_f_n_P())
  create_task(task_z_e_u_v())
  create_task(task_v_p_r_e())

async def main():
  await setup()
  while True:
    await asleep_ms(100)

run_loop(main())
