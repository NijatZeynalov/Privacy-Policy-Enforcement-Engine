# Privacy Policy Enforcement Engine

A machine learning-powered system that dynamically enforces privacy policies based on real-time analysis of data access patterns and user contexts.

## 🛠️ Installation

1. Clone the repository

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## 📋 Usage

### Basic Usage
```python
from privacy_engine import PrivacyEngine

# Initialize engine
engine = PrivacyEngine()

# Check access permission
result = engine.check_access(
    user_id="user123",
    data_type="customer_data",
    action="read",
    context={
        "location": "office",
        "device": "laptop",
        "time": "2024-01-01T09:00:00"
    }
)

print(f"Access allowed: {result['allowed']}")
```

### Policy Configuration
```python
# Add new policy
engine.policy_manager.add_policy(
    "sensitive_data_policy",
    {
        "rules": [
            {
                "data_type": "customer_data",
                "conditions": {
                    "location": ["office", "vpn"],
                    "time_range": ["09:00", "17:00"]
                },
                "action": "allow"
            }
        ]
    }
)
```

### Context Management
```python
# Update user context
engine.context_handler.update_context(
    "user123",
    {
        "location": "remote",
        "device": "mobile",
        "risk_flags": ["new_device"]
    }
)
```
