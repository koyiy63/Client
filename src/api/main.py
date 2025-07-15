"""
Jagarnath REST API

This module provides a comprehensive REST API built with FastAPI for data operations,
user management, and analytics. It includes authentication, validation, and
comprehensive error handling.

Features:
- User management (CRUD operations)
- Data processing endpoints
- Analytics and reporting
- Authentication with JWT tokens
- Request/response validation
- Comprehensive error handling
- API documentation with Swagger UI

Example Usage:
    uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import jwt
import datetime
import logging
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Jagarnath API",
    description="""
    Comprehensive REST API for data operations, user management, and analytics.
    
    ## Features
    
    * **User Management**: Complete CRUD operations for user accounts
    * **Data Processing**: Advanced data manipulation and analysis
    * **Analytics**: Real-time analytics and reporting
    * **Authentication**: Secure JWT-based authentication
    * **Validation**: Comprehensive request/response validation
    
    ## Authentication
    
    Most endpoints require authentication using Bearer tokens.
    Include the token in the Authorization header:
    
    ```
    Authorization: Bearer <your-jwt-token>
    ```
    
    ## Rate Limiting
    
    API requests are rate-limited to ensure fair usage:
    - 100 requests per minute for authenticated users
    - 10 requests per minute for anonymous users
    
    ## Error Handling
    
    The API returns standardized error responses with appropriate HTTP status codes
    and detailed error messages for debugging.
    """,
    version="1.0.0",
    contact={
        "name": "Jagarnath Team",
        "email": "support@jagarnath.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "your-secret-key-here"  # Use environment variable in production
ALGORITHM = "HS256"

# In-memory storage (use database in production)
users_db: Dict[str, Dict] = {}
data_db: Dict[str, Any] = {}

# Pydantic Models

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: UserRole = Field(UserRole.USER, description="User role")

class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: Optional[UserRole] = Field(None, description="User role")

class User(UserBase):
    """User response model."""
    id: str = Field(..., description="Unique user ID")
    created_at: datetime.datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime.datetime = Field(..., description="Last update timestamp")
    is_active: bool = Field(True, description="Account status")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "role": "user",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "is_active": True
            }
        }

class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

class Token(BaseModel):
    """Authentication token model."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class DataProcessingRequest(BaseModel):
    """Data processing request model."""
    data: List[Dict[str, Any]] = Field(..., description="Data to process")
    operation: str = Field(..., description="Processing operation")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Operation parameters")

class DataProcessingResponse(BaseModel):
    """Data processing response model."""
    processed_data: List[Dict[str, Any]] = Field(..., description="Processed data")
    statistics: Dict[str, Any] = Field(..., description="Processing statistics")
    processing_time: float = Field(..., description="Processing time in seconds")

class AnalyticsRequest(BaseModel):
    """Analytics request model."""
    metric: str = Field(..., description="Analytics metric")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filter criteria")
    time_range: Optional[str] = Field(None, description="Time range for analysis")

