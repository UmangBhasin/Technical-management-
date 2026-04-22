from sqlalchemy.orm import Session

from app.core.config import ADMIN_DEFAULT_EMAIL, ADMIN_DEFAULT_NAME, ADMIN_DEFAULT_PASSWORD
from app.core.security import hash_password
from app.models.user import User


class BootstrapService:
    @staticmethod
    def seed_admin_user(db: Session) -> None:
        existing_admin = db.query(User).filter(User.email == ADMIN_DEFAULT_EMAIL).first()
        if existing_admin:
            return

        admin_user = User(
            full_name=ADMIN_DEFAULT_NAME,
            email=ADMIN_DEFAULT_EMAIL,
            password_hash=hash_password(ADMIN_DEFAULT_PASSWORD),
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
