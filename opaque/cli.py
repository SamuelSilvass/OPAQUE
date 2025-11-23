import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from typing import Optional
from opaque.validators import Validators
from opaque.vault import Vault
from opaque.audit import AuditScanner
import importlib.metadata

# Initialize Typer app and Rich console
app = typer.Typer(
    name="opaque",
    help="OPAQUE - Deterministic Data Masking & Validation Engine",
    add_completion=True,
    rich_markup_mode="rich"
)
console = Console()

def get_version():
    try:
        return importlib.metadata.version("opaque-logger")
    except importlib.metadata.PackageNotFoundError:
        return "dev"

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, version: bool = typer.Option(False, "--version", "-v", help="Show version")):
    """
    OPAQUE CLI - The Ultimate Security & Validation Tool.
    """
    if version:
        console.print(f"[bold blue]OPAQUE[/bold blue] version [green]{get_version()}[/green]")
        raise typer.Exit()
        
    if ctx.invoked_subcommand is None:
        # Show banner if no command is invoked
        show_banner()
        console.print("[yellow]Use --help to see available commands.[/yellow]")

def show_banner():
    banner = r"""
   ____  ____  ___    ____  __  ____ 
  / __ \/ __ \/   |  / __ \/ / / / /_
 / / / / /_/ / /| | / / / / / / / __/
/ /_/ / ____/ ___ |/ /_/ / /_/ / /_  
\____/_/   /_/  |_|\___\_\____/\__/  
                                     
    """
    console.print(Panel(
        Text(banner, justify="center", style="bold cyan"),
        title="[bold white]Security & Validation Engine[/bold white]",
        subtitle="[dim]Professional Edition[/dim]",
        border_style="blue"
    ))

@app.command()
def validate(
    validator_type: str = typer.Argument(..., help="Type of validation (e.g., CPF, AR.DNI, PLATES.MERCOSUL_BR)"),
    value: str = typer.Argument(..., help="The value to validate")
):
    """
    [bold green]Validate[/bold green] a specific document or license plate.
    """
    validator_class = get_validator_by_name(validator_type)
    
    if not validator_class:
        console.print(f"[bold red]❌ Error:[/bold red] Validator '{validator_type}' not found.")
        console.print("[yellow]Tip: Use 'list-validators' to see all available options.[/yellow]")
        raise typer.Exit(code=1)
    
    is_valid = validator_class.validate(value)
    
    if is_valid:
        console.print(Panel(
            f"[bold green]VALID[/bold green]\n\nValue: [white]{value}[/white]\nType: [cyan]{validator_type}[/cyan]",
            title="Validation Result",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]INVALID[/bold red]\n\nValue: [white]{value}[/white]\nType: [cyan]{validator_type}[/cyan]",
            title="Validation Result",
            border_style="red"
        ))
        raise typer.Exit(code=1)

