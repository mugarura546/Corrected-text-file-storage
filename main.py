def save_records(store, filename=DATA_FILE):
    temp = filename + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        for r in store.values():
            f.write(f"{r['id']},{r['customer']},{r['point']},"
                    f"{r['quantity']},{r['amount']}\n")
    os.replace(temp, filename)

def load_records(filename=DATA_FILE, reject_file=REJECT_FILE):
    store, rejected = {}, []
    if not os.path.exists(filename):          # first run: no file yet
        return store, rejected
    with open(filename, "r", encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            fields = [p.strip() for p in line.split(",")]
            if len(fields) != 5:
                rejected.append((number, line, f"expected 5 fields, found {len(fields)}"))
                continue
            tid, customer, point, quantity, _stored_amount = fields
            ok, result = register_transaction(store, tid, customer, point, quantity)
            if not ok:
                rejected.append((number, line, result))
    if rejected:
        with open(reject_file, "a", encoding="utf-8") as log:
            for number, line, reason in rejected:
                log.write(f"line {number}: {line}  <-- {reason}\n")
    return store, rejected
