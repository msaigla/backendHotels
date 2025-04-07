import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI(debug=True)


tables = [
    {"id": 1, "title": "Table 1", "description": "столик у окна"},
    {"id": 2, "title": "Table 2", "description": "столик у двери"},
    {"id": 3, "title": "Table 3", "description": "столик у туалета"},
]


@app.get("/tables")
def get_tables():
    return tables


@app.delete("/tables/{table_id}")
def delete_table(table_id: int):
    global tables
    tables = [table for table in tables if table["id"] != table_id]
    return {"status": "OK"}


@app.post("/tables")
def create_table(
        title: str = Body(embed=True, description="Table title"),
):
    global tables
    tables.append({"id": tables[-1]["id"] + 1, "title": title})
    return {"status": "OK"}


@app.put("/tables/{table_id}")
def update_table(table_id: int,
                 title: str,
                 description: str):
    global tables
    for table in tables:
        if table["id"] == table_id:
            table["title"] = title
            table["description"] = description
    return {"status": "OK"}


@app.patch("/tables/{table_id}")
def update_table(table_id: int,
                 title: str | None = Body(default=None, embed=True, description="Table title"),
                 description: str | None = Body(default=None, embed=True, description="Table description")):
    for table in tables:
        if table["id"] == table_id:
            if title:
                table["title"] = title
            if description:
                table["description"] = description
    return {"status": "OK"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