@app.command()
def reveal(
    token: str = typer.Argument(..., help="The encrypted token (e.g., [VAULT:abc...])"),
    key: str = typer.Option(..., "--key", "-k", help="Master Key for decryption")
):
    """
    [bold yellow]Reveal[/bold yellow] (decrypt) a Vault token.
    """
    vault = Vault(key=key)
    try:
        with console.status("[bold green]Decrypting...[/bold green]", spinner="dots"):
            decrypted = vault.decrypt(token)
        
        console.print(Panel(
            f"[bold white]{decrypted}[/bold white]",
            title="[bold green]🔓 Decrypted Data[/bold green]",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[bold red]❌ Decryption Failed:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def scan(
    directory: str = typer.Argument(".", help="Directory to scan"),
    output: str = typer.Option("opaque_report.html", "--output", "-o", help="Output HTML file")
):
    """
    [bold blue]Scan[/bold blue] a directory for compliance and security issues.
    """
    console.print(f"[bold cyan]🔍 Starting Security Scan on:[/bold cyan] {directory}")
    
    scanner = AuditScanner()
    
    with console.status("[bold blue]Scanning files...[/bold blue]", spinner="earth"):
        report = scanner.scan_directory(directory)
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(report)
        
    # Extract score for display
    import re
    score_match = re.search(r"Security Score: <span.*?>(.*?)</span>", report)
    score = score_match.group(1) if score_match else "N/A"
    
    table = Table(title="Scan Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Target Directory", directory)
    table.add_row("Report File", output)
    table.add_row("Security Score", score)
    
    console.print(table)
    console.print(f"\n[bold green]✅ Scan Complete![/bold green] Open [underline]{output}[/underline] to view details.")

@app.command()
def benchmark():
    """
    [bold cyan]Benchmark[/bold cyan] OPAQUE performance.
    """
    import time
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    
    console.print(Panel("[bold cyan]Running Performance Benchmarks...[/bold cyan]", border_style="cyan"))
    
    results = []
    
    def run_bench(name, func, iterations=100000):
        start = time.time()
        for _ in range(iterations):
            func()
        end = time.time()
        duration = end - start
        ops_sec = iterations / duration
        return name, ops_sec

    # Setup dummy data
    cpf_valid = "529.982.247-25"
    cnpj_valid = "11.444.777/0001-61"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
    ) as progress:
        
        task1 = progress.add_task("[green]Benchmarking CPF Validation...", total=100)
        # Warmup
        for _ in range(1000): Validators.BR.CPF.validate(cpf_valid)
        
        # Run
        name, ops = run_bench("CPF Validation", lambda: Validators.BR.CPF.validate(cpf_valid))
        results.append((name, ops))
        progress.update(task1, advance=100)
        
        task2 = progress.add_task("[green]Benchmarking CNPJ Validation...", total=100)
        name, ops = run_bench("CNPJ Validation", lambda: Validators.BR.CNPJ.validate(cnpj_valid))
        results.append((name, ops))
        progress.update(task2, advance=100)
        
        task3 = progress.add_task("[green]Benchmarking Encryption (Vault)...", total=100)
        v = Vault(key="bench-key")
        name, ops = run_bench("Vault Encrypt", lambda: v.encrypt("sensitive-data"), iterations=10000)
        results.append((name, ops))
        progress.update(task3, advance=100)

    table = Table(title="Benchmark Results", show_header=True, header_style="bold magenta")
    table.add_column("Operation", style="cyan")
    table.add_column("Ops/Sec", style="green", justify="right")
    
    for name, ops in results:
        table.add_row(name, f"{ops:,.0f}")
        
    console.print(table)

@app.command()
def interactive():
    """
    [bold yellow]Interactive Mode[/bold yellow] - Real-time validation playground.
    """
    console.clear()
    show_banner()
    console.print("[bold green]Welcome to OPAQUE Interactive Shell[/bold green]")
    console.print("Type 'exit' to quit.\n")
    
    while True:
        try:
            cmd = typer.prompt("opaque >")
            if cmd.lower() in ('exit', 'quit'):
                break
                
            # Simple parsing: VALIDATOR value
            parts = cmd.split(" ", 1)
            if len(parts) != 2:
                console.print("[red]Invalid format. Use: VALIDATOR_NAME value[/red]")
                continue
                
            val_name, value = parts
            validator = get_validator_by_name(val_name)
            
            if not validator:
                console.print(f"[red]Validator '{val_name}' not found.[/red]")
                continue
                
            is_valid = validator.validate(value)
            if is_valid:
                console.print(f"[bold green]✔ VALID[/bold green]")
            else:
                console.print(f"[bold red]✘ INVALID[/bold red]")
                
        except KeyboardInterrupt:
            break
    
    console.print("\n[yellow]Goodbye![/yellow]")

@app.command("list-validators")
def list_validators():
    """
    [bold magenta]List[/bold magenta] all available validators.
    """
    table = Table(title="Available Validators", show_lines=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Validator Name", style="green")
    table.add_column("Description", style="white")

    # Helper to recursively find validators
    def add_validators(cls_obj, prefix=""):
        for name, attr in cls_obj.__dict__.items():
            if name.startswith("_"): continue
            
            if isinstance(attr, type):
                # Check if it's a nested class container (like BR, AR) or a Validator
                if hasattr(attr, "validate"):
                    # It's a validator class
                    full_name = f"{prefix}{name}" if prefix else name
                    doc = attr.validate.__doc__ or "No description"
                    category = prefix.rstrip(".") if prefix else "General"
                    table.add_row(category, full_name, doc)
                else:
                    # It's a container class (like BR, AR)
                    add_validators(attr, prefix=f"{prefix}{name}.")

    add_validators(Validators)
    console.print(table)

def get_validator_by_name(name: str):
    """Helper to retrieve a validator class by its dot-notation name."""
    parts = name.split(".")
    obj = Validators
    try:
        for part in parts:
            obj = getattr(obj, part)
        return obj if hasattr(obj, "validate") else None
    except AttributeError:
        return None

@app.command()
def analyze(
    target: str = typer.Argument(..., help="Text string or file path to analyze"),
    threshold: float = typer.Option(3.5, help="Entropy threshold for secret detection"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results in JSON format")
):
    """
    [bold red]Analyze[/bold red] text or file for sensitive data and secrets.
    """
    import os
    import json
    
    content = target
    source = "Text Input"
    
    if os.path.exists(target):
        source = f"File: {target}"
        try:
            with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)

    if not json_output:
        console.print(Panel(f"[bold cyan]Analyzing {source}...[/bold cyan]", border_style="blue"))
    
    found_items = []
    
    # Flatten validators
    all_validators = []
    def collect_validators(cls_obj, prefix=""):
        for name, attr in cls_obj.__dict__.items():
            if name.startswith("_"): continue
            if isinstance(attr, type):
                if hasattr(attr, "validate"):
                    all_validators.append((f"{prefix}{name}" if prefix else name, attr))
                else:
                    collect_validators(attr, prefix=f"{prefix}{name}.")
    
    collect_validators(Validators)
    
    # Heuristic scanning
    import re
    tokens = re.split(r'[\s\n\r"\'=,;:<>()\[\]{}]+', content)
    tokens = [t for t in tokens if len(t) > 4] # Ignore short tokens
    
    # Also check entropy on tokens
    for token in set(tokens): # Deduplicate for speed
        # Check Entropy
        if Validators.SECURITY.ENTROPY.validate(token, threshold=threshold):
            found_items.append({
                "type": "SECURITY.ENTROPY",
                "value": token,
                "description": "High Entropy String"
            })
        
        # Check other validators
        for name, val_cls in all_validators:
            if name == "SECURITY.ENTROPY": continue
            try:
                if val_cls.validate(token):
                    found_items.append({
                        "type": name,
                        "value": token,
                        "description": val_cls.validate.__doc__ or "No description"
                    })
            except:
                pass

    if json_output:
        console.print(json.dumps(found_items, indent=2))
    else:
        if found_items:
            table = Table(title=f"Found {len(found_items)} Sensitive Items", show_header=True)
            table.add_column("Type", style="cyan")
            table.add_column("Value", style="red")
            table.add_column("Description", style="white")
            
            for item in found_items:
                v_value = item["value"]
                # Mask value for display
                masked = v_value[:4] + "*" * (len(v_value)-8) + v_value[-4:] if len(v_value) > 8 else "*"*len(v_value)
                table.add_row(item["type"], masked, item["description"])
                
            console.print(table)
        else:
            console.print("[bold green]No sensitive data found![/bold green]")

@app.command()
def demo():
    """
    [bold magenta]Demo[/bold magenta] - Visual simulation of OPAQUE capabilities.
    """
    import time
    from rich.layout import Layout
    from rich.live import Live
    
    console.clear()
    
    simulated_logs = [
        ("INFO", "User login attempt: user@example.com"),
        ("DEBUG", "Payment processing for card: 4532-1234-5678-9012"),
        ("WARN", "Invalid CPF detected: 123.456.789-00"),
        ("INFO", "AWS Key rotation: AKIAIOSFODNN7EXAMPLE"),
        ("ERROR", "Connection failed to IP: 192.168.1.100"),
        ("DEBUG", "Received payload with token: ghp_123456789012345678901234567890123456"),
        ("INFO", "Patient CNS verified: 898001033308856"),
        ("WARN", "High entropy detected in config: 7^%#@!90$)(*&^%gHjK"),
    ]
    
    table = Table(title="OPAQUE Live Protection Demo", width=100)
    table.add_column("Level", style="bold")
    table.add_column("Message", style="white")
    table.add_column("OPAQUE Action", style="cyan")
    
    with Live(table, refresh_per_second=4) as live:
        for level, msg in simulated_logs:
            time.sleep(0.8)
            
            action = "✅ Allowed"
            style = "green"
            
            # Simple simulation logic
            if "card" in msg:
                msg = msg.replace("4532-1234-5678-9012", "[HASH-CC-8821]")
                action = "🛡️ Masked (Credit Card)"
                style = "yellow"
            elif "CPF" in msg:
                msg = msg.replace("123.456.789-00", "[INVALID-CPF]")
                action = "❌ Blocked (Invalid)"
                style = "red"
            elif "AWS" in msg:
                msg = msg.replace("AKIAIOSFODNN7EXAMPLE", "[VAULT:aws-key-1]")
                action = "🔒 Encrypted (Vault)"
                style = "blue"
            elif "ghp_" in msg:
                msg = re.sub(r"ghp_[a-zA-Z0-9]+", "[REDACTED-TOKEN]", msg)
                action = "🛡️ Redacted (GitHub)"
                style = "magenta"
            elif "CNS" in msg:
                 msg = msg.replace("898001033308856", "[HASH-CNS-9912]")
                 action = "🛡️ Masked (Health Data)"
                 style = "yellow"
            elif "entropy" in msg:
                msg = msg.replace("7^%#@!90$)(*&^%gHjK", "[HIGH-ENTROPY-BLOB]")
                action = "⚠️ Alerted (Secret)"
                style = "bold red"
                
            table.add_row(f"[{style}]{level}[/{style}]", msg, action)
            
    console.print(Panel("[bold green]Demo Complete![/bold green]\nOPAQUE protects your logs in real-time.", border_style="green"))

if __name__ == "__main__":
    app()
