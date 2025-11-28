from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from .. import schemas, models
from ..database import get_db

router = APIRouter()

@router.post("/buy", response_model=schemas.PurchaseResponse)
def create_purchase(req: schemas.PurchaseRequest, db: Session = Depends(get_db)):
    """
    Crea una factura (Invoice) y sus InvoiceLine para registrar una compra.
    - req.customer_id debe existir.
    - lines es lista de {track_id, quantity}.
    """
    customer = db.query(models.Customer).filter(models.Customer.CustomerId == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if not req.lines or len(req.lines) == 0:
        raise HTTPException(status_code=400, detail="No se proporcionaron líneas de compra")

    try:
        total = Decimal("0.00")
        invoice = models.Invoice(
            CustomerId=req.customer_id,
            InvoiceDate=datetime.utcnow(),
            BillingAddress=req.billing_address,
            BillingCity=req.billing_city,
            BillingCountry=req.billing_country,
            Total=Decimal("0.00"),  # se actualizará después
        )
        db.add(invoice)
        db.flush()  # asegura InvoiceId disponible

        # Crear líneas de invoice y calcular total
        for line in req.lines:
            track = db.query(models.Track).filter(models.Track.TrackId == line.track_id).with_for_update().first()
            if not track:
                raise HTTPException(status_code=404, detail=f"Track {line.track_id} no encontrado")

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

        invoice.Total = total
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
