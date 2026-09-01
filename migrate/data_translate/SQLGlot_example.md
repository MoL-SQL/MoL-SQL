# **show a example use sqlglot to generate sql syntax tree**

[https://gemini.google.com/app/e4dcd7b77844016e](https://gemini.google.com/app/e4dcd7b77844016e)

*User prompt: show a example use sqlglot to generate sql syntax tree*

Response: Here is an example of how to use **SQLGlot** to parse a SQL statement into an Abstract Syntax Tree (AST) and interact with it.

SQLGlot represents every part of your SQL query (like SELECT, WHERE, column names, and table names) as a distinct expression object in a hierarchical tree.

### **Parsing SQL into a Syntax Tree**

You can use the parse\_one function to convert a SQL string into a syntax tree. Printing the repr() of the resulting object will reveal the deeply nested structure of the AST.

`import sqlglot`  
`from sqlglot import exp`

`# Define your SQL query`  
`sql = "SELECT id, amount + 10 AS total FROM sales WHERE amount > 100"`

`# Parse the SQL statement into an Abstract Syntax Tree (AST)`  
`ast = sqlglot.parse_one(sql)`

`# 1. Print the full syntax tree representation`  
`print("--- AST Representation ---")`  
`print(repr(ast))`

**Output of the AST Representation:**

`Select(`  
  `expressions=[`  
    `Column(`  
      `this=Identifier(this=id, quoted=False)),`  
    `Alias(`  
      `this=Add(`  
        `this=Column(`  
          `this=Identifier(this=amount, quoted=False)),`  
        `expression=Literal(this=10, is_string=False)),`  
      `alias=Identifier(this=total, quoted=False))],`  
  `from=From(`  
    `this=Table(`  
      `this=Identifier(this=sales, quoted=False))),`  
  `where=Where(`  
    `this=GT(`  
      `this=Column(`  
        `this=Identifier(this=amount, quoted=False)),`  
      `expression=Literal(this=100, is_string=False)))`  
`)`

### **Traversing the Syntax Tree**

Once you have generated the syntax tree, the real power of SQLGlot is the ability to traverse it programmatically. You can use the .find\_all() method to search the tree for specific node types, like extracting every column or table referenced in the query.

`# 2. Traverse the tree to find all Tables`  
`print("\n--- Tables found in AST ---")`  
`for table in ast.find_all(exp.Table):`  
    `print(f"Table Name: {table.name}")`

`# 3. Traverse the tree to find all Columns`  
`print("\n--- Columns found in AST ---")`  
`for column in ast.find_all(exp.Column):`  
    `print(f"Column Name: {column.name}")`

**Output of the Traversal:**

`--- Tables found in AST ---`  
`Table Name: sales`

`--- Columns found in AST ---`  
`Column Name: id`  
`Column Name: amount`  
`Column Name: amount`

**Sources**

1. [sqlglot/posts/ast\_primer.md at main \- GitHub](https://github.com/tobymao/sqlglot/blob/main/posts/ast_primer.md)  
2. [sqlglot API documentation](https://sqlglot.com/)

---

*User prompt: can it get which column belong to which table?*

Response: Yes, SQLGlot can determine which column belongs to which table, but **how** it does this depends on whether your SQL query explicitly includes the table names (e.g., sales.id) or leaves them out (e.g., just id).

If your query uses unqualified columns (just id instead of table.id), SQLGlot cannot magically know where it came from just by reading the string — it needs to know your database schema.

SQLGlot has a built-in optimizer tool called qualify\_columns that takes your query, compares it against a schema you provide, and automatically attaches the correct table name to every column in the syntax tree.

Here is an example of how to resolve column lineage using a schema:

`import sqlglot`  
`from sqlglot import exp`  
`from sqlglot.optimizer.qualify_columns import qualify_columns`

`# A query where the SELECT columns don't specify their tables`  
`sql = """`  
`SELECT id, amount, customer_name`   
`FROM sales`   
`JOIN customers ON sales.customer_id = customers.id`  
`"""`

`# 1. Define your database schema (Tables and their Columns)`  
`schema = {`  
    `"sales": {"id": "INT", "amount": "FLOAT", "customer_id": "INT"},`  
    `"customers": {"id": "INT", "customer_name": "VARCHAR"}`  
`}`

`# 2. Parse the SQL into an AST`  
`ast = sqlglot.parse_one(sql)`

`# 3. Use the optimizer to "qualify" the columns using the schema`  
`# This modifies the AST so every Column node gets linked to its explicit Table`  
`qualified_ast = qualify_columns(expression=ast, schema=schema)`

`print("--- Resolved Column Lineage ---")`

`# 4. Traverse the qualified tree to extract the Table -> Column mapping`  
`for column in qualified_ast.find_all(exp.Column):`  
    `# 'table' extracts the table identifier from the column node`  
    `table_name = column.table`   
    `column_name = column.name`  
    `print(f"Table: {table_name:<10} -> Column: {column_name}")`

**Output:**

`--- Resolved Column Lineage ---`  
`Table: sales      -> Column: id`  
`Table: sales      -> Column: amount`  
`Table: customers  -> Column: customer_name`  
`Table: sales      -> Column: customer_id`  
`Table: customers  -> Column: id`

### **How this works under the hood**

1. **sqlglot.parse\_one()**: Initially creates a tree where Column(this=id) has no parent table attached to it.  
2. **qualify\_columns()**: Scans the FROM and JOIN clauses in the AST, looks up those tables in the schema dictionary, and resolves ambiguities (like id, which exists in both tables). It rewrites the AST node to be Column(this=id, table=sales).  
3. **column.table**: Safely extracts the table prefix from the AST node after it has been explicitly mapped.

If your original SQL already explicitly defines the tables (e.g., SELECT s.id FROM sales s), you can skip the schema and qualify\_columns step entirely, and just call column.table directly on your parsed AST.

---

*User prompt: what is the sql has sub-query and give name to joint tables*

Response: When your SQL query contains sub-queries (derived tables) and aliases (like AS t1), the columns in your final SELECT statement are technically pulling from those temporary aliases, not the underlying database tables.

SQLGlot handles this beautifully, but it requires a slightly different approach depending on what you want to achieve.

You have two main tools here:

1. **qualify**: Resolves every column to its immediate scope (e.g., matching a column to the alias t1).  
2. **lineage**: A specialized tool in SQLGlot that traces a column through all sub-queries and aliases back to its **original source table**.

Here is how you can handle sub-queries and aliases, and trace exactly where a column originated.

### **Example: Tracing Columns through Sub-queries and Aliases**

`import sqlglot`  
`from sqlglot import exp`  
`from sqlglot.optimizer.qualify import qualify`  
`from sqlglot.lineage import lineage`

`# A query with a sub-query (aliased as 'dev') and a JOIN (aliased as 'd')`  
`sql = """`  
`SELECT dev.emp_id, d.department_name`  
`FROM (`  
    `SELECT id AS emp_id, dept_id`   
    `FROM employees`   
    `WHERE role = 'Developer'`  
`) AS dev`  
`JOIN departments AS d ON dev.dept_id = d.id`  
`"""`

`# 1. Define the base schema`  
`schema = {`  
    `"employees": {"id": "INT", "dept_id": "INT", "role": "VARCHAR"},`  
    `"departments": {"id": "INT", "department_name": "VARCHAR"}`  
`}`

`# 2. Parse and qualify the AST`  
`ast = sqlglot.parse_one(sql)`  
`qualified_ast = qualify(ast, schema=schema)`

`print("--- Immediate Column Lineage (AST scopes) ---")`  
`for column in qualified_ast.find_all(exp.Column):`  
    `print(f"Scope/Table: {column.table:<12} -> Column: {column.name}")`

**Output of AST Scopes:**

`--- Immediate Column Lineage (AST scopes) ---`  
`Scope/Table: dev          -> Column: emp_id`  
`Scope/Table: d            -> Column: department_name`  
`Scope/Table: employees    -> Column: id`  
`Scope/Table: employees    -> Column: dept_id`  
`Scope/Table: employees    -> Column: role`  
`Scope/Table: dev          -> Column: dept_id`  
`Scope/Table: d            -> Column: id`

*(Notice how the AST knows emp\_id comes from the dev sub-query, while id inside the sub-query comes from employees.)*

### **Finding the Root Source Table (Data Lineage)**

If your goal is to find out that the final emp\_id actually originates from employees.id, extracting scopes isn't enough. You need to use SQLGlot's lineage module, which recursively climbs down the syntax tree.

`print("\n--- Tracing Root Source via Lineage ---")`

`# 3. Trace the lineage of 'emp_id' in the final SELECT statement`  
`# We pass the column name, the full query, and the schema`  
`node = lineage("emp_id", sql, schema=schema)`

`# node represents the final column. We can traverse down to its source.`  
`def print_source(node, depth=0):`  
    `indent = "  " * depth`  
    `# If the node is a Table, we found the root source!`  
    `if isinstance(node.expression, exp.Table):`  
        `print(f"{indent}Root Source -> Table: {node.expression.name}")`  
    `else:`  
        `# Otherwise, print the current step and keep going deeper`  
        `print(f"{indent}Alias/Step -> {node.name}")`  
        `for child_node in node.downstream:`  
            `print_source(child_node, depth + 1)`

`print_source(node)`

**Output of Lineage Trace:**

`--- Tracing Root Source via Lineage ---`  
`Alias/Step -> emp_id`  
  `Alias/Step -> id`  
    `Root Source -> Table: employees`

### **Why this matters**

* **qualify (AST traversal):** Is best when you need to rewrite the query, validate that aliases are used correctly, or analyze the structure of the query itself. Notice we used qualify() here instead of qualify\_columns() — qualify() is a master function that runs several optimizers in order, ensuring sub-query scopes are properly resolved before trying to attach columns to them.  
* **lineage:** Is best when you are building data governance tools, impact analysis, or ETL pipelines where you need to know exactly which physical database table populated the final output column, regardless of how many sub-queries or AS aliases the SQL author used in between.

---

