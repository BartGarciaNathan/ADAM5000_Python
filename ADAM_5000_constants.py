  # Constants Module for the ADAM-5000 python server
# 		 Made by Bart Garcia

# ---------------------------------------------------------
# 					Module Address
# ---------------------------------------------------------
ADM_ADD 	= 	'00' #Using the Init function (Init input connected to GND on the device, if not change this value to the individual address of the device)

# ---------------------------------------------------------
# 					CPU Command Set
# ---------------------------------------------------------
CONF_STATUS					=	'2'
READ_MODULE_NAME			=	'M'
fIRMWARE_VERSION			=	'F'
IO_TYPE						=	'T'
RESET_STATUS				=	'5'
SOFT_DIAGNOSTICS			=	'E'
# ---------------------------------------------------------
# 					Analog Input Command Set
# ---------------------------------------------------------
AI_CONF                     = 'A'
AI_CONF_STATUS              = 'B'
AI_EN                       = '5'
AI_CHN_STATUS               = '6'
# AI_ALL_DATA_IN              =
AI_DATA_IN                  = 'C'
AI_EEPROM_DATA              = 'ER'
AI_SPAN_CAL                 = '0'
AI_ZERO_CAL                 = '1'
AI_CJC_STATUS               = '3'
AI_CJC_ZERO_CAL             = '9'
# ---------------------------------------------------------
# 					Calibration Voltage
# ---------------------------------------------------------
# Voltage range or thermocouple type
VR_15MV     = '00'
VR_50MV     = '01'
VR_100MV    = '02'
VR_500MV    = '03'
VR_1V       = '04'
VR_25V     = '05'
IR_20MA     = '06'
TC_J        = '0E'
TC_K        = '0F'
TC_T        = '10'
TC_E        = '11'
TC_R        = '12'
TC_S        = '13'
TC_B        = '14'
# ---------------------------------------------------------
# 					Analog Input Alarm Command Set
# ---------------------------------------------------------
# ---------------------------------------------------------
# 					Analog Output Command Set
# ---------------------------------------------------------
# ---------------------------------------------------------
# 					Digital Input/Output Command Set
# ---------------------------------------------------------
