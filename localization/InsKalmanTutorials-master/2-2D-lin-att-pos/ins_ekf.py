import numpy as np
import numpy.ma as ma

# State prediction function
def exec_f_func( x_vect, u_vect, period ):
	pos_gx   = x_vect.item( ( 0, 0 ) )
	pos_gy   = x_vect.item( ( 1, 0 ) )
	speed_gx = x_vect.item( ( 2, 0 ) )
	speed_gy = x_vect.item( ( 3, 0 ) )
	alpha    = x_vect.item( ( 4, 0 ) )
	
	accel_ix = u_vect.item( ( 0, 0 ) )
	accel_iy = u_vect.item( ( 1, 0 ) )
	
	accel_gx = accel_ix * np.cos( alpha ) - accel_iy * np.sin( alpha )
	accel_gy = accel_ix * np.sin( alpha ) + accel_iy * np.cos( alpha )
	
	return np.matrix([
		[ pos_gx + speed_gx * period + accel_gx * 0.5 * period**2 ],
		[ pos_gy + speed_gy * period + accel_gy * 0.5 * period**2 ],
		[ speed_gx + accel_gx * period ],
		[ speed_gy + accel_gy * period ],
		[ alpha ],
	])
	
# State prediction Jacobian matrix
def get_F_matrix( x_vect, u_vect, period ):
	accel_ix = u_vect.item( ( 0, 0 ) )
	accel_iy = u_vect.item( ( 1, 0 ) )
	alpha = x_vect.item( ( 4, 0 ) )
	
	d_accel_gx = -accel_ix * np.sin( alpha ) - accel_iy * np.cos( alpha )
	d_accel_gy =  accel_ix * np.cos( alpha ) - accel_iy * np.sin( alpha )
	
	F = np.matrix([
		[1,   0,   period,   0,       d_accel_gx * 0.5 * period**2 ],
		[0,   1,   0,        period,  d_accel_gy * 0.5 * period**2 ],
		[0,   0,   1,        0,  	  d_accel_gx * period          ],
		[0,   0,   0,        1,  	  d_accel_gy * period          ],
		[0,   0,   0,        0,       1                            ]
	])
	
	return F
	
# Observation function
def exec_h_func( x_vect, period ):
	pos_gx   = x_vect.item( ( 0, 0 ) )
	pos_gy   = x_vect.item( ( 1, 0 ) )
	
	return np.matrix([
		[ pos_gx ],
		[ pos_gy ]
	])	
	
# Observation Jacobian matrix
def get_H_matrix( x_vect, period ):
	return np.matrix([
		[ 1, 0, 0, 0, 0 ],
		[ 0, 1, 0, 0, 0 ]
	])
	
def ins_ext_kfilter( imu_time, imu_accel, alpha0, alpha0_std, gnss_time, gnss_dist, gnss_std ):
	# Output data
	state_list = []
	
	# IMU sampling period
	imu_dt = imu_time[1] - imu_time[0]
	# State matrix
	X = np.matrix([ 
		# X position
		[0.0],
		# Y position
		[0.0],
		# X speed
		[0.0],
		# Y speed
		[0.0],
		# alpha
		[alpha0]
	])
	# Process noise matrix
	Q = np.matrix([
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
	])
	# Measurement noise matrix
	R = np.matrix([
		[gnss_std**2,   0          ],
		[0,             gnss_std**2]
	])
	# State covariance matrix
	P = np.matrix([
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, alpha0_std**2],
	])
	
	gnss_i = 0
	for t, U in zip( imu_time, imu_accel ):
		# Gnss data available
		if ( gnss_i < len( gnss_time ) and t > gnss_time[ gnss_i ] ):			
			# ----- Kalman update step
			H = get_H_matrix( X, imu_dt )
			Z = gnss_dist[ gnss_i ]
			# Calculate gain
			K = P * H.transpose() * np.linalg.inv( ( H * P * H.transpose() + R ) )
			# Estimate state
			X = X + K * ( Z - exec_h_func( X, imu_dt ) )
			# Estimate noise
			P = P - K * H * P
			
			gnss_i = gnss_i + 1
			
		# ----- Kalman predict step
		F = get_F_matrix( X, U, imu_dt )
		X = exec_f_func( X, U, imu_dt )
		P = F * P * F.transpose() + Q
		
		state_list.append( X.copy() )
	
	return state_list
		
	