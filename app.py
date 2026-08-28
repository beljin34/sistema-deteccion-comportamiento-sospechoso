from flask import Flask, render_template, Response, jsonify, request, abort
import cv2
import threading
import time
from detector import Detector
from collections import deque

app = Flask(__name__)
start_time = time.time()

detector = Detector(accum_weight=0.01, min_area=800, loiter_frames=90, loiter_radius=25)

# Shared camera and events
camera = cv2.VideoCapture(0)  # 0 = default camera. Change to path for video file.
if not camera.isOpened():
    print("No se pudo abrir la cámara. Revisa el índice o usa un archivo de vídeo.")

events = deque(maxlen=200)
lock = threading.Lock()

# --- Video streaming generator
def mjpeg_generator():
    while True:
        grabbed, frame = camera.read()
        if not grabbed:
            time.sleep(0.1)
            continue

        frame = cv2.resize(frame, (640, 480))
        annotated, evs = detector.process(frame)

        # Add events to log
        if evs:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            with lock:
                for e in evs:
                    events.appendleft(f"{ts} - {e}")

        # encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', annotated)
        if not ret:
            continue

        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- Web UI endpoints
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(mjpeg_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- API endpoints
@app.route('/api/health', methods=['GET'])
def api_health():
    uptime = time.time() - start_time
    return jsonify({
        'status': 'ok',
        'uptime_seconds': int(uptime)
    })

@app.route('/api/events', methods=['GET'])
def api_get_events():
    with lock:
        return jsonify(list(events))

@app.route('/api/events', methods=['POST'])
def api_post_event():
    if not request.is_json:
        return jsonify({'error': 'JSON body required'}), 400
    data = request.get_json()
    # validate
    typ = data.get('type')
    x = data.get('x')
    y = data.get('y')
    details = data.get('details', '')
    if not typ or x is None or y is None:
        return jsonify({'error': 'type, x and y are required'}), 400
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    ev = {
        'id': int(time.time() * 1000),
        'type': typ,
        'x': x,
        'y': y,
        'details': details,
        'ts': ts
    }
    with lock:
        events.appendleft(ev)
    return jsonify(ev), 201

@app.route('/api/config', methods=['GET'])
def api_get_config():
    cfg = {
        'accum_weight': detector.accum_weight,
        'min_area': detector.min_area,
        'loiter_frames': detector.loiter_frames,
        'loiter_radius': detector.loiter_radius
    }
    return jsonify(cfg)

@app.route('/api/config', methods=['PUT'])
def api_put_config():
    if not request.is_json:
        return jsonify({'error': 'JSON body required'}), 400
    data = request.get_json()
    # simple validations
    errors = []
    if 'accum_weight' in data:
        aw = data['accum_weight']
        if not (0.0 < float(aw) < 1.0):
            errors.append('accum_weight must be between 0 and 1')
        else:
            detector.accum_weight = float(aw)
    if 'min_area' in data:
        ma = int(data['min_area'])
        if ma <= 0:
            errors.append('min_area must be > 0')
        else:
            detector.min_area = ma
    if 'loiter_frames' in data:
        lf = int(data['loiter_frames'])
        if lf <= 0:
            errors.append('loiter_frames must be > 0')
        else:
            detector.loiter_frames = lf
            # also adjust history maxlen
            detector.history = deque(maxlen=detector.loiter_frames)
    if 'loiter_radius' in data:
        lr = int(data['loiter_radius'])
        if lr < 0:
            errors.append('loiter_radius must be >= 0')
        else:
            detector.loiter_radius = lr

    if errors:
        return jsonify({'errors': errors}), 400
    return jsonify({
        'message': 'config updated',
        'config': {
            'accum_weight': detector.accum_weight,
            'min_area': detector.min_area,
            'loiter_frames': detector.loiter_frames,
            'loiter_radius': detector.loiter_radius
        }
    })

@app.route('/api/video_url', methods=['GET'])
def api_video_url():
    return jsonify({'url': '/video_feed'})

@app.route('/detections')
def get_detections():
    with lock:
        # return recent events as list
        return jsonify(list(events))

def cleanup():
    try:
        camera.release()
    except:
        pass

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    finally:
        cleanup()
