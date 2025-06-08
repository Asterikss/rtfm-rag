import ast
import sys

import dash
from dash import Input, Output, dcc, html
import numpy as np
import pandas as pd
import plotly.express as px
from result import Err
import umap

from src.services.database_service import get_database_connection


app = dash.Dash(__name__)


def setup_data():
  conn_result = get_database_connection()
  if isinstance(conn_result, Err):
    print(conn_result.err())
    sys.exit(1)
  conn = conn_result.ok()

  cur = conn.cursor()
  cur.execute("""
        SELECT c.id, c.content, c.embedding, c.url, c.index_id, i.name as index_name
        FROM chunks c
        JOIN indexes i ON c.index_id = i.id
    """)
  rows = cur.fetchall()
  cur.close()
  conn.close()

  df = pd.DataFrame(
    rows,
    columns=["id", "content", "embedding", "url", "index_id", "index_name"],  # type: ignore
  )
  df["embedding"] = df["embedding"].apply(
    lambda x: np.array(ast.literal_eval(x), dtype=np.float32)
  )
  embeddings = np.stack(df["embedding"].values)  # type: ignore

  # Dimensionality reduction
  reducer = umap.UMAP(n_components=3, random_state=42)
  embedding_3d = reducer.fit_transform(embeddings)
  df["x"] = embedding_3d[:, 0]  # type: ignore
  df["y"] = embedding_3d[:, 1]  # type: ignore
  df["z"] = embedding_3d[:, 2]  # type: ignore

  fig = px.scatter_3d(
    df,
    x="x",
    y="y",
    z="z",
    color="index_name",
    hover_data=["content", "url"],
    title="Chunks in Embedding Space",
  )

  fig.update_layout(
    paper_bgcolor="#332726",
    plot_bgcolor="#332726",
    scene=dict(
      xaxis=dict(backgroundcolor="#332726"),
      yaxis=dict(backgroundcolor="#332726"),
      zaxis=dict(backgroundcolor="#332726"),
    ),
  )

  app.layout = html.Div(
    [
      html.H2("3D Embedding Explorer"),
      dcc.Graph(
        id="embedding-3d",
        figure=fig,
        style={"height": "80vh"},
      ),
      html.Div(id="chunk-info", style={"marginTop": 20}),
    ],
    style={"backgroundColor": "#332726"},
  )


@app.callback(Output("chunk-info", "children"), Input("embedding-3d", "clickData"))
def display_chunk_info(clickData):
  if clickData and "points" in clickData:
    point = clickData["points"][0]
    content = point["customdata"][0]
    url = point["customdata"][1]
    return html.Div(
      [
        html.H4("Chunk Details"),
        html.P(content),
        html.A("Source", href=url, target="_blank"),
      ]
    )
  return "Click a point to see details."


if __name__ == "__main__":
  setup_data()
  app.run(debug=True)
