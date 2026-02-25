# Cloud Computing: AWS Watermark project

This project is a serverless website for ***automatic image watermarking*** built entirely on ***AWS cloud services***. Users can upload images, apply custom watermarks, and download the processed images instantly. 

### Architecture - This system uses a serverless architecture with multiple AWS services:

- API Gateway: Entry point for HTTP requests, routes requests to Lambda functions.
- AWS Lambda: Implements core functionality:
- HealthCheckFunction – responds with service status (GET /)
- ShowFormFunction – serves HTML form for watermarking (GET /form)
- WatermarkFunction – processes uploaded images and applies watermarks (POST /watermark)
- AWS SAM: Simplifies deployment and management of serverless resources.

### Functional Features: 

- Image Upload: Users upload images for watermarking.
- Custom Watermark: Enter watermark text and customize font size and color.
- Automatic Download: Watermarked images are automatically downloaded after processing.
- Web Form Interface: Interactive HTML form for uploading images and configuring watermarks.

### Non-Functional Features:

- High Availability: API Gateway throttling ensures up to 10,000 requests/sec with burst capacity of 5,000.
- Fast Response: Watermark processing latency measured at approx. 0.4 seconds via AWS X-Ray.
- Scalability: Lambda functions scale horizontally to handle multiple concurrent requests.
- Monitoring & Debugging: Integrated AWS CloudWatch and X-Ray for latency tracking and error detection.

### Technologies & Skills:

- Cloud Computing & Serverless Architecture: AWS Lambda, API Gateway, AWS SAM
- Monitoring & Logging: AWS CloudWatch, AWS X-Ray
- Web Development: HTML form rendering, user input handling
- Python Programming: Image processing using PIL (Python Imaging Library)
- Infrastructure: AWS CloudFormation / SAM templates

---

sam package --template-file sam.yaml --output-template-file packaged.yaml --resolve-s3

sam deploy --template-file packaged.yaml --stack-name <CUSTOM-NAME> --capabilities CAPABILITY_IAM

---

sam build -t sam.yaml

sam deploy --guided
