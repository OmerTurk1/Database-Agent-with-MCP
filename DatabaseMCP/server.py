from mcp.server.fastmcp import FastMCP
import sqlite3
import os
import matplotlib.pyplot as plt

BASE_DIR = "./workspace"
mcp = FastMCP("Database Manager")

def get_db_connection():
    return sqlite3.connect(os.path.join(BASE_DIR, "database.db"))

@mcp.tool()
def list_database_tables():
    """Returns the list of all the tables in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        conn.commit()
        return cursor.fetchall()

@mcp.tool()
def get_table_schema(table_name: str):
    """Returns the related table's column names and features."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        conn.commit()
        return cursor.fetchall()

@mcp.tool()
def execute_query(sql_command: str):
    """Takes the sql commands from LLM and runs it on the database, then returns the output."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{sql_command}")
            conn.commit()
            return cursor.fetchall()
        return {"sql": sql_command, "result": result}
    except Exception as e:
        return f"Error occurred: {str(e)} | Executed SQL: {sql_command}"

@mcp.tool()
def write_file(filename:str,content:str,write_mode:str):
    """Writes the content into a file. write model can be 'w' or 'a'."""
    path = os.path.abspath(os.path.join(BASE_DIR, filename))

    if not path.startswith(os.path.abspath(BASE_DIR)):
        raise ValueError("Tried to access inacessable area!")

    with open(path, write_mode, encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "message": f"{filename} created."
    }

@mcp.tool()
def read_file(filename: str):
    """Returns the content in a file."""
    filename = os.path.basename(filename)
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return {"status": "error", "message": "Could not find the file!"}

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "status": "ok",
        "content": content
    }

@mcp.tool()
def delete(filename: str):
    """Deletes file or folder."""
    filename = os.path.basename(filename)
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return {
            "status": "error",
            "message": "Could not find the file!"
        }

    os.remove(path)

    return {
        "status": "ok",
        "message": f"{filename} deleted."
    }

@mcp.tool()
def list_files():
    """Lists the files and folders on the workspace."""
    try:
        items = os.listdir(BASE_DIR)
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Workspace could not be found!"
        }

    files = []
    directories = []

    for item in items:
        path = os.path.join(BASE_DIR, item)
        if os.path.isfile(path):
            files.append(item)
        elif os.path.isdir(path):
            directories.append(item)

    return {
        "status": "ok",
        "files": files,
        "directories": directories
    }

@mcp.tool()
def rename_file(oldname: str, newname: str):
    """Renames the existing file or folder."""
    oldname = os.path.basename(oldname)
    newname = os.path.basename(newname)

    old_path = os.path.join(BASE_DIR, oldname)
    new_path = os.path.join(BASE_DIR, newname)

    if not os.path.exists(old_path):
        return {
            "status": "error",
            "message": "Source file or folder could not be found!"
        }

    if os.path.exists(new_path):
        return {
            "status": "error",
            "message": "Target name already exists!"
        }

    os.rename(old_path, new_path)

    return {
        "status": "ok",
        "message": f"{oldname} renamed to {newname}."
    }

@mcp.tool()
def plot_data(
    x_values: list,
    y_values: list,
    title: str,
    xtitle: str,
    ytitle: str,
    plot_type: str
):
    """Plots the desired data. plot type can be line, scatter, or bar."""
    plot_funcs = {
        "line": lambda: plt.plot(x_values, y_values, marker='o'),
        "scatter": lambda: plt.scatter(x_values, y_values),
        "bar": lambda: plt.bar(x_values, y_values),
    }

    if plot_type not in plot_funcs:
        raise ValueError("plot_type 'line', 'scatter' veya 'bar' olmalı")

    plt.figure()
    plot_funcs[plot_type]()

    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Server Started Manually!")
    mcp.run()
    print("Server Closed Manually!")