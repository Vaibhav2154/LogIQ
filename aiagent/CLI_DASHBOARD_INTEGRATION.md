# CLI-Dashboard Integration Implementation

## Overview
This document describes the implementation of the CLI-Dashboard integration feature that updates the `cli_active` field in the users model when a user starts the CLI tool, and displays this status on the dashboard instead of active attacks.

## Changes Made

### 1. Server-Side Changes

#### Updated User Model (`server/model/users.py`)
- Added `cli_active: bool | None = None` to the `UserUpdate` model
- This allows the CLI tool to update the user's CLI active status

#### Existing User Update Endpoint (`server/routers/users.py`)
- The existing `PUT /users/me` endpoint already supports updating user fields
- No changes needed - it automatically supports the new `cli_active` field

### 2. CLI Tool Changes (`aiagent/cli_tool.py`)

#### New Methods Added:
- `_update_cli_status(is_active: bool)` - Updates the user's CLI active status on the server
- `cleanup_cli_status()` - Sets CLI status to False when CLI tool exits

#### Modified Methods:
- `authenticate()` - Now calls `_update_cli_status(True)` after successful authentication
- `__init__()` - Sets up cleanup handlers and updates CLI status if user is already authenticated
- `main()` - Added cleanup handlers for graceful exit (SIGINT, SIGTERM, atexit)

#### Key Features:
- **Automatic Status Update**: CLI status is set to `True` when user authenticates
- **Graceful Cleanup**: CLI status is set to `False` when CLI tool exits
- **Error Handling**: Robust error handling for network issues
- **Non-blocking**: Status updates don't block CLI operations

### 3. Dashboard Changes (`client/app/dashboard/page.tsx`)

#### New State:
- Added `userProfile` state to store user information including `cli_active` status

#### New Functions:
- `fetchUserProfile()` - Fetches user profile from `/users/me` endpoint

#### Modified UI:
- **Replaced "THREATS_ACTIVE"** with **"CLI_STATUS"** in the stats section
- **Dynamic Status Display**: Shows "ACTIVE" (green) or "INACTIVE" (gray) based on `cli_active`
- **Dynamic Icons**: Shows 🖥️ for active, 💤 for inactive
- **Real-time Updates**: Refreshes user profile every 5 seconds to show live status

#### Visual Changes:
- Changed from red warning icon (⚠️) to computer icons (🖥️/💤)
- Color coding: Green for active, Gray for inactive
- Maintains the same terminal-style aesthetic

### 4. Testing

#### Test Script (`aiagent/test_cli_dashboard_integration.py`)
- Comprehensive test suite to verify the integration
- Tests authentication, status updates, and cleanup
- Provides detailed feedback on each step

## How It Works

### 1. CLI Startup Flow
```
User starts CLI tool
    ↓
CLI initializes and loads credentials
    ↓
If user is authenticated:
    ↓
CLI calls _update_cli_status(True)
    ↓
Server updates user.cli_active = True
    ↓
Dashboard shows "CLI_STATUS: ACTIVE" 🖥️
```

### 2. CLI Exit Flow
```
User exits CLI tool (Ctrl+C, close, etc.)
    ↓
Cleanup handlers are triggered
    ↓
CLI calls _update_cli_status(False)
    ↓
Server updates user.cli_active = False
    ↓
Dashboard shows "CLI_STATUS: INACTIVE" 💤
```

### 3. Dashboard Display Flow
```
Dashboard loads
    ↓
fetchUserProfile() called
    ↓
GET /users/me returns user data
    ↓
Display cli_active status in stats section
    ↓
Refresh every 5 seconds for real-time updates
```

## API Endpoints Used

### 1. Authentication
- `POST /login` - User authentication
- Returns JWT token for subsequent requests

### 2. User Profile Management
- `GET /users/me` - Get current user profile (including cli_active)
- `PUT /users/me` - Update user profile (including cli_active)

### 3. Request/Response Format

#### Update CLI Status Request:
```http
PUT /users/me
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "cli_active": true
}
```

#### User Profile Response:
```json
{
  "email": "user@example.com",
  "username": "testuser",
  "cli_active": true
}
```

## Benefits

### 1. Real-time Visibility
- Dashboard users can see which CLI tools are currently active
- Helps with monitoring and resource management

### 2. Better User Experience
- Clear indication of CLI tool status
- Consistent with the terminal-style dashboard theme

### 3. System Monitoring
- Operators can see active CLI sessions
- Useful for security and operational monitoring

### 4. Graceful Cleanup
- CLI status is properly cleaned up on exit
- Prevents stale "active" status

## Error Handling

### 1. Network Issues
- CLI continues to work even if status update fails
- Non-blocking error handling with logging

### 2. Authentication Issues
- Status updates only happen for authenticated users
- Graceful fallback if authentication fails

### 3. Dashboard Resilience
- Dashboard continues to work if user profile fetch fails
- Shows default state until successful fetch

## Future Enhancements

### 1. Multiple CLI Sessions
- Track multiple CLI sessions per user
- Show session count instead of boolean status

### 2. Session Details
- Show CLI session start time
- Display last activity timestamp

### 3. CLI Activity Logging
- Log CLI commands and activities
- Display recent CLI activity on dashboard

### 4. Notifications
- Notify dashboard users when CLI becomes active/inactive
- Real-time updates without polling

## Testing

### Manual Testing
1. Start CLI tool and authenticate
2. Check dashboard shows "CLI_STATUS: ACTIVE"
3. Exit CLI tool
4. Check dashboard shows "CLI_STATUS: INACTIVE"

### Automated Testing
```bash
cd aiagent
python test_cli_dashboard_integration.py
```

## Conclusion

The CLI-Dashboard integration provides real-time visibility into CLI tool usage, enhancing the overall user experience and system monitoring capabilities. The implementation is robust, user-friendly, and maintains the existing terminal-style aesthetic of the dashboard.
