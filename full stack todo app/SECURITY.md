# Todo API Backend - Security Features

This document outlines the security features implemented in the Todo API backend.

## Security Measures Implemented

### 1. JWT-Based Authentication
- Secure JWT tokens with configurable expiration
- Separate access and refresh tokens
- Strong cryptographic signing using python-jose
- Automatic token refresh mechanism

### 2. User Authorization
- Role-based access control
- User data isolation (users can only access their own todos)
- Secure session management
- Proper validation of user permissions

### 3. Input Validation and Sanitization
- Pydantic models with field validation
- SQL injection prevention through SQLModel ORM
- Size limits and type checks for all inputs
- Email format validation

### 4. Rate Limiting
- Per-endpoint rate limiting using slowapi
- Different limits for different endpoints:
  - Login: 10 requests per minute
  - Registration: 5 requests per hour
  - Todo operations: 10-30 requests per minute depending on the operation
- IP-based rate limiting

### 5. Security Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security with long max-age
- Content-Security-Policy with default-src 'self'

### 6. HTTPS and Transport Security
- Enforced HTTPS in production
- Secure cookies with HttpOnly and Secure flags
- Encrypted communication for all API requests

### 7. Error Handling
- Generic error messages to prevent information disclosure
- Detailed server-side logging without sensitive data
- Proper exception handling for all endpoints

## API Endpoints Security

### Authentication Endpoints
- `/api/register` - Limited to 5 requests per hour per IP
- `/api/login` - Limited to 10 requests per minute per IP
- `/api/refresh` - Limited to 5 requests per minute per IP

### Todo Endpoints
- `/api/todos` - All operations require valid JWT
- User data isolation enforced at the application level
- Rate limits vary by operation type

## Configuration

Security settings are configured in `config.py`:
- `SECRET_KEY`: Secret key for JWT signing (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token lifetime
- Rate limiting settings are configured in the respective route decorators

## Best Practices Followed

- Principle of least privilege
- Defense in depth
- Fail secure
- Complete mediation
- Open design
- Separation of privilege
- Least common mechanism
- Psychological acceptability

## Production Recommendations

Before deploying to production:
1. Change the default SECRET_KEY to a strong, randomly generated value
2. Configure proper CORS settings (currently allowing all origins for development)
3. Set up HTTPS with a valid certificate
4. Monitor logs for security events
5. Regularly rotate secrets and tokens
6. Implement additional monitoring and alerting for suspicious activities