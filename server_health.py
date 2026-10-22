import psutil
import argparse


def check_status(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return "CRITICAL"
    elif value >= warning_threshold:
        return "WARNING"
    else:
        return "OK"


def main():
    parser = argparse.ArgumentParser(
        description="Monitor CPU, memory, and disk usage"
    )

    parser.add_argument(
        "--warning",
        type=float,
        default=80,
        help="Warning threshold percentage (default: 80)"
    )

    parser.add_argument(
        "--critical",
        type=float,
        default=90,
        help="Critical threshold percentage (default: 90)"
    )

    parser.add_argument(
        "--disk-path",
        default="C:\\",
        help="Disk path to monitor (default: C:\\)"
    )

    args = parser.parse_args()

    if args.warning >= args.critical:
        parser.error("Warning threshold must be lower than critical threshold.")

    print("================================\n\tSERVER HEALTH CHECK\n================================")

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    try:
        disk = psutil.disk_usage(args.disk_path).percent
    except OSError:
        parser.error(
            f"Disk path does not exist or cannot be accessed: {args.disk_path}"
        )

    resources = {
        "CPU": cpu,
        "Memory": memory,
        "Disk": disk
    }

    resource_status = [
        check_status(value, args.warning, args.critical)
        for value in resources.values()
    ]

    for name, value in resources.items():
        print(f"{name}: {value:.1f}% f{check_status(value, args.warning, args.critical)}")

    if "CRITICAL" in resource_status:
        print("Overall Status: CRITICAL")
    elif "WARNING" in resource_status:
        print("Overall Status: WARNING")
    else:
        print("Overall Status: OK")


if __name__ == "__main__":
    main()
