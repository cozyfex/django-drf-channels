import argparse
import multiprocessing
import subprocess


def get_cpu_count():
    parser = argparse.ArgumentParser(
        description='Example script with optional arguments.'
    )
    parser.add_argument(
        '--single', type=bool, default=False, help='Single mode (default: False)'
    )
    args = parser.parse_args()
    if args.single:
        return 1
    else:
        return multiprocessing.cpu_count()


def start_gunicorn():
    cpu_count = get_cpu_count()
    workers = 2 * cpu_count + 1
    command = [
        'gunicorn',
        'project.wsgi:application',
        '--workers',
        str(workers),
        '--bind',
        '0.0.0.0:8000',
    ]
    subprocess.Popen(command)


def start_daphne():
    cpu_count = get_cpu_count()
    workers = cpu_count  # Adjust if needed based on your application's characteristics
    command = ['daphne', '-u', str(workers), '-p', '8001', 'project.asgi:application']
    subprocess.Popen(command)


if __name__ == '__main__':
    # Start Gunicorn
    print('Starting Gunicorn...')
    start_gunicorn()

    # Start Daphne
    print('Starting Daphne...')
    start_daphne()

    # Keep the script running to keep both servers alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping servers...')
