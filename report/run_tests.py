import sys
import os
import subprocess
import time
import psutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from datetime import datetime
from rich.layout import Layout
from rich.text import Text
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

def make_ascii_progress_bar(percent, width=20):
    done = int(width * percent / 100)
    return '[' + '█' * done + '░' * (width - done) + ']'

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

def create_test_info_panel(test_info=None, percent=0, lang=None, compiler=None, limit=None):
    """Create a panel with test information, progress bar, language and limit."""
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    if test_info is None:
        for key in ["Limit", "Test", "Start Time", "Status", "Duration", "Memory Usage", "CPU Usage", "Language", "Compiler"]:
            table.add_row(key, "-")
    else:
        for key, value in test_info.items():
            table.add_row(key, str(value))
        if lang is not None:
            table.add_row("Language", lang)
        if compiler is not None:
            table.add_row("Compiler", compiler)
        if limit is not None:
            table.add_row("Current Limit", str(limit))
        table.add_row("Progress", f"{percent:.1f}% {make_ascii_progress_bar(percent)}")
    return Panel(table, title="Test Progress", border_style="green")

def parse_lang_compiler_from_line(line):
    # Пример: Тестирование python (python)...
    m = re.match(r"Тестирование\s+(\w+)\s*\(([^)]+)\)", line)
    if m:
        return m.group(1), m.group(2)
    return None, None

def run_all_tests_and_monitor(limits, progress, layout):
    start_time = time.time()
    test_info = {
        "Start Time": datetime.now().strftime("%H:%M:%S"),
        "Status": "Running",
        "Duration": "0.00s"
    }
    lang = compiler = None
    current_limit = None
    total_tests = 12 * len(limits)
    current_test = 0
    process = subprocess.Popen(['./run_all_tests.sh', str(limits[-1])],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               bufsize=1)
    output_lines = []
    while True:
        stats = get_system_stats()
        # Read next line from process
        line = process.stdout.readline() if process.stdout else ''
        if line:
            output_lines.append(line)
            l, c = parse_lang_compiler_from_line(line)
            if l and c:
                lang, compiler = l, c
                current_test += 1
                current_limit = limits[current_test-1] if current_test-1 < len(limits) else None
        # Update progress
        percent = 100 * (current_test / total_tests) if total_tests else 0
        layout["system_stats"].update(create_system_stats_panel(stats))
        layout["test_info"].update(create_test_info_panel(test_info, percent=percent, lang=lang, compiler=compiler, limit=current_limit))
        if not line and process.poll() is not None:
            break
        time.sleep(0.2)
    # Print remaining output
    for line in process.stdout:
        output_lines.append(line)
    process.stdout.close()
    process.wait()
    return output_lines

def main():
    console.print(Panel.fit(
        "[bold blue]Sieve of Eratosthenes Performance Test Runner[/]\n"
        "[dim]Running performance tests for different limits...[/]",
        border_style="blue"
    ))
    limits = list(range(1, 2000002, 1000))
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console
    )
    progress.add_task("[cyan]Overall Progress", total=100)
    progress.add_task("[green]Current Test", total=100)
    layout = Layout()
    layout.split_column(
        Layout(name="system_stats"),
        Layout(name="test_info")
    )
    layout["system_stats"].update(create_system_stats_panel())
    layout["test_info"].update(create_test_info_panel())
    with Live(layout, refresh_per_second=2) as live:
        run_all_tests_and_monitor(limits, progress, layout)
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