#!/usr/bin/env python3
"""
🔐 KMRL Authentication API
========================
FastAPI backend for user authentication with JWT tokens.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import timedelta
from pathlib import Path
import uvicorn

from auth_models import auth_manager, User
from inventory_management import InventoryManager

# Initialize FastAPI app
app = FastAPI(
    title="KMRL Authentication API",
    description="Authentication API for KMRL Fleet Optimization Dashboard",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Pydantic models
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    role: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

class MessageResponse(BaseModel):
    message: str
    success: bool

class InventoryPart(BaseModel):
    id: str
    name: str
    category: str
    available: int
    reorder_level: int
    status: str
    criticality: str
    supplier: str
    lead_time: int
    unit_cost: float

class InventorySummary(BaseModel):
    total_parts: int
    needs_reorder: int
    reorder_percentage: float
    critical_priority: int
    avg_lead_time_days: Optional[float]
    category_breakdown: Dict[str, int]
    supplier_breakdown: Dict[str, int]
    timestamp: str

class InventoryResponse(BaseModel):
    summary: InventorySummary
    parts: List[InventoryPart]
    success: bool

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    username = auth_manager.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = auth_manager.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure current user is admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

@app.post("/register", response_model=MessageResponse)
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    result = auth_manager.register_user(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password=user_data.password,
        role=user_data.role
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return MessageResponse(message=result["message"], success=True)

@app.post("/login", response_model=TokenResponse)
async def login_user(user_data: UserLogin):
    """Authenticate user and return JWT token"""
    user = auth_manager.authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth_manager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_manager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        role=user.role,
        created_at=user.created_at.isoformat() if user.created_at else None,
        last_login=user.last_login.isoformat() if user.last_login else None
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth_manager.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        user=user_response
    )

@app.post("/login/form")
async def login_form(username: str = Form(), password: str = Form()):
    """Form-based login for web integration"""
    user_data = UserLogin(username=username, password=password)
    return await login_user(user_data)

@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        role=current_user.role,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
        last_login=current_user.last_login.isoformat() if current_user.last_login else None
    )

@app.post("/logout", response_model=MessageResponse)
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (client should delete token)"""
    # In a stateless JWT system, logout is handled client-side by deleting the token
    # For session-based systems, we would invalidate the session here
    return MessageResponse(message="Logged out successfully", success=True)

@app.get("/users", response_model=list[UserResponse])
async def get_all_users(admin_user: User = Depends(get_admin_user)):
    """Get all users (admin only)"""
    users = auth_manager.get_all_users()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at.isoformat() if user.created_at else None,
            last_login=user.last_login.isoformat() if user.last_login else None
        ] for user in users
    ]

# --- INVENTORY MANAGEMENT ENDPOINTS ---

# Initialize inventory manager (singleton)
_inventory_manager = None

def get_inventory_manager() -> InventoryManager:
    """Get or create inventory manager instance."""
    global _inventory_manager
    if _inventory_manager is None:
        csv_path = Path('metro_spare_parts_inventory.csv')
        _inventory_manager = InventoryManager(csv_path)
        try:
            _inventory_manager.load_data()
            _inventory_manager.validate_data()
            _inventory_manager.analyze_reorder_needs()
        except Exception as e:
            print(f"Warning: Could not initialize inventory data: {e}")
            _inventory_manager = None
    return _inventory_manager

@app.get("/inventory/summary", response_model=InventorySummary)
async def get_inventory_summary(current_user: User = Depends(get_current_user)):
    """Get inventory summary statistics."""
    manager = get_inventory_manager()
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inventory service unavailable"
        )
    
    try:
        summary = manager.generate_summary()
        return InventorySummary(**summary)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating inventory summary: {str(e)}"
        )

