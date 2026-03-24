from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError, RevokedIdTokenError

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.firebase import get_firebase_app
from app.core.logging import get_logger
from app.schemas.auth import AuthenticatedUser

logger = get_logger(__name__)


class FirebaseAuthService:
    def verify_id_token(self, id_token: str) -> AuthenticatedUser:
        settings = get_settings()
        get_firebase_app()

        try:
            decoded = auth.verify_id_token(id_token, check_revoked=True)
        except (InvalidIdTokenError, RevokedIdTokenError) as exc:
            logger.warning(
                "Firebase token rejected by admin SDK",
                extra={"event": "firebase_token_rejected", "context": {"reason": exc.__class__.__name__}},
            )
            raise AuthenticationError() from exc
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Unexpected Firebase token validation failure",
                extra={"event": "firebase_token_validation_failure", "context": {}},
            )
            raise AuthenticationError("Unable to validate Firebase token") from exc

        expected_issuer = f"https://securetoken.google.com/{settings.firebase_project_id}"
        token_audience = decoded.get("aud")
        token_issuer = decoded.get("iss")
        token_subject = decoded.get("sub")

        if token_audience != settings.firebase_project_id:
            logger.warning(
                "Firebase token rejected because of audience mismatch",
                extra={"event": "firebase_token_invalid_audience", "context": {"aud": token_audience}},
            )
            raise AuthenticationError("Invalid Firebase token audience")

        if token_issuer != expected_issuer:
            logger.warning(
                "Firebase token rejected because of issuer mismatch",
                extra={"event": "firebase_token_invalid_issuer", "context": {"iss": token_issuer}},
            )
            raise AuthenticationError("Invalid Firebase token issuer")

        if not token_subject or not isinstance(token_subject, str):
            logger.warning(
                "Firebase token rejected because subject is missing",
                extra={"event": "firebase_token_invalid_subject", "context": {}},
            )
            raise AuthenticationError("Invalid Firebase token subject")

        logger.info(
            "Firebase token validated",
            extra={"event": "firebase_token_validated", "context": {"uid": decoded['uid']}},
        )
        return AuthenticatedUser(
            uid=decoded["uid"],
            email=decoded.get("email"),
            name=decoded.get("name"),
            picture=decoded.get("picture"),
            tenant_id=decoded.get("tenant_id") or decoded.get("tenantId"),
            role=decoded.get("role"),
            provider=decoded.get("firebase", {}).get("sign_in_provider"),
            claims=decoded,
        )
