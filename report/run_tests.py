import sys
import os
import subprocess
import time
import psutil
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from datetime import datetime
from rich.layout import Layout
import threading
import queue
import re
import generate_report

console = Console()

def get_system_stats():
    """Get detailed system statistics."""
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    load_avg = os.getloadavg()
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    return {
        'cpu_count': cpu_count,
        'cpu_freq': cpu_freq.current if cpu_freq else None,
        'cpu_per_core': cpu_percent,
        'cpu_avg': sum(cpu_percent) / len(cpu_percent),
        'mem_total': memory.total / (1024 * 1024 * 1024),
        'mem_used': memory.used / (1024 * 1024 * 1024),
        'mem_avail': memory.available / (1024 * 1024 * 1024),
        'mem_percent': memory.percent,
        'disk_total': disk.total / (1024 * 1024 * 1024),
        'disk_used': disk.used / (1024 * 1024 * 1024),
        'disk_percent': disk.percent,
        'net_sent': net_io.bytes_sent / (1024 * 1024),
        'net_recv': net_io.bytes_recv / (1024 * 1024),
        'load_1': load_avg[0],
        'load_5': load_avg[1],
        'load_15': load_avg[2],
    }

def create_system_stats_panel(stats=None):
    """Create a compact system statistics panel (one table, no double header)."""
    table = Table(box=box.ROUNDED, show_header=True, title=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    if stats is None:
        for key in ["Total Cores", "CPU Freq", "CPU Avg", "Mem Used", "Mem %", "Disk Used", "Disk %", "Net Sent", "Net Recv", "Load 1m"]:
            table.add_row(key, "-")
    else:
        table.add_row("Total Cores", str(stats['cpu_count']))
        table.add_row("CPU Freq", f"{stats['cpu_freq']:.1f} MHz" if stats['cpu_freq'] else "-")
        table.add_row("CPU Avg", f"{stats['cpu_avg']:.1f}%")
        table.add_row("Mem Used", f"{stats['mem_used']:.1f} GB / {stats['mem_total']:.1f} GB")
        table.add_row("Mem %", f"{stats['mem_percent']}%")
        table.add_row("Disk Used", f"{stats['disk_used']:.1f} GB / {stats['disk_total']:.1f} GB")
        table.add_row("Disk %", f"{stats['disk_percent']}%")
        table.add_row("Net Sent", f"{stats['net_sent']:.1f} MB")
        table.add_row("Net Recv", f"{stats['net_recv']:.1f} MB")
        table.add_row("Load 1m", f"{stats['load_1']:.2f}")
    return Panel(table, title="System Statistics", border_style="blue")

def create_logs_panel(log_lines):
    log_text = "".join(log_lines[-20:]) if log_lines else "(пока нет вывода)"
    return Panel(log_text, title="Тесты: вывод и логи", border_style="magenta")

def run_all_tests_and_stream_logs(limits, log_queue, done_flag):
    for limit in limits:
        log_queue.put(f"\n[bold yellow]=== Тесты для лимита N = {limit} ===[/bold yellow]\n")
        process = subprocess.Popen(['./run_all_tests.sh', str(limit)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True,
                                   bufsize=1)
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
    done_flag.set()

def main():
    console.print(Panel.fit(
        "[bold blue]Sieve of Eratosthenes Performance Test Runner[/]\n"
        "[dim]Running performance tests for different limits...[/]",
        border_style="blue"
    ))
    limits = list(range(100000, 2000002, 100000))
    layout = Layout()
    layout.split_column(
        Layout(name="system_stats"),
        Layout(name="logs")
    )
    layout["system_stats"].update(create_system_stats_panel())
    layout["logs"].update(create_logs_panel([]))
    log_queue = queue.Queue()
    done_flag = threading.Event()
    log_lines = []
    # Поток для тестов
    test_thread = threading.Thread(target=run_all_tests_and_stream_logs, args=(limits, log_queue, done_flag))
    test_thread.start()
    # Основной поток: обновление live-интерфейса
    with Live(layout, refresh_per_second=2) as live:
        while not done_flag.is_set() or not log_queue.empty():
            # Обновляем системную статистику
            stats = get_system_stats()
            layout["system_stats"].update(create_system_stats_panel(stats))
            # Обновляем логи
            while not log_queue.empty():
                log_lines.append(log_queue.get())
            layout["logs"].update(create_logs_panel(log_lines))
            time.sleep(0.5)
    test_thread.join()
    generate_report.generate_report()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Test execution interrupted by user.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/]")
        sys.exit(1)