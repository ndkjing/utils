import numpy as np
import matplotlib.pyplot as plt
from ins_sig_gen import generate_signals
from ins_ekf import ins_ext_kfilter


# Config
imu_period = 0.01
accel_bias_std = 0.3
accel_w_std = 0.05
gyro_bias_std = np.deg2rad( 1.0 )
gyro_w_std = np.deg2rad( 0.1 )
imu_body_alpha0_std = np.deg2rad( 3 )
gnss_period = 1
gnss_speed_w_std = 0.3
gnss_dist_w_std = 5
# 速度变化
speed_changes = [
	[ +3, 10 ],
	[  0, 10 ],
	[ +4, 20 ],
	[ -2, 10 ],
	[  0, 30 ],
	[ +5, 10 ],
	[ -4, 20 ],
	[  0, 20 ],
	[ -4, 10 ],
	[ -2, 20 ]
]
angle_changes = [
	[ np.deg2rad( 0 ),    20 ],
	[ np.deg2rad( +45 ),  20 ],
	[ np.deg2rad( +30 ),  20 ],
	[ np.deg2rad( +60 ),  25 ],
	[ np.deg2rad( +10 ),  5 ],
	[ np.deg2rad( -20 ),  10 ],
	[ np.deg2rad( -140 ), 30 ],
	[ np.deg2rad( 0 ),    30 ]
]

# Generate INS signals
[ imu_time, imu_accel, imu_gyro, 
  gnss_time, gnss_speed, gnss_dist,
  real_accel_bias, real_gyro_bias, real_body_angles, 
  real_glob_accel, real_glob_speed, real_glob_speed_norm, real_glob_dist 
] = generate_signals( 
	speed_changes, angle_changes,
	imu_period, accel_bias_std, accel_w_std, gyro_bias_std, gyro_w_std,
	gnss_period, gnss_speed_w_std, gnss_dist_w_std
)

# Initial params estimation
real_body_alpha0 = real_body_angles[0].item( ( 0, 0 ) )
imu_body_alpha0 = real_body_alpha0 + np.random.normal( 0, imu_body_alpha0_std )
print('Real a0: ' + str( np.rad2deg( real_body_alpha0 ) ) + ', estimated a0: ' + str( np.rad2deg( imu_body_alpha0 ) ) )


# Estimate body motion
[ ins_state, ins_var ] = ins_ext_kfilter( 
	imu_time, imu_accel, imu_gyro, accel_bias_std, gyro_bias_std,
	imu_body_alpha0, imu_body_alpha0_std, 
	gnss_time, gnss_speed, gnss_dist, gnss_speed_w_std, gnss_dist_w_std )


imu_accel_x 		= [ v.item( (0, 0) ) for v in imu_accel ]
imu_accel_y 		= [ v.item( (1, 0) ) for v in imu_accel ]
imu_alpha_speed		= [ np.rad2deg( v.item( (0, 0) ) ) for v in imu_gyro ]
gnss_dist_x 		= [ v.item( (0, 0) ) for v in gnss_dist ]
gnss_dist_y 		= [ v.item( (1, 0) ) for v in gnss_dist ]
gnss_speed_norm		= [ v.item( (0, 0) ) for v in gnss_speed ]

real_accel_bias_x 	= [ v.item( (0, 0) ) for v in real_accel_bias ]
real_accel_bias_y 	= [ v.item( (1, 0) ) for v in real_accel_bias ]
real_gyro_bias_alpha = [ np.rad2deg( v.item( (0, 0) ) ) for v in real_gyro_bias ]
real_glob_accel_x 	= [ v.item( (0, 0) ) for v in real_glob_accel ]
real_glob_accel_y 	= [ v.item( (1, 0) ) for v in real_glob_accel ]
real_glob_speed_x 	= [ v.item( (0, 0) ) for v in real_glob_speed ]
real_glob_speed_y 	= [ v.item( (1, 0) ) for v in real_glob_speed ]
real_glob_speed_norm = [ v.item( (0, 0) ) for v in real_glob_speed_norm ]
real_glob_dist_x 	= [ v.item( (0, 0) ) for v in real_glob_dist ]
real_glob_dist_y 	= [ v.item( (1, 0) ) for v in real_glob_dist ]
real_body_alpha		= [ np.rad2deg( v.item( (0, 0) ) ) for v in real_body_angles ]

