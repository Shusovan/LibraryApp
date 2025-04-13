from datetime import date, timedelta
import uuid
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional


from config.admin_client import borrow_approval_request
from config.book_client import fetch_book, update_book
from config.security_client import validate_token
# from event.kafka_producer import send_event
from model.borrow import BorrowRecords
from model.borrow_status import BorrowStatus


def borrow(request: Request, db: Session, book_id: str):
    """
    User requests to borrow a book. Store request in AdminService for approval.
    """

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService
    
    if user_data.get("role") != "USER":
        raise HTTPException(status_code=403, detail="Only USERS can borrow books")

    user_id = user_data.get("id")

    # Fetch book details
    book_data = fetch_book(book_id, auth_header)
    
    if not book_data or book_data.get("available_copies") < 1:
        raise HTTPException(status_code=400, detail="Book not available")


    # generate request ID
    request_id = str(uuid.uuid4())

    # save the borrow data in database
    save_borrow = BorrowRecords(user_id=user_id,
        book_id=book_id,
        request_id=request_id,
        borrow_date=date.today(),
        return_date=date.today() + timedelta(days=14),
        status="PENDING")

    # borrow request payload
    borrow_request_payload = {"request_id": request_id, "user_id": user_id, "book_id": book_id, "status": "PENDING"}
    
    # Send borrow approval request to Librarian in AdminService
    request_admin = borrow_approval_request(borrow_request_payload)

    if not request_admin:
        raise HTTPException(status_code=500, detail="Failed to send borrow request for approval")
    

    db.add(save_borrow)
    db.commit()
    db.refresh(save_borrow)

    # Notify Librarian for approval (via Kafka)
    # notify_librarian = {
    #     "message": f"User {user_id} requested to borrow book {book_id}. Please review the request.",
    #     "book_id": book_id,
    #     "user_id": user_id,
    #     "request_id": request_id
    # }

    # send_event("librarian.notification", notify_librarian)

    return {"message": f"Borrow request for book {book_id} sent. Awaiting librarian approval."}


def approved_borrow(request_id: str, approval_data: dict, db: Session):

    borrow_data = db.query(BorrowRecords).filter(BorrowRecords.request_id==request_id).first()

    if not borrow_data:
        raise HTTPException(status_code=404, detail="borrow data not found")
    
    book_id = borrow_data.book_id

    try:
        borrow_data.status = BorrowStatus[approval_data["status"]]  # Convert string to enum

    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid status value: {approval_data['status']}")

    db.commit()
    db.refresh(borrow_data)

    # Decrement available copies in BookService
    update_book_availability = update_book(book_id, status=borrow_data.status.value)

    if not update_book_availability:
        raise HTTPException(status_code=500, detail="Failed to update book availability")

    print(f"Message: Your book borrow request is {borrow_data.status.value}")

    return {"message": f"Your book borrow request is {borrow_data.status.value}"}


def book_return(request: Request, db: Session, book_id: str):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService
    
    if user_data.get("role") != "USER":
        raise HTTPException(status_code=403, detail="Only USERS can borrow books")
    
    user_id = user_data.get("id")
    
    # fetch bokk of a particular user
    borrow_data = db.query(BorrowRecords).filter(BorrowRecords.book_id==book_id, BorrowRecords.user_id==user_id).first()

    if not borrow_data:
        raise HTTPException(status_code=404, detail="You didn't borrow this book")

    borrow_data.status = BorrowStatus.RETURNED

    db.commit()
    db.refresh(borrow_data)

    # increment available copies in BookService
    update_book_availability = update_book(book_id, status=borrow_data.status.value)

    return {"message": f"Book {book_id} returned successfully",
            "book_status": borrow_data.status.value,
            "book_service_response": update_book_availability}


def borrowed_books(request: Request, db: Session):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService
    
    if user_data.get("role") != "USER":
        raise HTTPException(status_code=403, detail="Only USERS can borrow books")
    
    user_id = user_data.get("id")

    # fetch borrowed books of logged-in user user
    borrow_data = db.query(BorrowRecords).filter(BorrowRecords.user_id==user_id).first()

    return borrow_data


# include function to check the due_date and impose the fine