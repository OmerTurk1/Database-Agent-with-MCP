from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("Database Manager")

@mcp.tool()
def list_database_tables():
    """Returns the list of all the tables in the database."""
    return tools.show_tables()

@mcp.tool()
def get_table_schema(table_name: str):
    """Returns the related table's column names and features."""
    return tools.table_info(table_name)

@mcp.tool()
def execute_query(sql_command: str):
    """Takes the sql commands from LLM and runs it on the database, then returns the output."""
    try:
        result = tools.execute_query(sql_command)
        return {"sql": sql_command, "result": result}
    except Exception as e:
        return f"Error occurred: {str(e)} | Executed SQL: {sql_command}"

if __name__ == "__main__":
    print("Server Started Manually!")
    mcp.run()
    print("Server Closed Manually!")