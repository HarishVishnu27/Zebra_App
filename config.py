DEVICE = 'cuda'
FRAME_SKIP = 2
RTSP_URLS = {
    'cam1': 'rtsp://cam1_url',
    'cam2': 'rtsp://cam2_url',
    'cam3': 'rtsp://cam3_url',
    'cam4': 'rtsp://cam4_url'
}
REGIONS_FILE = 'regions_config.json'
REGIONS = {
    'cam1': {
        'Zebra': {
            'vertices': [[100, 100], [200, 100], [200, 200], [100, 200]],
            'color': [0, 0, 255],
        }
    },
    'cam2': {
        'Zebra': {
            'vertices': [[150, 150], [250, 150], [250, 250], [150, 250]],
            'color': [0, 0, 255],
        }
    },
    'cam3': {
        'Zebra': {
            'vertices': [[200, 200], [300, 200], [300, 300], [200, 300]],
            'color': [0, 0, 255],
        }
    },
    'cam4': {
        'Zebra': {
            'vertices': [[250, 250], [350, 250], [350, 350], [250, 350]],
            'color': [0, 0, 255],
        }
    },
}