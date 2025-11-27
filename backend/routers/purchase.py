from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from .. import schemas
from .. import models
from ..database import get_db

router = APIRouter()

@router.post("/buy", response_model=schemas.PurchaseResponse)
def create_purchase(req: schemas.PurchaseRequest, db: Session = Depends(get_db)):
    """
    Crea una factura (invoice) y sus invoice lines atomically.
    - req.customer_id debe existir.
    - lines es lista de {track_id, quantity}
    """
    # Validar cliente
    customer = db.query(models.Customer).filter(models.Customer.CustomerId == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if not req.lines or len(req.lines) == 0:
        raise HTTPException(status_code=400, detail="No se proporcionaron líneas de compra")

    # Cálculo del total y creación de invoice dentro de una transacción
    try:
        # start transaction block
        total = Decimal("0.00")
        invoice = models.Invoice(
            CustomerId=req.customer_id,
            InvoiceDate=datetime.utcnow(),
            BillingAddress=req.billing_address,
            BillingCity=req.billing_city,
            BillingCountry=req.billing_country,
            Total=Decimal("0.00"),  # set later
        )
        db.add(invoice)
        db.flush()  # asegura invoice.InvoiceId disponible

        for line in req.lines:
            track = db.query(models.Track).filter(models.Track.TrackId == line.track_id).with_for_update().first()
            if not track:
                raise HTTPException(status_code=404, detail=f"Track {line.track_id} no encontrado")

            # Unit price from track.UnitPrice (Decimal-like)
            unit_price = Decimal(str(track.UnitPrice))
            line_total = (unit_price * Decimal(line.quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total += line_total

            invoice_line = models.InvoiceLine(
                InvoiceId=invoice.InvoiceId,
                TrackId=track.TrackId,
                UnitPrice=unit_price,
                Quantity=line.quantity,
            )
            db.add(invoice_line)

        # persist totals
        invoice.Total = total
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        return schemas.PurchaseResponse(
            invoice_id=invoice.InvoiceId,
            total=invoice.Total,
            created_at=invoice.InvoiceDate,
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creando la compra") from e

@router.get("/purchase/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.Invoice).filter(models.Invoice.InvoiceId == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice no encontrado")
    # serializar manualmente para no necesitar schema extenso
    return {
        "InvoiceId": inv.InvoiceId,
        "CustomerId": inv.CustomerId,
        "InvoiceDate": inv.InvoiceDate,
        "Total": float(inv.Total),
        "lines": [
            {"TrackId": l.TrackId, "UnitPrice": float(l.UnitPrice), "Quantity": l.Quantity} for l in inv.lines
        ],
    }