ekf_glob_dist_x			= [ v.item( ( 0, 0 ) ) 	for v in ins_state ]
ekf_glob_dist_y			= [ v.item( ( 1, 0 ) ) 	for v in ins_state ]
ekf_glob_speed_x		= [ v.item( ( 2, 0 ) ) 	for v in ins_state ]
ekf_glob_speed_y		= [ v.item( ( 3, 0 ) ) 	for v in ins_state ]
ekf_glob_speed_norm		= [ np.sqrt(x**2+y**2) 	for x,y in zip(ekf_glob_speed_x, ekf_glob_speed_y) ]
ekf_accel_bias_x		= [ v.item( ( 4, 0 ) ) 	for v in ins_state ]
ekf_accel_bias_x_var	= [ np.sqrt( v.item( ( 4, 4 ) ) ) 	for v in ins_var ]
ekf_accel_bias_y		= [ v.item( ( 5, 0 ) ) 	for v in ins_state ]
ekf_accel_bias_y_var	= [ np.sqrt( v.item( ( 5, 5 ) ) ) 	for v in ins_var ]
ekf_alpha				= [ np.rad2deg( v.item( ( 6, 0 ) ) ) for v in ins_state ]
ekf_alpha_var			= [ np.rad2deg( np.sqrt( v.item( ( 6, 6 ) ) ) ) for v in ins_var ]
ekf_gyro_bias_alpha		= [ np.rad2deg( v.item( ( 7, 0 ) ) ) for v in ins_state ]
ekf_gyro_bias_alpha_var	= [ np.rad2deg( np.sqrt( v.item( ( 7, 7 ) ) ) )	for v in ins_var ]



plt.figure()
plt.title('alpha speed')
plt.plot(imu_time, imu_alpha_speed, 'r')

plt.figure()
plt.title('accel')
plt.subplot(211)
plt.plot(imu_time, imu_accel_x, 'r')
plt.subplot(212)
plt.plot(imu_time, imu_accel_y, 'r')

plt.figure()
plt.title('speed norm')
plt.plot(imu_time, real_glob_speed_norm, 'b', gnss_time, gnss_speed_norm, 'g', imu_time, ekf_glob_speed_norm, 'c')

plt.figure()
plt.title('bias')
plt.subplot(231)
plt.plot(imu_time, real_accel_bias_x, 'b', imu_time, ekf_accel_bias_x, 'c')
plt.subplot(232)
plt.plot(imu_time, real_accel_bias_y, 'b', imu_time, ekf_accel_bias_y, 'c')
plt.subplot(233)
plt.plot(imu_time, real_gyro_bias_alpha, 'b', imu_time, ekf_gyro_bias_alpha, 'c')
plt.subplot(234)
plt.plot(imu_time, ekf_accel_bias_x_var, 'c')
plt.subplot(235)
plt.plot(imu_time, ekf_accel_bias_y_var, 'c')
plt.subplot(236)
plt.plot(imu_time, ekf_gyro_bias_alpha_var, 'c')

plt.figure()
plt.title('speed')
plt.subplot(211)
plt.plot(imu_time, real_glob_speed_x, 'b', imu_time, ekf_glob_speed_x, 'c')
plt.subplot(212)
plt.plot(imu_time, real_glob_speed_y, 'b', imu_time, ekf_glob_speed_y, 'c')

plt.figure()
plt.title('dist')
plt.subplot(211)
plt.plot(imu_time, real_glob_dist_x, 'b', gnss_time, gnss_dist_x, 'g', imu_time, ekf_glob_dist_x, 'c')
plt.subplot(212)
plt.plot(imu_time, real_glob_dist_y, 'b', gnss_time, gnss_dist_y, 'g', imu_time, ekf_glob_dist_y, 'c')

plt.figure()
plt.title('surf')
plt.plot(real_glob_dist_x, real_glob_dist_y, 'b', gnss_dist_x, gnss_dist_y, 'g', ekf_glob_dist_x, ekf_glob_dist_y, 'c')

plt.figure()
plt.title('alpha')
plt.subplot(211)
plt.plot(imu_time, real_body_alpha, 'b', imu_time, ekf_alpha, 'c' )
plt.subplot(212)
plt.title('alpha var')
plt.plot(imu_time, ekf_alpha_var, 'c' )

plt.show()