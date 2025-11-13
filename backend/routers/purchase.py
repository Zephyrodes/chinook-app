from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import SessionLocal
from datetime import datetime
import json

router = APIRouter(prefix="/purchase", tags=["purchase"])

class PurchaseRequest(BaseModel):
    customer_id: int
    track_ids: list[int]
    billing_address: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def make_purchase(req: PurchaseRequest, db=Depends(get_db)):
    # Simple transactional pattern: insert Invoice + InvoiceLine, then outbox event
    conn = db.bind.raw_connection()
    try:
        cur = conn.cursor()
        # Insert Invoice
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO Invoice (CustomerId, InvoiceDate, BillingAddress, Total) VALUES (%s,%s,%s,%s)",
                    (req.customer_id, now, req.billing_address, 0.0))
        invoice_id = cur.lastrowid
        total = 0.0
        for tid in req.track_ids:
            cur.execute("SELECT UnitPrice FROM Track WHERE TrackId=%s", (tid,))
            row = cur.fetchone()
            if not row:
                conn.rollback()
                raise HTTPException(status_code=404, detail=f"Track {tid} not found")
            price = float(row[0])
            total += price
            cur.execute("INSERT INTO InvoiceLine (InvoiceId, TrackId, UnitPrice, Quantity) VALUES (%s,%s,%s,%s)",
                        (invoice_id, tid, price, 1))
        cur.execute("UPDATE Invoice SET Total=%s WHERE InvoiceId=%s", (total, invoice_id))
        # Write outbox event (atomic inside same txn)
        payload = json.dumps({"invoice_id": invoice_id, "customer_id": req.customer_id,
                              "track_ids": req.track_ids, "total": total, "invoice_date": now})
        cur.execute("INSERT INTO outbox_events (event_type, payload, created_at) VALUES (%s,%s,%s)",
                    ("purchase", payload, now))
        conn.commit()
        return {"invoice_id": invoice_id, "total": total}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
