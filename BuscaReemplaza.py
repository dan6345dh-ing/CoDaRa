import csv

# CSV con reglas de reemplazo
rules_file = "reglas.csv"
# CSV de entrada que quieres procesar
input_file = "entrada.csv"
# CSV de salida ya modificado
output_file = "salida.csv"

# --- Leer reglas ---
rules = {}
with open(rules_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # saltar encabezado si lo tiene
    for row in reader:
        if len(row) >= 2:
            buscar, reemplazar = row[0], row[1]
            rules[buscar] = reemplazar

# --- Procesar archivo ---
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", newline="", encoding="utf-8") as fout:
    
    reader = csv.reader(fin)
    writer = csv.writer(fout)

    for row in reader:
        new_row = [rules.get(cell, cell) for cell in row]
        writer.writerow(new_row)

print("✅ CSV procesado y guardado en:", output_file)
