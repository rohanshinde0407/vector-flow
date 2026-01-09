from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get("/")
def read_root():
    return {"Ping": "Pong"}

@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)

    graph = {node.id: [] for node in pipeline.nodes}

    for edge in pipeline.edges:
        graph[edge.source].append(edge.target)

    visited = set()
    stack = set()

    def has_cycle(v):
        if v in stack:
            return True
        if v in visited:
            return False

        visited.add(v)
        stack.add(v)

        for n in graph[v]:
            if has_cycle(n):
                return True

        stack.remove(v)
        return False

    is_dag = True
    for node in graph:
        if has_cycle(node):
            is_dag = False
            break

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
