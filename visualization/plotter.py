
import matplotlib.pyplot as plt
import os

def try_generate_plot(columns, rows, question):
    try:
        if len(columns) == 2 and len(rows) <= 20:
            x = [r[0] for r in rows]
            y = [r[1] for r in rows]
            plt.figure(figsize=(8,5))
            plt.bar(x, y, color='skyblue')
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])
            plt.title(question)
            path = os.path.join("visualization", "last_plot.png")
            plt.tight_layout()
            plt.savefig(path)
            return f"/static/last_plot.png"
        return None
    except Exception as e:
        print("Plot error:", e)
        return None
