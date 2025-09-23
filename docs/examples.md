# Examples

This directory contains example specifications to help you get started with goal-dev-spec.

## Simple Goal Example

```yaml
id: "abc123"
title: "Implement user authentication"
description: "Create a user authentication system with login, registration, and password reset functionality."
objectives:
  - "Implement user registration with email verification"
  - "Create secure login functionality"
  - "Add password reset capability"
success_criteria:
  - "Users can register with a valid email address"
  - "Users can login with their credentials"
  - "Users can reset their password via email"
dependencies: []
related_goals: []
priority: "high"
status: "in_progress"
created_at: "2023-05-15T10:30:00Z"
updated_at: "2023-05-20T14:22:00Z"
owner: "development-team"
tags:
  - "authentication"
  - "security"
metadata:
  estimated_duration: "2 weeks"
```

## Complex Goal with Dependencies

```yaml
id: "def456"
title: "Implement e-commerce checkout flow"
description: "Create a complete checkout flow including cart management, payment processing, and order confirmation."
objectives:
  - "Implement shopping cart functionality"
  - "Integrate with payment processor"
  - "Create order management system"
  - "Send order confirmation emails"
success_criteria:
  - "Users can add/remove items from cart"
  - "Payment processing works securely"
  - "Orders are stored in database"
  - "Confirmation emails are sent"
dependencies:
  - "abc123"  # Depends on user authentication
related_goals:
  - "ghi789"  # Related to product catalog
priority: "critical"
status: "planned"
created_at: "2023-05-18T09:15:00Z"
updated_at: "2023-05-18T09:15:00Z"
owner: "ecommerce-team"
tags:
  - "ecommerce"
  - "checkout"
  - "payment"
metadata:
  estimated_duration: "3 weeks"
  budget: "$15000"
```