@app.get("/inventory/parts", response_model=List[InventoryPart])
async def get_inventory_parts(
    category: Optional[str] = None,
    status: Optional[str] = None,
    criticality: Optional[str] = None,
    limit: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """Get inventory parts with optional filters."""
    manager = get_inventory_manager()
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inventory service unavailable"
        )
    
    try:
        data = manager.processed_data
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inventory data not processed"
            )
        
        # Apply filters
        filtered_data = data.copy()
        
        if category and category.lower() != 'all':
            filtered_data = filtered_data[filtered_data.get('Category', '') == category]
        
        if status and status.lower() != 'all':
            if status.lower() == 'needs_reorder':
                filtered_data = filtered_data[filtered_data['needs_reorder'] == True]
            elif status.lower() == 'sufficient':
                filtered_data = filtered_data[filtered_data['needs_reorder'] == False]
        
        if criticality and criticality.lower() != 'all':
            crit_col = manager._find_criticality_column()
            if crit_col:
                filtered_data = filtered_data[filtered_data[crit_col].str.lower() == criticality.lower()]
        
        # Limit results
        if limit:
            filtered_data = filtered_data.head(limit)
        
        # Convert to response format
        parts = []
        for _, row in filtered_data.iterrows():
            # Determine status
            part_status = 'sufficient'
            if row.get('needs_reorder', False):
                if row.get('Quantity_Available', 0) == 0:
                    part_status = 'critical'
                else:
                    part_status = 'reorder'
            
            parts.append(InventoryPart(
                id=str(row.get('Part_ID', '')),
                name=str(row.get('Part_Name', '')),
                category=str(row.get('Category', '')),
                available=int(row.get('Quantity_Available', 0)),
                reorder_level=int(row.get('Reorder_Level', 0)),
                status=part_status,
                criticality=str(row.get('Criticality_Level', 'Medium')),
                supplier=str(row.get('Supplier_Name', '')),
                lead_time=int(row.get('Lead_Time_Days', 0)),
                unit_cost=float(row.get('Unit_Cost', 0))
            ))
        
        return parts
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching inventory parts: {str(e)}"
        )

@app.get("/inventory/reorder-report", response_model=List[InventoryPart])
async def get_reorder_report(
    limit: Optional[int] = 20,
    current_user: User = Depends(get_current_user)
):
    """Get prioritized reorder report."""
    manager = get_inventory_manager()
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inventory service unavailable"
        )
    
    try:
        report = manager.get_reorder_report(limit=limit)
        
        parts = []
        for _, row in report.iterrows():
            # Determine status
            part_status = 'reorder'
            if row.get('Quantity_Available', 0) == 0:
                part_status = 'critical'
            
            parts.append(InventoryPart(
                id=str(row.get('Part_ID', '')),
                name=str(row.get('Part_Name', '')),
                category=str(row.get('Category', '')),
                available=int(row.get('Quantity_Available', 0)),
                reorder_level=int(row.get('Reorder_Level', 0)),
                status=part_status,
                criticality=str(row.get('Criticality_Level', 'Medium')),
                supplier=str(row.get('Supplier_Name', '')),
                lead_time=int(row.get('Lead_Time_Days', 0)),
                unit_cost=float(row.get('Unit_Cost', 0))
            ))
        
        return parts
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating reorder report: {str(e)}"
        )

@app.get("/inventory/refresh", response_model=MessageResponse)
async def refresh_inventory(
    admin_user: User = Depends(get_admin_user)
):
    """Refresh inventory data (admin only)."""
    global _inventory_manager
    try:
        _inventory_manager = None  # Reset the singleton
        manager = get_inventory_manager()  # Reinitialize
        
        if manager is None:
            return MessageResponse(
                message="Could not refresh inventory data - check CSV file",
                success=False
            )
        
        return MessageResponse(
            message="Inventory data refreshed successfully",
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refreshing inventory: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """API health check"""
    user_count = auth_manager.get_user_count()
    return {
        "status": "healthy",
        "message": "Authentication API is running",
        "user_count": user_count,
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "KMRL Authentication & Inventory API",
        "version": "1.0.0",
        "endpoints": [
            "/register - POST - Register new user",
            "/login - POST - User login",
            "/me - GET - Current user info",
            "/logout - POST - User logout",
            "/users - GET - All users (admin only)",
            "/inventory/summary - GET - Inventory summary",
            "/inventory/parts - GET - Inventory parts with filters",
            "/inventory/reorder-report - GET - Prioritized reorder report",
            "/inventory/refresh - GET - Refresh inventory data (admin only)",
            "/health - GET - Health check"
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting KMRL Authentication API...")
    print("📝 Default admin user: admin / admin123")
    print("🌐 API will be available at: http://localhost:8001")
    print("📚 API docs will be available at: http://localhost:8001/docs")
    
    uvicorn.run(
        "auth_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )