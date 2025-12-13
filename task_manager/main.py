from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
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
    console.print("[4] Editar tarefa")
    console.print("[5] Remover tarefa")
    console.print("[6] Sair", style= "red")

def list_tasks():
    if not tasks:
        console.print("[dim italic]📭 Nenhuma tarefa ainda...[/]")
        return
    table = Table(title="Suas Tarefas", box=None) # box=None deixa mais "clean"
    
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Título", style="magenta")
    table.add_column("Status", style="green", justify="center")  
    
    for task in tasks:
        status = "✅ Concluída" if task["done"] else "⏳ Pendente"
        table.add_row(str(task["id"]), task["title"], status)
            
    console.print(table)
    
def edit_task():
    list_tasks()
    task_id = Prompt.ask("Digite o ID da tarefa que deseja editar")
    for task in tasks:
        if str(task["id"]) == task_id:
            novo_titulo = Prompt.ask("Novo título da tarefa", default=task["title"])
            task["title"] = novo_titulo
            save_tasks()
            console.print("[bold green]✏️  Tarefa atualizada com sucesso! [/bold green]")
            return
    console.print("[bold red]❌ ID não encontrado.[/bold red] ")
        
def remove_task():
    list_tasks()
    task_id = Prompt.ask("Qual tarefa(ID) deseja remover?")
    for index, task in enumerate(tasks):
        if str(task["id"]) == task_id:
            tasks.pop(index)
            save_tasks()
            console.print("[bold green]🗑️  Tarefa removida![/bold green]")
            return
    console.print("[bold red]❌ Tarefa não encontrada")

# Programa principal
show_banner()
while True:
    show_menu()
    choice = IntPrompt.ask("Escolha", choices=["1", "2", "3", "4", "5", "6"])
    
    if choice == 1:
        list_tasks()
    elif choice == 2:
        title = Prompt.ask("📝 Novo título")
        tasks.append({"id": len(tasks)+1, "title": title, "done": False})
        save_tasks()
        console.print("[bold green]✅ Tarefa salva com sucesso![/bold green]")
    elif choice == 3:
        list_tasks()
        if tasks:
            task_id = IntPrompt.ask("ID para concluir")
            for task in tasks:
                if task["id"] == task_id:
                    task["done"] = True
                    save_tasks()
                    console.print("[bold green]🎉 Tarefa Concluída![/bold green]")
                    break
            else:
                console.print("[bold red]❌ ID não encontrado.[/bold red]")
    elif choice == 4:
        edit_task()
        
    elif choice == 5:
        remove_task()
    
    elif choice == 6:
        console.print("[bold blue]👋 Tchau![/]")
        break
    
    console.print()  # Linha em branco