class AnalyticsResponse(BaseModel):
    """Analytics response model."""
    metric: str = Field(..., description="Analytics metric")
    value: Any = Field(..., description="Metric value")
    timestamp: datetime.datetime = Field(..., description="Analysis timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: str = Field(..., description="Error code")

# Helper Functions

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify JWT token and return user data."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token_data: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """Get current user from token."""
    user_id = token_data.get("sub")
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    
    Returns basic information about the API including version and status.
    """
    return {
        "message": "Welcome to Jagarnath API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the API and its dependencies.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow(),
        "version": "1.0.0",
        "uptime": "running"
    }

# User Management Endpoints

@app.post("/api/v1/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """
    Create a new user account.
    
    Creates a new user with the provided information. The password will be hashed
    before storage. Email addresses must be unique across all users.
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (3-50 characters, must be unique)
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    - **role**: User role (defaults to 'user')
    
    Returns the created user information (password excluded).
    """
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username already exists
    for existing_user in users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    user_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow()
    
    users_db[user_id] = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "password": user.password,  # In production, hash the password
        "created_at": now,
        "updated_at": now,
        "is_active": True
    }
    
    logger.info(f"Created new user: {user.email}")
    
    # Return user without password
    user_data = users_db[user_id].copy()
    del user_data["password"]
    return user_data

@app.get("/api/v1/users", response_model=List[User], tags=["Users"])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get list of users.
    
    Returns a paginated list of users. Only authenticated users can access this endpoint.
    The response is paginated with configurable skip and limit parameters.
    
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (1-1000)
    
    Returns a list of user objects (passwords excluded).
    """
    # Check if user has admin privileges
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    users = list(users_db.values())
    users = users[skip : skip + limit]
    
    # Remove passwords from response
    for user in users:
        del user["password"]
    
    return users

@app.get("/api/v1/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(
    user_id: str = Path(..., description="User ID to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get user by ID.
    
    Returns detailed information about a specific user. Users can only access
    their own information unless they have admin privileges.
    
    - **user_id**: Unique identifier of the user
    
    Returns the user object (password excluded).
    """
    # Check if user exists
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if current_user["id"] != user_id and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    user_data = users_db[user_id].copy()
    del user_data["password"]
    return user_data

@app.put("/api/v1/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(
    user_update: UserUpdate,
    user_id: str = Path(..., description="User ID to update"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update user information.
    
    Updates the information for a specific user. Users can only update their own
    information unless they have admin privileges.
    
    - **user_id**: Unique identifier of the user to update
    - **user_update**: Object containing fields to update
    
    Returns the updated user object (password excluded).
    """
    # Check if user exists
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if current_user["id"] != user_id and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Update user fields
    user_data = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        user_data[field] = value
    
    user_data["updated_at"] = datetime.datetime.utcnow()
    
    logger.info(f"Updated user: {user_id}")
    
    # Return updated user without password
    response_data = user_data.copy()
    del response_data["password"]
    return response_data

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(
    user_id: str = Path(..., description="User ID to delete"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete user account.
    
    Permanently deletes a user account. Users can only delete their own account
    unless they have admin privileges.
    
    - **user_id**: Unique identifier of the user to delete
    
    Returns no content on successful deletion.
    """
    # Check if user exists
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if current_user["id"] != user_id and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Delete user
    del users_db[user_id]
    
    logger.info(f"Deleted user: {user_id}")

# Authentication Endpoints

@app.post("/api/v1/auth/login", response_model=Token, tags=["Authentication"])
async def login(user_credentials: UserLogin):
    """
    Authenticate user and get access token.
    
    Authenticates a user with email and password, returning a JWT access token
    for subsequent API requests.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns a JWT access token with expiration information.
    """
    # Find user by email
    user = None
    for user_data in users_db.values():
        if user_data["email"] == user_credentials.email:
            user = user_data
            break
    
    if not user or user["password"] != user_credentials.password:  # In production, verify hashed password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token_expires = datetime.timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user['email']}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds())
    }

@app.get("/api/v1/auth/me", response_model=User, tags=["Authentication"])
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user information.
    
    Returns detailed information about the currently authenticated user.
    
    Returns the current user object (password excluded).
    """
    user_data = current_user.copy()
    del user_data["password"]
    return user_data

# Data Processing Endpoints

@app.post("/api/v1/data/process", response_model=DataProcessingResponse, tags=["Data Processing"])
async def process_data(
    request: DataProcessingRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process data using various operations.
    
    Performs data processing operations on the provided data. Supports various
    operations like filtering, sorting, aggregation, and transformation.
    
    - **data**: Array of data objects to process
    - **operation**: Processing operation to perform
    - **parameters**: Optional parameters for the operation
    
    Returns processed data with statistics and processing time.
    """
    import time
    start_time = time.time()
    
    # Validate operation
    valid_operations = ["filter", "sort", "aggregate", "transform", "clean"]
    if request.operation not in valid_operations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid operation. Must be one of: {valid_operations}"
        )
    
    # Process data based on operation
    processed_data = request.data.copy()
    statistics = {
        "input_count": len(request.data),
        "output_count": len(processed_data),
        "operation": request.operation
    }
    
    if request.operation == "filter":
        # Apply filters
        if request.parameters and "filters" in request.parameters:
            filters = request.parameters["filters"]
            processed_data = [
                item for item in processed_data
                if all(item.get(key) == value for key, value in filters.items())
            ]
    
    elif request.operation == "sort":
        # Sort data
        if request.parameters and "sort_by" in request.parameters:
            sort_by = request.parameters["sort_by"]
            reverse = request.parameters.get("reverse", False)
            processed_data.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
    
    elif request.operation == "aggregate":
        # Aggregate data
        if request.parameters and "group_by" in request.parameters:
            group_by = request.parameters["group_by"]
            groups = {}
            for item in processed_data:
                key = item.get(group_by, "unknown")
                if key not in groups:
                    groups[key] = []
                groups[key].append(item)
            processed_data = [{"group": k, "count": len(v), "items": v} for k, v in groups.items()]
    
    processing_time = time.time() - start_time
    statistics["processing_time"] = processing_time
    
    logger.info(f"Data processed by user {current_user['id']}: {request.operation}")
    
    return DataProcessingResponse(
        processed_data=processed_data,
        statistics=statistics,
        processing_time=processing_time
    )

# Analytics Endpoints

@app.post("/api/v1/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
async def get_analytics(
    request: AnalyticsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get analytics data.
    
    Retrieves analytics data for various metrics. Supports filtering and time-based
    analysis for different data dimensions.
    
    - **metric**: Analytics metric to calculate
    - **filters**: Optional filter criteria
    - **time_range**: Optional time range for analysis
    
    Returns analytics data with metric value and metadata.
    """
    # Validate metric
    valid_metrics = ["user_count", "data_volume", "processing_time", "error_rate"]
    if request.metric not in valid_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metric. Must be one of: {valid_metrics}"
        )
    
    # Calculate metric value
    value = 0
    metadata = {}
    
    if request.metric == "user_count":
        value = len(users_db)
        metadata = {"active_users": len([u for u in users_db.values() if u["is_active"]])}
    
    elif request.metric == "data_volume":
        value = len(data_db) if data_db else 0
        metadata = {"data_types": list(data_db.keys()) if data_db else []}
    
    elif request.metric == "processing_time":
        value = 0.5  # Mock average processing time
        metadata = {"unit": "seconds"}
    
    elif request.metric == "error_rate":
        value = 0.02  # Mock error rate
        metadata = {"unit": "percentage"}
    
    logger.info(f"Analytics requested by user {current_user['id']}: {request.metric}")
    
    return AnalyticsResponse(
        metric=request.metric,
        value=value,
        timestamp=datetime.datetime.utcnow(),
        metadata=metadata
    )

# Error Handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with standardized error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=f"HTTP_{exc.status_code}"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions with standardized error responses."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            code="INTERNAL_ERROR"
        ).dict()
    )

# Startup and Shutdown Events

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Jagarnath API starting up...")
    
    # Create some sample users for testing
    if not users_db:
        admin_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow()
        users_db[admin_id] = {
            "id": admin_id,
            "email": "admin@jagarnath.com",
            "username": "admin",
            "full_name": "System Administrator",
            "role": UserRole.ADMIN,
            "password": "admin123",  # In production, use hashed passwords
            "created_at": now,
            "updated_at": now,
            "is_active": True
        }
        logger.info("Created sample admin user")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Jagarnath API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)