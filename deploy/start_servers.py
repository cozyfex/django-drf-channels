import argparse
import multiprocessing
import os
import subprocess


def get_cpu_count():
    return multiprocessing.cpu_count()


def start_gunicorn(is_single=False, port=8000):
    cpu_count = 1 if is_single else get_cpu_count()
    workers = 2 * cpu_count + 1
    command = [
        'gunicorn',
        'project.wsgi:application',
        '--workers',
        str(workers),
        '--bind',
        f'0.0.0.0:{port}',
        '--timeout',
        '120',
    ]
    subprocess.Popen(command)


def start_daphne(port=8001):
    cpu_count = get_cpu_count()
    workers = cpu_count  # Adjust if needed based on your application's characteristics
    command = [
        'daphne',
        '-u',
        str(workers),
        '-b',
        '0.0.0.0',
        '-p',
        f'{port}',
        'project.asgi:application',
    ]
    subprocess.Popen(command)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Example script with optional arguments.'
    )
    parser.add_argument(
        '--single', type=bool, default=False, help='Single mode (default: False)'
    )
    parser.add_argument(
        '--http-port', type=int, default=8000, help='HTTP Port (default: 8000)'
    )
    parser.add_argument(
        '--websocket-port',
        type=int,
        default=8001,
        help='WebSocket Port (default: 8001)',
    )
    args = parser.parse_args()

    # Get OS environment variables
    IS_SINGLE = os.environ.get('IS_SINGLE')
    HTTP_PORT = os.environ.get('HTTP_PORT')
    WEBSOCKET_PORT = os.environ.get('WEBSOCKET_PORT')

    single = IS_SINGLE if IS_SINGLE else args.single
    http_port = HTTP_PORT if HTTP_PORT else args.http_port
    websocket_port = WEBSOCKET_PORT if WEBSOCKET_PORT else args.websocket_port

    # Start Daphne
    print('Starting Daphne...')
    start_daphne(websocket_port)

    # Start Gunicorn
    print('Starting Gunicorn...')
    start_gunicorn(single, http_port)

    # Keep the script running to keep both servers alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping servers...')
