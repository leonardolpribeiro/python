from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
import json
from pathlib import Path
DATA_FILE = Path("tasks.json")

def load_tasks():
    global tasks
    if DATA_FILE.exists():
        tasks = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    else:
        tasks =[]
        
def save_tasks():
    DATA_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")
    
console = Console()
tasks = []
load_tasks()

def show_banner():
    """Banner simples com Rich (sem pyfiglet)"""
    banner = """
[bold cyan]🧠 TASK MANAGER CLI[/bold cyan]
[green]Gerenciador de Tarefas em Python[/green]
    """
    console.print(Panel.fit(banner, title="[bold yellow]Bem-vindo![/]", border_style="bold blue"))

def show_menu():
    console.print("\n[bold green]📋 Opções:[/bold green]")
    console.print("[1] Listar tarefas")
    console.print("[2] Adicionar tarefa") 
    console.print("[3] Concluir tarefa")
    console.print("[4] Sair", style= "red")

def list_tasks():
    if not tasks:
        console.print("[dim italic]📭 Nenhuma tarefa ainda...[/]")
    else:
        console.print("\n[bold cyan]📝 Suas tarefas:[/bold cyan]")
        for task in tasks:
            status = "✅" if task["done"] else "⏳"
            console.print(f"  {status} [bold]{task['id']}:[/bold] {task['title']}")


# Programa principal
show_banner()
while True:
    show_menu()
    choice = IntPrompt.ask("Escolha", choices=["1", "2", "3", "4"])
    
    if choice == 1:
        list_tasks()
    elif choice == 2:
        title = Prompt.ask("📝 Novo título")
        tasks.append({"id": len(tasks)+1, "title": title, "done": False})
        save_tasks()
        console.print("[green bold]✅ Tarefa salva![/]")
    elif choice == 3:
        list_tasks()
        if tasks:
            task_id = IntPrompt.ask("ID para concluir")
            for task in tasks:
                if task["id"] == task_id:
                    task["done"] = True
                    save_tasks()
                    console.print("[green bold]🎉 Concluída![/]")
                    break
            else:
                console.print("[red]❌ ID não encontrado[/]")
    elif choice == 4:
        console.print("[bold blue]👋 Tchau![/]")
        break
    
    console.print()  # Linha em branco
