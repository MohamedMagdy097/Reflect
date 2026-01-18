from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.config import settings
from app.face_recognition import get_embedding, find_matching_user
from app.utils.image_processing import save_uploaded_image, cleanup_temp_image

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=schemas.SignupResponse)
async def signup(
    email: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Signup flow:
    1. Validate email format
    2. Check if email already exists
    3. Extract face embedding from image
    4. Check if face already exists (compare against ALL users)
    5. If face unique, create account
    """
    temp_image_path = None

    try:
        # 1. Check if email already exists
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # 2. Save uploaded image temporarily
        temp_image_path = await save_uploaded_image(image)

        # 3. Extract embedding
        try:
            new_embedding = get_embedding(temp_image_path)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        # 4. Get all existing users and check for face match
        all_users = db.query(models.User).all()
        user_data = [(u.id, u.email, u.embedding) for u in all_users]

        match = find_matching_user(new_embedding, user_data, settings.SIMILARITY_THRESHOLD)

        if match:
            user_id, matched_email, similarity = match
            raise HTTPException(
                status_code=409,
                detail=f"User is already signed up with email: {matched_email}"
            )

        # 5. Create new user
        new_user = models.User(
            email=email,
            embedding=new_embedding
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return schemas.SignupResponse(
            success=True,
            message="Account created successfully",
            user_id=new_user.id,
            email=new_user.email
        )

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

    finally:
        # Cleanup temporary image
        if temp_image_path:
            cleanup_temp_image(temp_image_path)


@router.post("/signin", response_model=schemas.SigninResponse)
async def signin(
    email: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Signin flow:
    1. Check if email exists
    2. Extract face embedding from image
    3. Compare against stored embedding for this email
    4. Also check if face matches different email
    """
    temp_image_path = None

    try:
        # 1. Check if email exists
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Email not registered"
            )

        # 2. Save uploaded image temporarily
        temp_image_path = await save_uploaded_image(image)

        # 3. Extract embedding
        try:
            signin_embedding = get_embedding(temp_image_path)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        # 4. Get all users to check for any face match
        all_users = db.query(models.User).all()
        user_data = [(u.id, u.email, u.embedding) for u in all_users]

        match = find_matching_user(signin_embedding, user_data, settings.SIMILARITY_THRESHOLD)

        if not match:
            raise HTTPException(
                status_code=401,
                detail="Face not recognized. Please try again."
            )

        matched_user_id, matched_email, similarity = match

        # 5. Check if matched face belongs to different email
        if matched_email != email:
            raise HTTPException(
                status_code=403,
                detail=f"User signed up with different email: {matched_email}"
            )

        # 6. Success - face matches the provided email
        return schemas.SigninResponse(
            success=True,
            message="Authentication successful",
            user_id=matched_user_id,
            email=matched_email,
            similarity_score=round(similarity, 4)
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signin failed: {str(e)}")

    finally:
        # Cleanup temporary image
        if temp_image_path:
            cleanup_temp_image(temp_image_path)


@router.get("/check-email")
async def check_email(email: str, db: Session = Depends(get_db)):
    """Check if email is already registered"""
    user = db.query(models.User).filter(models.User.email == email).first()
    return {"exists": user is not None}
